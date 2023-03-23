import cv2
import math
import os
from PIL import Image


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
    data = str(len(data)) + "$" + data

    binary_data = [format(ord(char), '08b') for char in data]

    return binary_data


def image_to_binary(file_path):
    img = Image.open(file_path)

    rgb_im = img.convert('RGB')

    width, height = img.size

    data = "{}${}$".format(width, height)
    binary_data = [format(ord(char), '08b') for char in data]

    for x in range(height):
        for y in range(width):
            r, g, b = rgb_im.getpixel((y, x))

            binary_data.append(int_to_binary(r))
            binary_data.append(int_to_binary(g))
            binary_data.append(int_to_binary(b))

    return binary_data


def video_to_binary(file_path):
    cap = cv2.VideoCapture(file_path)

    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    data = "{}${}${}${}$".format(width, height, video_fps, total_frames)
    binary_data = [format(ord(char), '08b') for char in data]

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        for x in range(height):
            for y in range(width):
                r, g, b = rgb_frame[x][y]

                binary_data.append(int_to_binary(r))
                binary_data.append(int_to_binary(g))
                binary_data.append(int_to_binary(b))

    return binary_data


def lsb332_embedding(cap, writer, binary_data):
    robust_regions = {}

    for i in range(300):
        robust_regions[i] = [{
            'start': (0, 0),
            'end': (287, 351),
        }]

    frame_no = 0
    count = 0
    flag = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if flag:
            writer.write(frame)
            continue

        frame_no = frame_no + 1

        if frame_no in robust_regions.keys():
            for element in robust_regions[frame_no]:
                region = frame[element['start'][0]:element['end']
                               [0] + 1, element['start'][1]:element['end'][1] + 1]
                region_height = element['end'][0] + 1 - element['start'][0]
                region_width = element['end'][1] + 1 - element['start'][1]

                for i in range(0, region_height):
                    for j in range(0, region_width):
                        binary = binary_data[count]
                        count += 1

                        region[i, j, 0] = math.floor(
                            region[i, j, 0] / 8) * 8 + (int(binary[2]) + int(binary[1]) * 2 + int(binary[0]) * 4)
                        region[i, j, 1] = math.floor(
                            region[i, j, 1] / 8) * 8 + (int(binary[5]) + int(binary[4]) * 2 + int(binary[3]) * 4)
                        region[i, j, 2] = math.floor(
                            region[i, j, 2] / 4) * 4 + (int(binary[7]) + int(binary[6]) * 2)

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
            lsb332_embedding(cap=cap, writer=writer,
                             binary_data=text_to_binary("assets/secret_files/texts/input.txt"))
        elif (file_type == 2):
            lsb332_embedding(cap=cap, writer=writer,
                             binary_data=image_to_binary('assets/secret_files/images/input.jpg'))
        elif (file_type == 3):
            lsb332_embedding(cap=cap, writer=writer, binary_data=video_to_binary(
                'assets/secret_files/videos/input1.mp4'))
        else:
            print("Invalid option!")
            flag = True


if __name__ == '__main__':
    main()
