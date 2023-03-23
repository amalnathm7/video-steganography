import cv2
import numpy as np
import cv2
import heapq
from sewar import ssim


def option(opt):
    match opt:
        case 1: return "akiyo"
        case 2: return "bowing"
        case 3: return "bus"
        case 4: return "city"
        case 5: return "crew"

# METHOD 3: Histogram difference


def get_k_smallest(test_list, k):
    return sorted(range(len(test_list)), key=lambda sub: test_list[sub])[:k]


def get_k_largest(test_list, k):
    return sorted(range(len(test_list)), key=lambda sub: test_list[sub])[-k:]


cap = cv2.VideoCapture('assets/cover_videos/bus_cif.y4m')

key_frames = []
hist_list = []
prev_hist = None
frame_count = 0

while True:
    ret, frame = cap.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    hist = cv2.normalize(hist, hist).flatten()

    # hist = cv2.calcHist([frame], [0, 1, 2], None, [256, 256, 256], [0, 256, 0, 256, 0, 256])
    # hist = cv2.normalize(hist, hist).flatten()

    if prev_hist is None:
        prev_hist = hist
        continue

    hist_list.append(cv2.compareHist(prev_hist, hist, cv2.HISTCMP_CHISQR))
    prev_hist = hist
    frame_count += 1

count = int(input("Enter number of frames: "))

key_frames = get_k_smallest(hist_list, count)

for frame_num in key_frames:
    print(frame_num)

cap.release()
cap = cv2.VideoCapture('assets/cover_videos/bus_cif.y4m')
count = 0
while True:
    ret, frame = cap.read()

    if not ret:
        break

    if count in key_frames:
        cv2.imshow('Akiyo', frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    count += 1

cap.release()
cv2.destroyAllWindows()

# METHOD 2: Fibonacci with a key
# nterms = int(input("No. of frames required:  "))
# key = int(input("Enter the key: "))
# n1, n2 = 0, 1
# count = 0
# key_frames = []
# print("1. akiyo\n2. bowing\n3. bus\n4. city\n5. crew\n")
# opt = int(input("Select cover video: "))
# if (opt > 0 and opt < 6):
#    # read video from file
#     filename = option(opt)
#     cap = cv2.VideoCapture(f'assets/cover_videos/{filename}_cif.y4m')
#     total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
# if nterms <= 0:
#     print("Please enter a positive integer")
# else:
#     print("Fibonacci sequence:")
#     while count < nterms:
#         # print(n1)
#         key_frames.append(n1)
#         nth = ((n1 + n2) + key) % total_frames
#         n1 = n2
#         n2 = nth
#         count += 1


# METHOD 1: SSIM Merthod
# def get_frame_numbers_of_smallest_k(ssim_list, opt1):
#     return [i for i, x in heapq.nsmallest(opt1, enumerate(ssim_list
#                                                           ), key=lambda x:x[1])]


# ssim_list = []
# print("1. akiyo\n2. bowing\n3. bus\n4. city\n5. crew\n")
# opt = int(input("Select cover video: "))
# if (opt > 0 and opt < 6):
#     # read video from file
#     filename = option(opt)
#     cap = cv2.VideoCapture(f'assets/cover_videos/{filename}_cif.y4m')
#     total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

# opt1 = int(input("Number of frames to be sent: "))
# print(
#     f"Total Frames: {total_frames}\n")

# index = 0
# ret1, frame1 = cap.read()
# if ret1:
#     while True:
#         ret2, frame2 = cap.read()
#         if not ret2:
#             break  # break if no next frame
#         ssim_val1, cs_val1 = ssim(frame1, frame2)
#         ssim_list.append(ssim_val1)
#         print(f"SSIM({index}, {index + 1}): {ssim(frame1, frame2)[0]}")
#         index = index + 1
#         frame1 = frame2

#         # cv2.imshow('Akiyo Frames', frame)  # show frame

#         # if cv2.waitKey(1) & 0xFF == ord('q'):  # on press of q break
#         #     break

# key_frames = get_frame_numbers_of_smallest_k(ssim_list, opt1)
print(key_frames)
cap.release()
cv2.destroyAllWindows()