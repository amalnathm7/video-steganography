import pywt
import cv2

def dwt_embedding():
    video_path = "assets/cover_videos/akiyo_cif.y4m"
    cap = cv2.VideoCapture(video_path)

    wavelet = 'haar'

    message = "This is a secret message."

    binary_message = ''.join(format(ord(char), '08b') for char in message)
    print(binary_message)

    output_path = "assets/stego_videos/akiyo_stego.avi"
    fourcc = cv2.VideoWriter_fourcc(*'HFYU')
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    out = cv2.VideoWriter(output_path, fourcc, fps, frame_size)

    binary_message_index = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        ycrcb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)

        y_channel = ycrcb_frame[:,:,0]
        coeffs = pywt.dwt2(y_channel, wavelet)
        cA, (cH, cV, cD) = coeffs

        rows, cols = cA.shape
        for i in range(rows):
            for j in range(cols):
                if binary_message_index < len(binary_message):

                    bit = int(binary_message[binary_message_index])
                    
                    if(int(cA[i][j] % 2) != bit):
                        if bit == 1:
                            cA[i][j] = cA[i][j] + 1
                        else:
                            cA[i][j] = cA[i][j] - 1
                    binary_message_index += 1
                else:
                    break

        ycrcb_frame[:,:,0] = pywt.idwt2((cA, (cH, cV, cD)), wavelet, 'per')

        frame = cv2.cvtColor(ycrcb_frame, cv2.COLOR_YCrCb2BGR)

        out.write(frame)

    cap.release()
    out.release()
