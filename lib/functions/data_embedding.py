import cv2

# read video from file
cap = cv2.VideoCapture('assets/cover_videos/akiyo_cif.y4m')
video_fps = cap.get(cv2.CAP_PROP_FPS),
total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

print(f"Frame Per second: {video_fps } \nTotal Frames: {total_frames} \nHeight: {height} \nWidth: {width}")

while True:
    ret, frame = cap.read()
    if not ret: break # break if no next frame
    
    cv2.imshow('', frame) # show frame
    
    if cv2.waitKey(1) & 0xFF == ord('q'): # on press of q break
        break
    
# release and destroy windows
cap.release()
cv2.destroyAllWindows()