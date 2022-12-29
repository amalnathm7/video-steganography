import cv2
import math


def decimalToBinary(n):
    return bin(n).replace("0b", "").zfill(8)


# read video from file
cap = cv2.VideoCapture('assets/cover_videos/akiyo_cif.y4m')
video_fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

print(
    f"Frame Per second: {video_fps}\nTotal Frames: {total_frames}\nHeight: {height}\nWidth: {width}")

data = input("Enter secret data: ")
data = data + "$"

fourcc = cv2.VideoWriter_fourcc(*'HFYU')
writer = cv2.VideoWriter('assets/akiyo_stego.avi', apiPreference=0, fourcc=fourcc,
                         fps=video_fps, frameSize=(int(width), int(height)))

while True:
    ret, frame = cap.read()
    if not ret:
        break  # break if no next frame

    for i in range(0, len(data)):
        binary = decimalToBinary(ord(data[i]))

        frame[i, 0, 0] = math.floor(
            frame[i, 0, 0] / 8) * 8 + (int(binary[2]) + int(binary[1]) * 2 + int(binary[0]) * 4)
        frame[i, 0, 1] = math.floor(
            frame[i, 0, 1] / 8) * 8 + (int(binary[5]) + int(binary[4]) * 2 + int(binary[3]) * 4)
        frame[i, 0, 2] = math.floor(
            frame[i, 0, 2] / 4) * 4 + (int(binary[7]) + int(binary[6]) * 2)

    writer.write(frame)  # write frame

    cv2.imshow('Akiyo Frames', frame)  # show frame

    if cv2.waitKey(1) & 0xFF == ord('q'):  # on press of q break
        break

# release and destroy windows
print("Embedded successfully")
writer.release()
cap.release()
cv2.destroyAllWindows()
