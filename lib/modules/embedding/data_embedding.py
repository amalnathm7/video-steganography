import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_dir)
import cv2
import math
from preprocessing.encrypt import encrypt_data
import selection.frame_selection as fs
import selection.region_selection as rs
import pickle
import random
import base64


INIT_DATA_THRESHOLD = 0.1


def int_to_binary(n):
    return bin(n).replace("0b", "").zfill(8)


def option(opt):
    match opt:
        case 1: return "akiyo"
        case 2: return "bowing"
        case 3: return "bus"
        case 4: return "carphone"
        case 5: return "city"
        case 6: return "crew"
        case 7: return "deadline"
        case 8: return "football"
        case 9: return "salesman"
        case 10: return "suzie"


def base64_enc_dec(data ):
    return base64.b64encode(data).decode('utf-8')


def file_to_binary(file_path):
    print("\nAccessing file " + file_path)
    file = open(file_path, "rb")
    data = file.read()
    return data_to_binary(data=data)


def data_to_binary(data):
    encrypted_data, iv, key = encrypt_data(data)
    data_hex = base64_enc_dec(encrypted_data)
    data = base64_enc_dec(key) + "$" + base64_enc_dec(iv) + "$" + str(len(data_hex)) + "$" + data_hex
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


def get_init_frames(total_frames, count):
    list = [i for i in range(0, total_frames)]
    random.seed(len(list))
    return random.sample(list, count)


def embed_data(cap, writer, binary_data):
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    pixel_count = len(binary_data)
    is_embedded = False

    if total_frames == 0:
        print("\nNo frames in cover video!\n")
        return
    
    if (width < len(str(pixel_count) + "$")): # To embed pixel_count in the first row of first frame
        print("\nData is large!\n")
        return

    init_frames_count = 0

    while ((width * height * init_frames_count) < (pixel_count * INIT_DATA_THRESHOLD)):
        init_frames_count += 1

    init_frames = get_init_frames(total_frames=int(total_frames), count=init_frames_count)

    no_of_blocks = 1

    block_size = math.floor(math.sqrt(min(width, height)))
    no_of_frames = math.ceil(pixel_count / (block_size * block_size * no_of_blocks))

    while no_of_frames > (total_frames - init_frames_count):
        no_of_blocks += 1
        no_of_frames = math.ceil(pixel_count / (block_size * block_size * no_of_blocks))

    if(block_size * block_size * no_of_blocks > width * height):
        print("\nData is large!\n")
        return

    print("\nSelecting robust frames")

    # selected_frames = []
    # for i in range(0, int(total_frames)):
    #     if i not in init_frames:
    #         selected_frames.append(i)
    
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    selected_frames = fs.histogram_difference_frame_selection(cap=cap, frame_count=no_of_frames, init_frames=init_frames)
    # selected_frames = fs.ssim_frame_selection(cap=cap, frame_count=no_of_frames, init_frames=init_frames)

    # selected_frames.sort()
    # print(f'\nSelected frames: {selected_frames}')

    print("\nSelecting robust regions")

    # selected_regions = {}
    # for i in range(0, int(total_frames)):
    #         if i not in init_frames:
    #             if i == 0:
    #                 selected_regions[i] = [{'start': (1, 0), 'end': (int(height) - 1, int(width) - 1)}]
    #             else:
    #                 selected_regions[i] = [{'start': (0, 0), 'end': (int(height) - 1, int(width) - 1)}]

    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    selected_regions = rs.pca_region_selection(
        cap=cap, block_size=block_size, frame_list=selected_frames, no_of_blocks=no_of_blocks)
    # selected_regions = rs.gwo_region_selection(cap=cap, msg_size=block_size,
    #                         frame_list=selected_frames, no_of_blocks=no_of_blocks)

    # print(f'\nSelected regions: {selected_regions}')

    init_data = {}
    for frame in selected_regions:
        data = []

        for region in selected_regions[frame]:
            data.append(region['start'])

        init_data[frame] = data

    init_binary_data = data_to_binary(data=pickle.dumps(init_data))
    init_pixel_count = len(init_binary_data)

    frame_no = 0
    init_count = 0
    count = 0
    is_init_embedded = False
    is_embedded = False

    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if (frame_no == 0):
            pixel_count_str = str(pixel_count) + "$"

            j = 0
            for c in pixel_count_str:
                binary = format(ord(c), '08b')
                adaptive_lsb332_embedding(binary=binary, region=frame, i=0, j=j)
                j += 1

        if frame_no in init_frames:
            if (not is_init_embedded):
                for i in range(0, height):
                    if (frame_no == 0 and i == 0):
                        continue
                    
                    for j in range(0, width):
                        binary = init_binary_data[init_count]
                        init_count += 1

                        adaptive_lsb332_embedding(binary=binary, region=frame, i=i, j=j)

                        if (init_count == init_pixel_count):
                            is_init_embedded = True
                            break

                    if is_init_embedded:
                        break
        elif frame_no in selected_frames:
            if (not is_embedded):
                for element in selected_regions[frame_no]:
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

                            if (count == pixel_count):
                                is_embedded = True
                                break

                        if is_embedded:
                            break

                    if is_embedded:
                        break
        
        writer.write(frame)
        frame_no += 1

    writer.write(frame)

    if (init_count < init_pixel_count or count < pixel_count):
        print("\nEmbedding error!\n")
    else:
        print(f"\nEmbedded successfully\n")


def data_embedding():
    print("\nVideo Steganography\n")

    flag = True
    
    while flag:
        print("1. akiyo\n2. bowing\n3. bus\n4. carphone\n5. city\n6. crew\n7. deadline\n8. football\n9. salesman\n10. suzie\n")
        opt = int(input("Select cover video: "))

        if (1 <= opt <= 10):
            filename = option(opt)
            cap = cv2.VideoCapture(f'assets/cover_videos/{filename}_cif.y4m')

            video_fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
            height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            flag = False
        else:
            print("\nInvalid option!\n")

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

        if file_type not in [1, 2, 3, 4]:
            print("\nInvalid option!")
            continue
        
        flag = False
        flag2 = True

        while (flag2):
            print("\n1. 10 KB\n2. 50 KB\n3. 100 KB\n4. 500 KB\n5. 1 MB\n6. 5 MB\n7. 10 MB\n")
            input_size = int(input("Select input size: "))

            if(input_size < 1 or input_size > 7):
                print("\nInvalid option!")
                continue

            flag2 = False
            
            match file_type:
                case 1:
                    input_file_path = f"assets/secret_files/texts/input{input_size}.txt"
                case 2:
                    input_file_path = f"assets/secret_files/images/input{input_size}.jpg"
                case 3:
                    input_file_path = f"assets/secret_files/audios/input{input_size}.mp3"
                case 4:
                    input_file_path = f"assets/secret_files/videos/input{input_size}.mp4"

            binary_data = file_to_binary(file_path=input_file_path)

            embed_data(cap=cap, writer=writer, binary_data=binary_data)
    
    writer.release()
    cap.release()

if __name__ == '__main__':
    data_embedding()