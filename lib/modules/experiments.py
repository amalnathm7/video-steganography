import cv2
from sewar import psnr, ssim


def option(opt):
    match opt:
        case 1: return "akiyo"
        case 2: return "bowing"
        case 3: return "bus"
        case 4: return "city"
        case 5: return "crew"


def main():
    flag = True
    while flag:
        print("1. akiyo\n2. bowing\n3. bus\n4. city\n5. crew\n")
        opt = int(input("Select video: "))
        if (opt > 0 and opt < 6):
            flag = False
        else:
            print("Invalid option!\n")

    filename = option(opt)
    cap = cv2.VideoCapture(f'assets/cover_videos/{filename}_cif.y4m')
    cap1 = cv2.VideoCapture(f'assets/stego_videos/{filename}_stego.avi')

    while True:
        ret, frame = cap.read()
        ret1, frame1 = cap1.read()

        if not ret:
            break

        print("PSNR: " + str(psnr(frame, frame1)))

        print("SSIM: " + str(ssim(frame, frame1)[0]))

    cap.release()
    cap1.release()
    cv2.destroyAllWindows()


if (__name__ == '__main__'):
    main()
