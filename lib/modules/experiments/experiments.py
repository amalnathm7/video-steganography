import cv2
import numpy as np
from sewar.full_ref import psnr, ssim
from scipy.stats import pearsonr
import csv


def option(opt):
    match opt:
        case 1: return "akiyo"
        case 2: return "bowing"
        case 3: return "bus"
        case 4: return "carphone"
        case 5: return "city"
        case 6: return "crew"
        case 7: return "deadline"
        case 8: return "football"
        case 9: return "salesman"
        case 10: return "suzie"


def calculate_ncc(original_signal, received_signal):
    ncc, _ = pearsonr(original_signal.flatten(), received_signal.flatten())
    return ncc


def calculate_ber(original_signal, received_signal):
    original_binary = np.where(original_signal.flatten() >= 128, 1, 0)
    received_binary = np.where(received_signal.flatten() >= 128, 1, 0)
    num_errors = np.sum(original_binary != received_binary)
    ber = num_errors / len(original_binary)
    return ber


def experiments():
    flag = True
    total_psnr = 0
    total_ssim = 0
    total_ncc = 0
    total_ber = 0
    count = 0
    index = 0

    print("\nVideo Steganography\n")

    while flag:
        print("\n1. akiyo\n2. bowing\n3. bus\n4. carphone\n5. city\n6. crew\n7. deadline\n8. football\n9. salesman\n10. suzie\n")
        opt = int(input("Select video: "))
        if 1 <= opt <= 10:
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
            ssim_val = ssim(frame, frame1)[0]
            ncc_val = calculate_ncc(frame, frame1)
            ber_val = calculate_ber(frame, frame1)

            total_psnr += psnr_val
            total_ssim += ssim_val
            total_ncc += ncc_val
            total_ber += ber_val

            # print(f'Frame {index}')
            # print(psnr_val)
            # print(ssim_val)
            # print(ncc_val)
            # print(ber_val)
            # print("\n")

            count += 1
        
        index += 1

    average_psnr = total_psnr / count
    average_ssim = total_ssim / count
    average_ncc = total_ncc / count
    average_ber = total_ber / count

    with open("output.csv", "a") as file:
        writter = csv.writer(file)
        writter.writerow([average_psnr, average_ssim, average_ncc, average_ber])
    
    # print("Average PSNR:", average_psnr)
    # print("Average SSIM:", average_ssim)
    # print("Average NCC:", average_ncc)
    # print("Average BER:", average_ber)

    cap.release()
    cap1.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    experiments()
