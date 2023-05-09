import cv2
import numpy as np
from sewar.full_ref import psnr, ssim
from scipy.stats import pearsonr

def option(opt):
    match opt:
        case 1: return "akiyo"
        case 2: return "bowing"
        case 3: return "bus"
        case 4: return "city"
        case 5: return "crew"

def calculate_ncc(original_signal, received_signal):
    ncc, _ = pearsonr(original_signal, received_signal)
    return ncc

def calculate_ber(original_signal, received_signal):
    original_binary = np.where(original_signal >= 0.5, 1, 0)
    received_binary = np.where(received_signal >= 0.5, 1, 0)
    num_errors = np.sum(original_binary != received_binary)
    ber = num_errors / len(original_binary)
    return ber

def main():
    flag = True
    total_psnr = 0
    total_ssim = 0
    total_ncc = 0
    total_ber = 0
    count = 0
    while flag:
        print("1. akiyo\n2. bowing\n3. bus\n4. city\n5. crew\n")
        opt = int(input("Select video: "))
        if 1 <= opt <= 5:
            flag = False
        else:
            print("Invalid option!\n")

    filename = option(opt)
    cap = cv2.VideoCapture(f'assets/cover_videos/{filename}_cif.y4m')
    cap1 = cv2.VideoCapture(f'assets/stego_videos/{filename}_stego.avi')

    while True:
        ret, frame = cap.read()
        ret1, frame1 = cap1.read()

        if not ret or not ret1:
            break

        psnr_val = psnr(frame, frame1)

        if psnr_val != float("inf"):
            total_psnr += psnr_val
            count += 1

        ssim_val = ssim(frame, frame1)[0]

        if ssim_val != 1:
            total_ssim += ssim_val

        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame1_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

        # Calculate NCC and BER
        ncc_val = calculate_ncc(frame_gray.flatten(), frame1_gray.flatten())
        ber_val = calculate_ber(frame_gray.flatten(), frame1_gray.flatten())

        total_ncc += ncc_val
        total_ber += ber_val

        print(f'Frame {count}')
        print(psnr_val)
        print(ssim_val)
        print(ncc_val)
        print(ber_val)
        print("\n")

    average_psnr = total_psnr / count
    average_ssim = total_ssim / count
    average_ncc = total_ncc / count
    average_ber = total_ber / count

    print("Average PSNR:", average_psnr)
    print("Average SSIM:", average_ssim)
    print("Average NCC:", average_ncc)
    print("Average BER:", average_ber)

    cap.release()
    cap1.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()