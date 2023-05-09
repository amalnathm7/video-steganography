import sys
import os
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_dir)
import selection.frame_selection as fs
import selection.region_selection as rs
from decryption.imgdec import decrypt_image_data
from decryption.textdec import decrypt_text
from PIL import Image
import math
import cv2
import io


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
    data = ""
    flag = False
    pixel_count = 0
    selected_frames = []

    ret, frame = cap.read()
    if not ret:
        print("No frames in stego video!")
        return

    region = frame[0:height, 0:width]

    for i in range(0, height):
        for j in range(0, width):
            num = adaptive_lsb332_extraction(region=region, i=i, j=j)

            if (chr(num) == '$'):
                if (pixel_count == 0):
                    pixel_count = int(data)
                    data = ""
                else:
                    flag = True
                    break
            elif (chr(num) == ','):
                selected_frames.append(int(data))
                data = ""
            else:
                data += chr(num)

        if (flag):
            break

    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    no_of_blocks = 1

    no_of_frames = math.ceil(pixel_count / (min(width, height) * no_of_blocks))

    while no_of_frames > total_frames:
        no_of_blocks += 1
        no_of_frames = math.ceil(pixel_count / (math.ceil(math.sqrt(min(width, height)))
                                 * math.ceil(math.sqrt(min(width, height))) * no_of_blocks))

    block_size = math.ceil(math.sqrt(min(width, height)))

    selected_frames.sort()
    print(selected_frames)

    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # selected_regions = {}

    # for i in range(1, 300):
    #     selected_regions[i] = [{'start': (0, 0), 'end': (200, 200)}]

    selected_regions = rs.PCA_Implementation(
        cap=cap, block_size=block_size, frame_list=selected_frames, no_of_blocks=no_of_blocks)

    # selected_regions = rs.GWO(cap=cap, msg_size=math.ceil(math.sqrt(pixel_count)),
    #                         frame_list=selected_frames, no_of_blocks=no_of_blocks)

    cap.set(cv2.CAP_PROP_POS_FRAMES, 1)  # Skipping first frame

    data = ""
    flag = False
    frame_no = 0
    total_len = 0
    extracted_len = -1
    height = -1
    width = -1
    total_frames = -1
    key = None
    iv = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_no = frame_no + 1

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
                            if (type == 1):
                                text_bytes = decrypt_text(
                                    bytes.fromhex(data), iv, key)

                                file = open(
                                    "assets/extracted_files/texts/output.txt", "w")

                                file.write(text_bytes)

                                print(
                                    "Output file at assets/extracted_files/texts/output.txt successfully created")
                                flag = True
                                break
                            elif (type == 2):
                                image_bytes = decrypt_image_data(
                                    ciphertext=bytes.fromhex(data), key=key, iv=iv)

                                image = Image.open(io.BytesIO(image_bytes))

                                image.save(
                                    'assets/extracted_files/images/output.jpg')

                                print(
                                    "Output file at assets/extracted_files/images/output.jpg successfully created")
                                flag = True
                                break
                            elif (type == 3):
                                pass
                    if (flag):
                        break

                if (flag):
                    break

            if (flag):
                break

    cap.release()
    cv2.destroyAllWindows()


def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def main():
    print("\nVideo Steganography")

    flag = False
    while not flag:
        print("1. akiyo\n2. bowing\n3. bus\n4. city\n5. crew\n")
        opt = int(input("Select stego video: "))
        if (opt > 0 and opt < 6):
            flag = True

    filename = option(opt)
    cap = cv2.VideoCapture(f'assets/stego_videos/{filename}_stego.avi')
    flag = True

    while (flag):
        print("\n1. Text\n2. Image\n3. Video\n")
        file_type = int(input("Select secret file type: "))

        match (file_type):
            case 1:
                create_folder("assets/extracted_files/texts")
            case 2:
                create_folder("assets/extracted_files/images")
            case 3:
                create_folder("assets/extracted_files/videos")

        flag = False

        if file_type in [1, 2, 3]:
            extract_data(cap=cap, type=file_type)
        else:
            print("Invalid option!")
            flag = True


if __name__ == '__main__':
    main()
