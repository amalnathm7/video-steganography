import cv2
import numpy as np
from sewar.full_ref import psnr, ssim
from scipy.stats import pearsonr
import csv
import cv2
from matplotlib import pyplot as plt\


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


def pdh_analysis(stego_frame, cover_frame):
    stego_gray = cv2.cvtColor(stego_frame, cv2.COLOR_BGR2GRAY).astype(np.int16)
    stego_diff = np.diff(stego_gray.ravel())
    stego_unique_diffs, stego_counts = np.unique(stego_diff, return_counts=True)


    cover_gray = cv2.cvtColor(cover_frame, cv2.COLOR_BGR2GRAY).astype(np.int16)
    cover_diff = np.diff(cover_gray.ravel())
    cover_unique_diffs, cover_counts = np.unique(cover_diff, return_counts=True)

    font = {'family': 'Times New Roman', 'size': 12}
    plt.rc('font', **font)
    plt.figure()
    plt.xlabel('Pixel Difference')
    plt.ylabel('Frequency')
    plt.plot(stego_unique_diffs, stego_counts, label='Stego Frame')
    plt.plot(cover_unique_diffs, cover_counts, label='Cover Frame')
    plt.legend()
    plt.xlim(-40, 40)
    plt.ylim(bottom=0)
    plt.show()


def histogram_analysis(cover_frame, stego_frame):
    cover_gray = cv2.cvtColor(cover_frame, cv2.COLOR_BGR2GRAY)
    stego_gray = cv2.cvtColor(stego_frame, cv2.COLOR_BGR2GRAY)

    cover_hist = cv2.calcHist([cover_gray], [0], None, [256], [0, 256])
    stego_hist = cv2.calcHist([stego_gray], [0], None, [256], [0, 256])
    
    font = {'family': 'Times New Roman', 'size': 12}
    plt.rc('font', **font)
    plt.figure()
    plt.xlabel('Pixel Value')
    plt.ylabel('Frequency')
    plt.plot(stego_hist, label='Stego Frame')
    plt.plot(cover_hist, label='Cover Frame')
    plt.legend()
    plt.xlim([0, 256])
    plt.ylim(bottom=0)
    plt.show()


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
        print("1. akiyo\n2. bowing\n3. bus\n4. carphone\n5. city\n6. crew\n7. deadline\n8. football\n9. salesman\n10. suzie\n")
        opt = int(input("Select video: "))
        if (1 <= opt <= 10):
            flag = False
        else:
            print("\nInvalid option!\n")

    filename = option(opt)
    cover_cap = cv2.VideoCapture(f'assets/cover_videos/{filename}_cif.y4m')
    stego_cap = cv2.VideoCapture(f'assets/stego_videos/{filename}_stego.avi')

    print()
    while True:
        cover_ret, cover_frame = cover_cap.read()
        stego_ret, stego_frame = stego_cap.read()

        if not cover_ret or not stego_ret:
            break

        psnr_val = psnr(cover_frame, stego_frame)

        if psnr_val != float("inf"):
            ssim_val = ssim(cover_frame, stego_frame)[0]
            ncc_val = calculate_ncc(cover_frame, stego_frame)
            ber_val = calculate_ber(cover_frame, stego_frame)

            total_psnr += psnr_val
            total_ssim += ssim_val
            total_ncc += ncc_val
            total_ber += ber_val

            print(f'Processing frame {index}')

            count += 1
        
        index += 1

    average_psnr = total_psnr / count
    average_ssim = total_ssim / count
    average_ncc = total_ncc / count
    average_ber = total_ber / count

    with open("output.csv", "a") as file:
        writter = csv.writer(file)
        writter.writerow([average_psnr, average_ssim, average_ncc, average_ber])
    
    print("\nAverage PSNR:", average_psnr)
    print("Average SSIM:", average_ssim)
    print("Average NCC:", average_ncc)
    print("Average BER:", average_ber)

    cover_cap.set(cv2.CAP_PROP_POS_FRAMES, 1)
    stego_cap.set(cv2.CAP_PROP_POS_FRAMES, 1)

    _, cover_frame = cover_cap.read()
    _, stego_frame = stego_cap.read()

    cv2.imshow('Cover Frame', cover_frame)
    cv2.waitKey(0)
    cv2.imshow('Stego Frame', stego_frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    pdh_analysis(stego_frame, cover_frame)
    histogram_analysis(stego_frame, cover_frame)

    print("\nExperiments completed.\n")

    cover_cap.release()
    stego_cap.release()

if __name__ == '__main__':
    experiments()