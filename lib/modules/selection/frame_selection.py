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


def histogram_difference(cap, frame_count):
    key_frames = []
    hist_list = []
    prev_hist = None

    cap.set(cv2.CAP_PROP_POS_FRAMES, 1)  # Skipping the first frame

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
            hist_list.append(-1)
            prev_hist = hist
            continue

        hist_list.append(cv2.compareHist(
            prev_hist, hist, cv2.HISTCMP_CHISQR_ALT))
        prev_hist = hist

    key_frames = get_k_largest(hist_list, frame_count)
    key_frames = [x + 1 for x in key_frames]

    return key_frames


def ssim_based_frame_selection(cap, frame_count):
    cap.set(cv2.CAP_PROP_POS_FRAMES, 1)  # Skipping the first frame

    ssim_list = []
    index = 1
    ret1, frame1 = cap.read()
    ssim_list.append(-1)
    
    if ret1:
        while True:
            ret2, frame2 = cap.read()

            if not ret2:
                break

            ssim_val1 = ssim(frame1, frame2)[0]
            ssim_list.append(ssim_val1)

            print(f"SSIM({index}, {index + 1}): {ssim_val1}")

            index = index + 1
            frame1 = frame2

    key_frames = get_k_largest(ssim_list, frame_count)
    key_frames = [x + 1 for x in key_frames]

    return key_frames
