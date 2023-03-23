import cv2
import math
from PIL import Image
import numpy as np
import decryption.textdec as dec


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


def lsb332_extraction(cap, type):
    robust_regions = {}

    for i in range(300):
        robust_regions[i] = [{
            'start': (0, 0),
            'end': (287, 351),
        }]

    len = 0
    extracted_len = -1
    frame_no = 0
    data = ""
    flag = False
    height = -1
    width = -1
    total_frames = -1
    fps = -1
    frame_index = 0
    pixels = []
    index = 0
    rgb = ()
    key = b""
    iv = b""
    encrypted_text = b""
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(
        'assets/extracted_files/videos/output.mp4', fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_no = frame_no + 1

        if frame_no in robust_regions.keys():
            for element in robust_regions[frame_no]:
                region = frame[element['start'][0]:element['end']
                               [0] + 1, element['start'][1]:element['end'][1] + 1]
                region_height = element['end'][0] + 1 - element['start'][0]
                region_width = element['end'][1] + 1 - element['start'][1]

                for i in range(0, region_height):
                    for j in range(0, region_width):
                        a = region[i, j, 0] - \
                            (math.floor(region[i, j, 0] / 8) * 8)
                        b = region[i, j, 1] - \
                            (math.floor(region[i, j, 1] / 8) * 8)
                        c = region[i, j, 2] - \
                            (math.floor(region[i, j, 2] / 4) * 4)

                        num = binary_to_decimal(decimal_to_binary(a, 3) +
                                                decimal_to_binary(b, 3) + decimal_to_binary(c, 2))
                        ch = chr(num)

                        if (type == 1):
                            if (extracted_len == -1 and ch == '$'):
                                if (key == b""):
                                    key = bytes.fromhex(data)
                                    data = ""
                                elif (iv == b""):
                                    key = bytes.fromhex(data)
                                    data = ""
                                else:
                                    len = int(data)
                                    data = ""
                                    extracted_len = 0
                            elif extracted_len < len:
                                if (extracted_len != -1):
                                    extracted_len += 1
                                data += ch
                            else:
                                decrypted_data = dec.decrypt_text(data, iv, key)

                                file = open(
                                    "assets/extracted_files/texts/output.txt", "w")
                                
                                file.write(decrypted_data)

                                print(
                                    "Output file at assets/extracted_files/texts/output.txt successfully created")
                                flag = True
                                break
                        elif (type == 2):
                            if (extracted_len == -1 and ch == '$'):
                                if (width == -1):
                                    width = int(data)
                                    data = ""
                                elif (height == -1):
                                    height = int(data)
                                    len = height * width * 3
                                    extracted_len = 0
                            elif extracted_len < len:
                                if (extracted_len == -1):
                                    data += ch
                                else:
                                    index = (index + 1) % 3

                                    if (index == 0):
                                        rgb += (num,)
                                        pixels.append(rgb)
                                        rgb = ()
                                    else:
                                        rgb += (num,)

                                    extracted_len += 1
                            else:
                                img = Image.new(
                                    'RGB', (width, height), color=0)
                                img.putdata(pixels)
                                img.save(
                                    'assets/extracted_files/images/output.jpg')
                                print(
                                    "Output file at assets/extracted_files/images/output.jpg successfully created")
                                flag = True
                                break
                        elif (type == 3):
                            if (extracted_len == -1 and ch == '$'):
                                if (width == -1):
                                    width = int(data)
                                    data = ""
                                elif (height == -1):
                                    height = int(data)
                                    data = ""
                                elif (fps == -1):
                                    fps = int(data)
                                    data = ""
                                elif (total_frames == -1):
                                    total_frames = int(data)
                                    len = height * width * 3
                                    extracted_len = 0
                            elif extracted_len < len:
                                if (extracted_len == -1):
                                    data += ch
                                else:
                                    index = (index + 1) % 3

                                    if (index == 0):
                                        rgb += (num,)
                                        pixels.append(rgb)
                                        rgb = ()
                                    else:
                                        rgb += (num,)

                                    extracted_len += 1
                            else:
                                img = Image.new(
                                    'RGB', (width, height), color=0)

                                img.putdata(pixels)

                                video_writer.write(np.array(img))

                                print(frame_index)
                                frame_index += 1

                                if (frame_index == total_frames):
                                    print(
                                        "Output file at assets/extracted_files/videos/output.mp4 successfully created")
                                    flag = True
                                    break
                                else:
                                    extracted_len = 0
                                    pixels.clear()
                    if (flag):
                        break

                if (flag):
                    break

            if (flag):
                break

    video_writer.release()
    cap.release()
    cv2.destroyAllWindows()


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

        flag = False

        if file_type in [1, 2, 3]:
            lsb332_extraction(cap=cap, type=file_type)
        else:
            print("Invalid option!")
            flag = True


if __name__ == '__main__':
    main()