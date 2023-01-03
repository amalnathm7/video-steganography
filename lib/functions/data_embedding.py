import cv2
import math


def option(opt):
    match opt:
        case 1: return "akiyo"
        case 2: return "bowing"
        case 3: return "bus"
        case 4: return "city"
        case 5: return "crew"


def decimalToBinary(n):
    return bin(n).replace("0b", "").zfill(8)


flag = False
while not flag:
    print("1. akiyo\n2. bowing\n3. bus\n4. city\n5. crew\n")
    opt = int(input("Select cover video: "))
    if (opt > 0 and opt < 6):
        flag = True

# read video from file
filename = option(opt)
cap = cv2.VideoCapture(f'assets/cover_videos/{filename}_cif.y4m')
video_fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

print(
    f"Frame Per second: {video_fps}\nTotal Frames: {total_frames}\nHeight: {height}\nWidth: {width}")

file = open("assets/secret_files/texts/input.txt", "r")
data = file.read()
data = data + "$"

fourcc = cv2.VideoWriter_fourcc(*'HFYU')
writer = cv2.VideoWriter(f'assets/stego_videos/{filename}_stego.avi', apiPreference=0, fourcc=fourcc,
                         fps=video_fps, frameSize=(int(width), int(height)))

flag = True

while True:
    ret, frame = cap.read()
    if not ret:
        break  # break if no next frame

    if (flag):
        for i in range(0, len(data)):
            binary = decimalToBinary(ord(data[i]))

            frame[i, 0, 0] = math.floor(
                frame[i, 0, 0] / 8) * 8 + (int(binary[2]) + int(binary[1]) * 2 + int(binary[0]) * 4)
            frame[i, 0, 1] = math.floor(
                frame[i, 0, 1] / 8) * 8 + (int(binary[5]) + int(binary[4]) * 2 + int(binary[3]) * 4)
            frame[i, 0, 2] = math.floor(
                frame[i, 0, 2] / 4) * 4 + (int(binary[7]) + int(binary[6]) * 2)

    writer.write(frame)  # write frame

    flag = False
    # cv2.imshow('Akiyo Frames', frame)  # show frame

    # if cv2.waitKey(1) & 0xFF == ord('q'):  # on press of q break
    #     break

# release and destroy windows
print("Embedded successfully")
writer.release()
cap.release()
cv2.destroyAllWindows()
