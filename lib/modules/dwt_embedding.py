import pywt
import cv2
import numpy as np

# Read video file
video_path = "assets/cover_videos/akiyo_cif.y4m"
cap = cv2.VideoCapture(video_path)

# Define DWT parameters
wavelet = 'haar'
level = 1

# Read text message
message = "This is a secret message."

# Convert message to binary
binary_message = ''.join(format(ord(char), '08b') for char in message)
print(binary_message)

# Create video writer object
output_path = "assets/stego_videos/akiyo_stego.avi"
fourcc = cv2.VideoWriter_fourcc(*'HFYU')
fps = cap.get(cv2.CAP_PROP_FPS)
frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
out = cv2.VideoWriter(output_path, fourcc, fps, frame_size)

# Embed binary message in video frames
binary_message_index = 0
while True:
    # Read frame from video
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to YCbCr color space
    ycrcb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)

    # Apply 2D DWT to Y channel
    y_channel = ycrcb_frame[:,:,0]
    coeffs = pywt.dwt2(y_channel, wavelet)
    cA, (cH, cV, cD) = coeffs

    # Embed binary message in LL subband
    rows, cols = cA.shape
    for i in range(rows):
        for j in range(cols):
            if binary_message_index < len(binary_message):
                # Get current bit from binary message
                bit = int(binary_message[binary_message_index])
                # Modify pixel value in LL subband
                if(int(cA[i][j] % 2) != bit):
                    if bit == 1:
                        cA[i][j] = cA[i][j] + 1
                    else:
                        cA[i][j] = cA[i][j] - 1
                binary_message_index += 1
            else:
                break

    # Apply inverse 2D DWT to Y channel
    ycrcb_frame[:,:,0] = pywt.idwt2((cA, (cH, cV, cD)), wavelet, 'per')

    # Convert frame back to BGR color space
    frame = cv2.cvtColor(ycrcb_frame, cv2.COLOR_YCrCb2BGR)

    # Write modified frame to output video
    out.write(frame)

# Release video file and output video
cap.release()
out.release()
