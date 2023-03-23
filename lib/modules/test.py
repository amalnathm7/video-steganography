import cv2

cap = cv2.VideoCapture('assets/secret_files/videos/input.y4m')
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
video_fps = int(cap.get(cv2.CAP_PROP_FPS))
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter('assets/secret_files/videos/input1.mp4', fourcc, video_fps, (width, height))

for i in range(5):
    ret, frame = cap.read()
    if not ret:
        break

    video_writer.write(frame)
