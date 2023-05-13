import sys
import os
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_dir)
import selection.region_selection as rs
from preprocessing.decrypt import decrypt_data
import math
import cv2
import pickle
import random


INIT_DATA_THRESHOLD = 0.15


def option(opt):
    match opt:
        case 1: return "akiyo"
        case 2: return "bowing"
        case 3: return "bus"
        case 4: return "city"
        case 5: return "crew"


def decimal_to_binary(n, fill):
    return bin(n).replace("0b", "").zfill(fill)


def binary_to_decimal(n):
    return int(n, 2)


def get_init_frames(total_frames, count):
    list = [i for i in range(0, total_frames)]
    random.seed(len(list))
    return random.sample(list, count)


def adaptive_lsb332_extraction(region, i, j):
    a = region[i, j, 0] - (math.floor(region[i, j, 0] / 8) * 8)
    b = region[i, j, 1] - (math.floor(region[i, j, 1] / 8) * 8)
    c = region[i, j, 2] - (math.floor(region[i, j, 2] / 4) * 4)

    binary = decimal_to_binary(
        a, 3) + decimal_to_binary(b, 3) + decimal_to_binary(c, 2)
    num = binary_to_decimal(binary)

    if (num >= 128):
        num = ~int(binary, 2) & 0b11111111

    return num


def extract_data(cap, type):
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    selected_frames = []
    selected_regions = {}
    extracted_len = -1
    total_len = 0
    data = ""
    flag = False
    data = ""
    key = None
    iv = None
    frame_no = 0

    pixel_count = int(input("\nEnter secret code: "))
    init_frames_count = 0

    while ((width * height * init_frames_count) < (pixel_count * INIT_DATA_THRESHOLD)):
        init_frames_count += 1

    init_frames = get_init_frames(total_frames=int(total_frames), count=init_frames_count)
    block_size = math.floor(math.sqrt(min(width, height)))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if (frame_no in init_frames):
            for i in range(0, height):
                for j in range(0, width):
                    ch = chr(adaptive_lsb332_extraction(region=frame, i=i, j=j))

                    if (extracted_len == -1 and ch == '$'):
                        if (key == None):
                            key = bytes.fromhex(data)
                            data = ""
                        elif (iv == None):
                            iv = bytes.fromhex(data)
                            data = ""
                        else:
                            total_len = int(data)
                            data = ""
                            extracted_len = 0
                    elif extracted_len < total_len:
                        if (extracted_len != -1):
                            extracted_len += 1
                        data += ch
                    else:
                            extracted_data = decrypt_data(bytes.fromhex(data), iv, key)

                            init_data = pickle.loads(extracted_data)

                            print("\nIdentifying selected frames")

                            print("\nIdentifying selected regions")

                            for frame in init_data:
                                selected_frames.append(frame)
                                selected_regions[frame] = []

                                for region in init_data[frame]:
                                    selected_regions[frame].append({'start': region, 'end': (region[0] + block_size - 1, region[1] + block_size - 1)})

                            flag = True
                            break

                if (flag):
                    break

        frame_no += 1
        
        if (flag):
            break

    data = ""
    total_len = 0
    extracted_len = -1
    key = None
    iv = None
    flag = False
    frame_no = 0

    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_no in selected_frames:
            for element in selected_regions[frame_no]:
                region = frame[element['start'][0]:element['end']
                               [0] + 1, element['start'][1]:element['end'][1] + 1]
                region_height = element['end'][0] + 1 - element['start'][0]
                region_width = element['end'][1] + 1 - element['start'][1]

                for i in range(0, region_height):
                    for j in range(0, region_width):
                        ch = chr(adaptive_lsb332_extraction(
                            region=region, i=i, j=j))

                        if (extracted_len == -1 and ch == '$'):
                            if (key == None):
                                key = bytes.fromhex(data)
                                data = ""
                            elif (iv == None):
                                iv = bytes.fromhex(data)
                                data = ""
                            else:
                                total_len = int(data)
                                data = ""
                                extracted_len = 0
                        elif extracted_len < total_len:
                            if (extracted_len != -1):
                                extracted_len += 1
                            data += ch
                        else:
                                extracted_data = decrypt_data(bytes.fromhex(data), iv, key)

                                match type:
                                    case 1:
                                        output_file_path = "assets/extracted_files/texts/output.txt"
                                    case 2:
                                        output_file_path = "assets/extracted_files/texts/output.jpg"
                                    case 3:
                                        output_file_path = "assets/extracted_files/texts/output.mp3"
                                    case 4:
                                        output_file_path = "assets/extracted_files/texts/output.mp4"

                                file = open(output_file_path, "wb")

                                file.write(extracted_data)

                                print(
                                    f'\n{output_file_path} successfully created\n')
                                
                                flag = True
                                break
                    if (flag):
                        break

                if (flag):
                    break

            if (flag):
                break

        frame_no += 1

    cap.release()
    cv2.destroyAllWindows()


def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def data_extraction():
    print("\nVideo Steganography")

    flag = False
    while not flag:
        print("1. akiyo\n2. bowing\n3. bus\n4. city\n5. crew\n")
        opt = int(input("Select stego video: "))
        if (opt > 0 and opt < 6):
            flag = True

    filename = option(opt)
    cap = cv2.VideoCapture(f'assets/stego_videos/{filename}_stego.avi')
    print(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    flag = True

    while (flag):
        print("\n1. Text\n2. Image\n3. Audio\n4. Video\n")
        file_type = int(input("Select secret file type: "))

        match (file_type):
            case 1:
                create_folder("assets/extracted_files/texts")
            case 2:
                create_folder("assets/extracted_files/images")
            case 3:
                create_folder("assets/extracted_files/audios")
            case 4:
                create_folder("assets/extracted_files/videos")

        flag = False

        if file_type in [1, 2, 3, 4]:
            extract_data(cap=cap, type=file_type)
        else:
            print("Invalid option!")
            flag = True


if __name__ == '__main__':
    data_extraction()