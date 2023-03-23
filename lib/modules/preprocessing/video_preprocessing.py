# importing libraries
import cv2
import numpy as np

# Create a VideoCapture object and read from input file
cap = cv2.VideoCapture('assets/cover_videos/akiyo_cif.y4m')

# Check if camera opened successfully
if (cap.isOpened()== False):
	print("Error opening video file")

# Read until video is completed
while(cap.isOpened()):
	
# Capture frame-by-frame
	ret, frame = cap.read()
	if ret == True:
	# Display the resulting frame
		cv2.imshow('Frame', frame)
		
	# Press Q on keyboard to exit
		if cv2.waitKey(25) & 0xFF == ord('q'):
			break

# Break the loop
	else:
		break

# When everything done, release
# the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()








































# import cv2

# # read video from file
# cap = cv2.VideoCapture('assets/cover_videos/akiyo_cif.y4m')
# video_fps = cap.get(cv2.CAP_PROP_FPS),
# total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
# height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
# width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

# print(f"Frame Per second: {video_fps } \nTotal Frames: {total_frames} \nHeight: {height} \nWidth: {width}")

# while True:
#     ret, frame = cap.read()
#     if not ret: break # break if no next frame
    
#     cv2.imshow('', frame) # show frame
    
#     if cv2.waitKey(1) & 0xFF == ord('q'): # on press of q break
#         break
        
# # release and destroy windows
# cap.release()
# cv2.destroyAllWindows()