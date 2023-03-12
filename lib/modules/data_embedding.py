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


def text_to_binary():
    file = open("assets/secret_files/texts/input.txt", "r")
    data = file.read()
    data = str(len(data)) + "$" + data

    binary_data = ''.join(format(ord(char), '08b') for char in data)

    return binary_data


def image_to_binary():
    # Load the image file
    img = Image.open('assets/secret_files/images/input.jpg')

    # Get the RGB values for each pixel in the image
    rgb_im = img.convert('RGB')

    width, height = img.size

    data = "{}${}$".format(width, height)
    binary_data = ''.join(format(ord(char), '08b') for char in data)

    for x in range(height):
        for y in range(width):
            r, g, b = rgb_im.getpixel((y, x))

            binary_data += int_to_binary(r)
            binary_data += int_to_binary(g)
            binary_data += int_to_binary(b)
    
    return binary_data


def video_to_binary():
    print("")


def lsb332_embedding(cap, writer, binary_data):
    robust_regions = {
        1: [
            {
                'start': (0, 0),
                'end': (200, 200),
            },
        ],

        2: [
            {
                'start': (0, 0),
                'end': (200, 200),
            },
        ],

        3: [
            {
                'start': (0, 0),
                'end': (200, 200),
            },
        ],

        4: [
            {
                'start': (0, 0),
                'end': (200, 200),
            },
        ],

        5: [
            {
                'start': (0, 0),
                'end': (200, 200),
            },
        ],

        6: [
            {
                'start': (0, 0),
                'end': (200, 200),
            },
        ],

        7: [
            {
                'start': (0, 0),
                'end': (200, 200),
            },
        ],

        8: [
            {
                'start': (0, 0),
                'end': (200, 200),
            },
        ],

        9: [
            {
                'start': (0, 0),
                'end': (200, 200),
            },
        ],

        10: [
            {
                'start': (0, 0),
                'end': (200, 200),
            },
        ],

        11: [
            {
                'start': (0, 0),
                'end': (200, 200),
            },
        ],

        12: [
            {
                'start': (0, 0),
                'end': (200, 200),
            },
        ],
    }

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
                        binary = binary_data[count:count+8]

                        region[i, j, 0] = math.floor(
                            region[i, j, 0] / 8) * 8 + (int(binary[2]) + int(binary[1]) * 2 + int(binary[0]) * 4)
                        region[i, j, 1] = math.floor(
                            region[i, j, 1] / 8) * 8 + (int(binary[5]) + int(binary[4]) * 2 + int(binary[3]) * 4)
                        region[i, j, 2] = math.floor(
                            region[i, j, 2] / 4) * 4 + (int(binary[7]) + int(binary[6]) * 2)

                        count = count+8

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
                             binary_data=text_to_binary())
        elif (file_type == 2):
            lsb332_embedding(cap=cap, writer=writer,
                             binary_data=image_to_binary())
        elif (file_type == 3):
            lsb332_embedding(cap=cap, writer=writer,
                             binary_data=video_to_binary())
        else:
            print("Invalid option!")
            flag = True


if __name__ == '__main__':
    main()
