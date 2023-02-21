import cv2
import math
import os


def option(opt):
    match opt:
        case 1: return "akiyo"
        case 2: return "bowing"
        case 3: return "bus"
        case 4: return "city"
        case 5: return "crew"


def decimalToBinary(n):
    return bin(n).replace("0b", "").zfill(8)


def text_embedding():
    file = open("assets/secret_files/texts/input.txt", "r")
    data = file.read()
    data = data + "$"

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
    fourcc = cv2.VideoWriter_fourcc(*'HFYU')
    writer = cv2.VideoWriter(f'assets/stego_videos/{filename}_stego.avi', apiPreference=0, fourcc=fourcc,
                             fps=video_fps, frameSize=(int(width), int(height)))

    frame_no = 0
    selected_frames = [77, 84, 85, 86, 87, 88, 89, 91, 102, 299]

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_no = frame_no + 1

        if frame_no in selected_frames:
            count = 0

            for i in range(0, int(height)):
                flag = False

                for j in range(0, int(width)):
                    binary = decimalToBinary(ord(data[count]))

                    frame[i, j, 0] = math.floor(
                        frame[i, j, 0] / 8) * 8 + (int(binary[2]) + int(binary[1]) * 2 + int(binary[0]) * 4)
                    frame[i, j, 1] = math.floor(
                        frame[i, j, 1] / 8) * 8 + (int(binary[5]) + int(binary[4]) * 2 + int(binary[3]) * 4)
                    frame[i, j, 2] = math.floor(
                        frame[i, j, 2] / 4) * 4 + (int(binary[7]) + int(binary[6]) * 2)

                    count = count+1

                    if (count == len(data)):
                        flag = True
                        break

                if (flag):
                    break

        writer.write(frame)

    print("\nEmbedded successfully")
    writer.release()
    cap.release()


def image_embedding():
    print("")


def video_embedding():
    print("")


def main():
    print("\nVideo Steganography")
    flag = True

    while (flag):
        print("\n1. Text\n2. Image\n3. Video\n")
        file_type = int(input("Select secret file type: "))

        flag = False

        if (file_type == 1):
            text_embedding()
        elif (file_type == 2):
            image_embedding()
        elif (file_type == 3):
            video_embedding()
        else:
            print("Invalid option!")
            flag = True


if __name__ == '__main__':
    main()
