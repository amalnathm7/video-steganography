import cv2
import pywt
import numpy as np
from sklearn.decomposition import PCA
from PIL import Image
import math
import matplotlib.pyplot as plt


def decimaltoBinary(n):
    return bin(n).replace("0b", "").zfill(8)


def Find_Summation(next_components):
    s = 0
    for i in next_components:
        s = s+(i*i)
    return s


"""def Find_Index_Min(block,value):
    l = []
    mini = 1000000
    ind = -1
    for b in block:
        if(b[pca]< value):
            if(b[pca]< mini):
                mini = b[pca]
                ind = b[index]
    return -1"""


def pca_analysis(y, msg_size, height, width):
    """if multiple blocks to be selected
    blocks=[]
    b = 0
    no_of_blocks = 5"""

    max_pca = 0
    max_row, max_col = 0, 0

    # Dividing the image into blocks and finding the PCA of each block
    for i in range(0, int(height), msg_size):
        for j in range(0, int(width), msg_size):
            r = y[i:i+msg_size, j:j+msg_size]

            # cv2.imshow('t',r)
            # cv2.waitKey(1000)
            """Applying PCA to find the first principal component"""
            pca = PCA(n_components=1, svd_solver='full')
            # print(pca)
            # npdata =  np.asarray(r)
            X = np.array(r)
            pca.fit(X)
            first_component = pca.singular_values_
            first_component_sq = first_component**2

            """ Applying PCA to find the 2 principal components"""
            pca = PCA()
            Y = np.array(r)
            pca.fit(Y)
            next_components = pca.singular_values_
            # print(next_components)
            summation = Find_Summation(next_components)

            """Finding the propotion of the first principal component of the image"""
            if (summation != 0):
                propotion_first_component = first_component_sq/summation
            else:
                propotion_first_component = -1

            """if(len(block) < no_of_blocks):
                block[b]={}
                block[b][pca] = pca.singular_values_
                block[b][row] = i 
                block[b][col] = j
                block[b][index] = b
                b+=1
            else:
                ind = Find_Index_Min(block,pca.singular_values_)
                if(ind != -1):
                    block[ind][pca] = pca.singular_values_
                    block[ind][row] = i
                    block[ind][col] = j
                    block[ind][index] = ind"""

            # print(pca.singular_values_)
            if (propotion_first_component > max_pca):
                max_pca = pca.singular_values_[0]
                print(max_pca)
                max_row = i
                max_col = j

    # print(max_row)
    # print(max_col)

    return (max_row, max_row+msg_size, max_col, max_col+msg_size)
    """return block"""


def main():

    # Capturing the video
    vid = cv2.VideoCapture('assets/cover_videos/akiyo_cif.y4m')

    video_fps = vid.get(cv2.CAP_PROP_FPS)
    total_frames = vid.get(cv2.CAP_PROP_FRAME_COUNT)
    height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)

    print(
        f"Frame per sec: {video_fps}\n Total FRame: {total_frames}\n Height: {height} \nWidth: {width}")

    # reading the first frame of video for simplicity
    ret, frame = vid.read()

    """  NOTE:: Have to go through all the selected frames"""

    # Looping through all the frames in the video
    """while True:
        ret, frame =  vid.read()
        if not ret:
            break

        cv2.imshow('Frame',frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break"""

    # Taking first frame in video
    ret, frame = vid.read()
    if not ret:
        print("The frame does not exist")
    cv2.imshow('Frame', frame)
    cv2.waitKey(1000)

    # Getting data to be embedded
    msg = input("Enter the message to be embedded: ")
    msg_index = 0
    msg_size = len(msg)

    """ NOTE: The data to be embedded can be of different types
            1. text
            2. image
            3. video
            4. audio"""

    if (msg_size > width):
        print("Get another video to embedd")
        exit()

    # Extracting yuv components from the image
    yuv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
    cv2.imshow('YUV', yuv_img)
    cv2.waitKey(1000)

    y, u, v = cv2.split(yuv_img)
    """cv2.imshow('Y',y)
    cv2.waitKey(1000)
    cv2.imshow('U',u)
    cv2.waitKey(1000)
    cv2.imshow('V',v)
    cv2.waitKey(1000)"""

    (max_row, max_row_end, max_col, max_col_end) = pca_analysis(
        y, msg_size, height, width)
    """Selected region printed"""
    img = y[max_row:max_row_end, max_col:max_col_end]
    cv2.imshow('Selected region', img)
    cv2.waitKey(100)

    # print("This prinyinh")

    """Taking the DWT subands of the region selected from the y component"""
    coeffs = pywt.dwt2(img, 'haar')
    LL, (LH, HL, HH) = coeffs
    """fig, ax = plt.subplots(2,2)
    ax[0,0].imshow(LL)
    ax[0,1].imshow(LH)
    ax[1,0].imshow(HL)
    ax[1,1].imshow(HH)
    plt.tight_layout()
    plt.show()"""
    dim = LL.shape
    LL_h = LL.shape[0]
    LL_w = LL.shape[1]
    # LL_n = LL.shape[2]

    print("Image height: {} Image width: {}".format(LL_h, LL_w))

    flag = 0
    for i in range(max_row, max_row+LL_h):
        for j in range(max_col, max_col+LL_w):
            # print('LL[i][j]: '+LL[i][j])
            binary = decimaltoBinary(ord(msg[msg_index]))
            print(binary)

            LL[i, j] = float(int(binary, 2))
            msg_index += 1
            if msg_index == msg_size:
                flag = 1
                break
        if flag == 1:
            break

    pywt.idwt2(coeffs, 'haar')
    yuv = cv2.merge((y, u, v))
    cv2.imshow('The new frame', frame)
    cv2.waitKey(10000)

    vid.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
