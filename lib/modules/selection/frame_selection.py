import cv2
from sewar import ssim


def option(opt):
    match opt:
        case 1: return "akiyo"
        case 2: return "bowing"
        case 3: return "bus"
        case 4: return "city"
        case 5: return "crew"


def get_k_smallest(test_list, k):
    return sorted(range(len(test_list)), key=lambda sub: test_list[sub])[:k]


def get_k_largest(test_list, k):
    return sorted(range(len(test_list)), key=lambda sub: test_list[sub])[-k:]


def histogram_difference_frame_selection(cap, frame_count, init_frames):
    key_frames = []
    hist_list = []
    prev_hist = None
    index = 0

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
            hist_list.append(0)
            prev_hist = hist
            index += 1
            continue

        if (index in init_frames):
            hist_list.append(-1)
        else:
            hist_list.append(cv2.compareHist(prev_hist, hist, cv2.HISTCMP_CHISQR_ALT))
        
        prev_hist = hist

        index += 1

    key_frames = get_k_largest(hist_list, frame_count)
    key_frames = [x for x in key_frames]

    return key_frames


def ssim_frame_selection(cap, frame_count, init_frames):
    ssim_list = []
    index = 1
    ret1, frame1 = cap.read()
    ssim_list.append(0)

    if(0 in init_frames):
        print(f"Init frame 0")
    
    if ret1:
        while True:
            ret2, frame2 = cap.read()

            if not ret2:
                break

            if (index in init_frames):
                ssim_list.append(-1)
                print(f"Init frame {index}")
            else:
                ssim_val1 = ssim(frame1, frame2)[0]
                ssim_list.append(ssim_val1)
                print(f"SSIM({index}): {ssim_val1}")

            index += 1
            frame1 = frame2

    key_frames = get_k_largest(ssim_list, frame_count)
    key_frames = [x for x in key_frames]

    return key_frames