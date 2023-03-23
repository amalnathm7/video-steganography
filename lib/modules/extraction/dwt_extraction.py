import pywt
import cv2

# Read stego video file
video_path = "assets/stego_videos/akiyo_stego.avi"
cap = cv2.VideoCapture(video_path)
f = open('assets/file.txt', 'r')

# Define DWT parameters
wavelet = 'haar'
level = 1

# Initialize message variable
binary_message = ""

# Extract binary message from video frames
binary_message_index = 0
binary_message_len = 200
while True:
    # Read frame from video
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to YCbCr color space
    ycrcb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)

    # Apply 2D DWT to Y channel
    y_channel = ycrcb_frame[:, :, 0]
    coeffs = pywt.dwt2(y_channel, wavelet, 'per')
    cA, (cH, cV, cD) = coeffs

    # Extract binary message from LL subband
    rows, cols = cA.shape
    for i in range(rows):
        for j in range(cols):
            if binary_message_index < binary_message_len:
                # Extract bit from LL pixel value
                bit = int(cA[i][j] % 2)
                # Add bit to message string
                binary_message += str(bit)
                binary_message_index += 1
            else:
                break

# Release stego video file
cap.release()

# Convert binary message to text
print(binary_message)
text_message = "".join([chr(int(binary_message[i:i+8], 2))
                       for i in range(0, len(binary_message), 8)])

# Print extracted text message
print("Extracted message:", text_message)
