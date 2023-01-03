import cv2
import math


def option(opt):
    match opt:
        case 1: return "akiyo"
        case 2: return "bowing"
        case 3: return "bus"
        case 4: return "city"
        case 5: return "crew"


def decimalToBinary(n, fill):
    return bin(n).replace("0b", "").zfill(fill)


def binaryToDecimal(n):
    return int(n, 2)


flag = False
while not flag:
    print("1. akiyo\n2. bowing\n3. bus\n4. city\n5. crew\n")
    opt = int(input("Select stego video: "))
    if (opt > 0 and opt < 6):
        flag = True

# read video from file
filename = option(opt)
cap = cv2.VideoCapture(f'assets/stego_videos/{filename}_stego.avi')
video_fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

while True:
    ret, frame = cap.read()
    if not ret:
        break  # break if no next frame

    data = ""
    for x in range(0, int(width)):
        flag = False

        for y in range(0, int(height)):
            a = frame[y, x, 0] - (math.floor(frame[y, x, 0] / 8) * 8)
            b = frame[y, x, 1] - (math.floor(frame[y, x, 1] / 8) * 8)
            c = frame[y, x, 2] - (math.floor(frame[y, x, 2] / 4) * 4)

            ch = chr(binaryToDecimal(decimalToBinary(a, 3) +
                     decimalToBinary(b, 3) + decimalToBinary(c, 2)))

            if (ch == '$'):
                file = open("assets/extracted_files/texts/output.txt", "w")
                print(
                    "Output file at assets/extracted_files/texts/output.txt successfully created")
                file.write(data)
                flag = True
                break
            else:
                data += ch

        if (flag):
            break

    if (flag):
        break

# release and destroy windows
cap.release()
cv2.destroyAllWindows()
