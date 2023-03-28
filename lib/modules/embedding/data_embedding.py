import math
import cv2
from PIL import Image
import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_dir)
from encryption.imgenc import encrypt_image_data
from encryption.textenc import encrypt_text
import selection.frame_selection as fs
import selection.region_selection as rs
import io


THRESHOLD = 9


def int_to_binary(n):
    return bin(n).replace("0b", "").zfill(8)


def option(opt):
    match opt:
        case 1: return "akiyo"
        case 2: return "bowing"
        case 3: return "bus"
        case 4: return "city"
        case 5: return "crew"


def text_to_binary(file_path):
    file = open(file_path, "r")

    data = file.read()

    encrypted_data, iv, key = encrypt_text(data)

    data_hex = encrypted_data.hex()

    data = key.hex() + "$" + iv.hex() + "$" + str(len(data_hex)) + "$" + data_hex

    binary_data = [format(ord(char), '08b') for char in data]

    return binary_data


def image_to_binary(file_path):
    img = Image.open(file_path)

    bytes_io = io.BytesIO()

    img.save(bytes_io, format=img.format.lower())

    bytes_data = bytes_io.getvalue()

    encrypted_data, key, iv = encrypt_image_data(bytes_data)

    data_hex = encrypted_data.hex()

    data = key.hex() + "$" + iv.hex() + "$" + str(len(data_hex)) + "$" + data_hex

    binary_data = [format(ord(char), '08b') for char in data]

    return binary_data


def video_to_binary(file_path):
    pass
    # cap = cv2.VideoCapture(file_path)

    # height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # video_fps = int(cap.get(cv2.CAP_PROP_FPS))
    # total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # data = "{}${}${}${}$".format(width, height, video_fps, total_frames)
    # binary_data = [format(ord(char), '08b') for char in data]

    # while True:
    #     ret, frame = cap.read()
    #     if not ret:
    #         break

    #     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    #     for x in range(height):
    #         for y in range(width):
    #             r, g, b = rgb_frame[x][y]

    #             binary_data.append(int_to_binary(r))
    #             binary_data.append(int_to_binary(g))
    #             binary_data.append(int_to_binary(b))

    # return binary_data


def adaptive_inverted_lsb332_embedding(binary, region, i, j):
    r_binary = int_to_binary(region[i, j, 0])
    g_binary = int_to_binary(region[i, j, 1])
    b_binary = int_to_binary(region[i, j, 2])

    r_penalty = (int(binary[0]) * 4) ^ int(r_binary[5]) + (
        int(binary[1]) * 2) ^ int(r_binary[6]) + (int(binary[2])) ^ int(r_binary[7])
    g_penalty = (int(binary[3]) * 4) ^ int(g_binary[5]) + (
        int(binary[4]) * 2) ^ int(g_binary[6]) + (int(binary[5])) ^ int(g_binary[7])
    b_penalty = (
        int(binary[6]) * 4) ^ int(b_binary[5]) + (int(binary[7]) * 2) ^ int(b_binary[6])

    penalty = r_penalty + g_penalty + b_penalty
    
    if(penalty >= THRESHOLD):
        binary = str(int_to_binary(~int(binary, 2) & 0b11111111))

    region[i, j, 0] = math.floor(
        region[i, j, 0] / 8) * 8 + (int(binary[2]) + int(binary[1]) * 2 + int(binary[0]) * 4)
    region[i, j, 1] = math.floor(
        region[i, j, 1] / 8) * 8 + (int(binary[5]) + int(binary[4]) * 2 + int(binary[3]) * 4)
    region[i, j, 2] = math.floor(
        region[i, j, 2] / 4) * 4 + (int(binary[7]) + int(binary[6]) * 2)
    
    return region


def embed_data(cap, writer, binary_data):
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    pixel_count = len(binary_data)
    index = 0
    flag = False

    ret, frame = cap.read()
    if not ret:
        print("No frames in cover video!")
        return

    region = frame[0:height, 0:width]

    for i in range(0, height):
        for j in range(0, width):
            if(index == len(str(pixel_count))):
                adaptive_inverted_lsb332_embedding(binary="00001010", region=region, i=i, j=j) # Embed binary of 10 as a delimiter
                flag = True
                break

            binary = int_to_binary(int(str(pixel_count)[index]))
            adaptive_inverted_lsb332_embedding(binary=binary, region=region, i=i, j=j)
            index += 1
        if(flag):
            break

    writer.write(frame)
    
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    no_of_blocks = 1

    no_of_frames = math.ceil(pixel_count / (min(width, height) * no_of_blocks))

    while no_of_frames > total_frames:
        no_of_blocks += 1
        no_of_frames = math.ceil(pixel_count / (math.ceil(math.sqrt(min(width, height)))
                                 * math.ceil(math.sqrt(min(width, height))) * no_of_blocks))

    block_size = math.ceil(math.sqrt(min(width, height)))

    selected_frames = fs.histogram_difference(
        cap=cap, frame_count=no_of_frames)
    
    # TODO
    
    selected_frames.sort()
    print(selected_frames)

    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    selected_regions = {}

    # for i in range(1, 300):
    #     selected_regions[i] = [{'start': (0, 0), 'end': (200, 200)}]

    selected_regions = rs.PCA_Implementation(
        cap=cap, block_size=block_size, frame_list=selected_frames, no_of_blocks=no_of_blocks)

    # selected_regions = rs.GWO(cap=cap, msg_size=math.ceil(math.sqrt(pixel_count)),
    #                         frame_list=selected_frames, no_of_blocks=no_of_blocks)

    cap.set(cv2.CAP_PROP_POS_FRAMES, 1) # Skipping the first frame
    frame_no = 0
    count = 0
    flag = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_no = frame_no + 1

        if flag:
            writer.write(frame)
            continue

        if frame_no in selected_frames:
            for element in selected_regions[frame_no]:
                region = frame[element['start'][0]:element['end']
                               [0] + 1, element['start'][1]:element['end'][1] + 1]
                region_height = element['end'][0] + 1 - element['start'][0]
                region_width = element['end'][1] + 1 - element['start'][1]

                for i in range(0, region_height):
                    for j in range(0, region_width):
                        binary = binary_data[count]
                        count += 1

                        adaptive_inverted_lsb332_embedding(binary=binary, region=region, i=i, j=j)

                        if (count == len(binary_data)):
                            flag = True
                            break

                    if (flag):
                        break

                if (flag):
                    break

        writer.write(frame)

    if (count < len(binary_data)):
        print("\nData is large!")
    else:
        print("\nEmbedded successfully")

    writer.release()
    cap.release()


def main():
    print("\nVideo Steganography")

    flag = True
    while flag:
        print("\n1. akiyo\n2. bowing\n3. bus\n4. city\n5. crew\n")
        opt = int(input("Select cover video: "))

        if (opt > 0 and opt < 6):
            filename = option(opt)
            cap = cv2.VideoCapture(f'assets/cover_videos/{filename}_cif.y4m')

            video_fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
            height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            flag = False
        else:
            print("Invalid option!")

    print(
        f"\nVideo: {filename}\nFrame per second: {video_fps}\nTotal frames: {total_frames}\nHeight: {height}\nWidth: {width}")

    if not os.path.exists('assets/stego_videos'):
        os.makedirs('assets/stego_videos')
    fourcc = cv2.VideoWriter_fourcc(*'FFV1')
    writer = cv2.VideoWriter(f'assets/stego_videos/{filename}_stego.avi', apiPreference=0, fourcc=fourcc,
                             fps=video_fps, frameSize=(int(width), int(height)))

    flag = True

    while (flag):
        print("\n1. Text\n2. Image\n3. Video\n")
        file_type = int(input("Select secret file type: "))

        flag = False

        if (file_type == 1):
            embed_data(cap=cap, writer=writer,
                             binary_data=text_to_binary("assets/secret_files/texts/input0.txt"))
        elif (file_type == 2):
            embed_data(cap=cap, writer=writer,
                             binary_data=image_to_binary('assets/secret_files/images/input1.jpg'))
        elif (file_type == 3):
            embed_data(cap=cap, writer=writer, binary_data=video_to_binary(
                'assets/secret_files/videos/input1.mp4'))
        else:
            print("Invalid option!")
            flag = True


if __name__ == '__main__':
    main()
