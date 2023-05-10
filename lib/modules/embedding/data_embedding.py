import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_dir)
import cv2
import math
from preprocessing.encrypt import encrypt_data
import selection.frame_selection as fs
import selection.region_selection as rs


def int_to_binary(n):
    return bin(n).replace("0b", "").zfill(8)


def option(opt):
    match opt:
        case 1: return "akiyo"
        case 2: return "bowing"
        case 3: return "bus"
        case 4: return "city"
        case 5: return "crew"


def to_binary(file_path):
    print("\nAccessing file " + file_path)
    file = open(file_path, "rb")
    data = file.read()
    encrypted_data, iv, key = encrypt_data(data)
    data_hex = encrypted_data.hex()
    data = key.hex() + "$" + iv.hex() + "$" + str(len(data_hex)) + "$" + data_hex
    binary_data = [format(ord(char), '08b') for char in data]
    return binary_data


def adaptive_lsb332_embedding(binary, region, i, j):
    threshold = 9
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

    if (penalty >= threshold):
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
    flag = False

    ret, frame = cap.read()
    if not ret:
        print("No frames in cover video!")
        return

    no_of_blocks = 1

    block_size = math.floor(math.sqrt(min(width, height)))
    no_of_frames = math.ceil(pixel_count / (block_size * block_size * no_of_blocks))

    while no_of_frames > total_frames:
        no_of_blocks += 1
        no_of_frames = math.ceil(pixel_count / (block_size * block_size * no_of_blocks))

    print("\nSelecting robust frames")

    selected_frames = fs.histogram_difference(
        cap=cap, frame_count=no_of_frames)
    
    # selected_frames = []
    # for i in range(0, int(total_frames)):
    #     selected_frames.append(i)

    # selected_frames.sort()
    # print(f'\nSelected frames: {selected_frames}')

    print("\nSelecting robust regions")

    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # selected_regions = {}

    # for i in range(1, 300):
    #     selected_regions[i] = [{'start': (0, 0), 'end': (200, 200)}]

    selected_regions = rs.PCA_Implementation(
        cap=cap, block_size=block_size, frame_list=selected_frames, no_of_blocks=no_of_blocks)

    # selected_regions = rs.GWO(cap=cap, msg_size=block_size,
    #                         frame_list=selected_frames, no_of_blocks=no_of_blocks)

    region = frame[0:height, 0:width]

    selected_frames_string = ""

    for i in range(0, len(selected_frames)):
        selected_frames_string += f'{str(selected_frames[i])},'

    init_string = f'{pixel_count}${selected_frames_string}$'

    count = 0

    for i in range(0, height):
        for j in range(0, width):
            init_binary = [format(ord(char), '08b') for char in init_string]
            adaptive_lsb332_embedding(
                binary=init_binary[count], region=region, i=i, j=j)
            count += 1

            if (count == len(init_binary)):
                flag = True
                break

        if (flag):
            break

    if (count != len(init_binary)):
        print("Data is large!")

    writer.write(frame)

    cap.set(cv2.CAP_PROP_POS_FRAMES, 1)  # Skipping the first frame
    frame_no = 1
    count = 0
    flag = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if flag:
            writer.write(frame)
            continue

        if frame_no in selected_frames:
            index = 0

            for element in selected_regions[frame_no]:
                index += 1
                
                region = frame[element['start'][0]:element['end']
                               [0] + 1, element['start'][1]:element['end'][1] + 1]
                region_height = element['end'][0] + 1 - element['start'][0]
                region_width = element['end'][1] + 1 - element['start'][1]

                for i in range(0, region_height):
                    for j in range(0, region_width):
                        binary = binary_data[count]
                        count += 1

                        adaptive_lsb332_embedding(
                            binary=binary, region=region, i=i, j=j)

                        if (count == len(binary_data)):
                            flag = True
                            break

                    if (flag):
                        break

                if (flag):
                    break

            print(index)
            print(no_of_blocks)

        writer.write(frame)
        frame_no = frame_no + 1

    if (count < len(binary_data)):
        print("\nData is large!")
    else:
        print("\nEmbedded successfully\n")

    writer.release()
    cap.release()


def data_embedding():
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
        print("\n1. Text\n2. Image\n3. Audio\n4. Video\n")
        file_type = int(input("Select secret file type: "))

        flag = False

        match file_type:
            case 1:
                input_file_path = "assets/secret_files/texts/input6.txt"
            case 2:
                input_file_path = "assets/secret_files/images/input1.jpg"
            case 3:
                input_file_path = "assets/secret_files/audios/input1.mp3"
            case 4:
                input_file_path = "assets/secret_files/videos/input1.mp4"
            case _:
                print("Invalid option!")
                flag = True
                continue

        binary_data = to_binary(file_path=input_file_path)

        embed_data(cap=cap, writer=writer, binary_data=binary_data)

if __name__ == '__main__':
    data_embedding()