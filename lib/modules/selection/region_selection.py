# Code to implement region selection with grey wolf optimisation and PCA analysis

import cv2
import numpy as np
from sklearn.decomposition import PCA
import random
import math
from scipy.stats import kurtosis
from scipy.stats import entropy


def option(opt):
    match opt:
        case 1: return "akiyo"
        case 2: return "bowing"
        case 3: return "bus"
        case 4: return "city"
        case 5: return "crew"


def get_energy(img):
    entropies = entropy(img.flatten())
    return np.mean(entropies)
    # return (img ** 2).sum()/img.size


def get_intensity(img):
    diff = np.abs(np.diff(img.flatten()))
    return np.mean(diff)
    # return img.sum()/img.size


def get_coverage(img):
    return np.count_nonzero(img)/img.size
    # threshold = 30
    # similar = np.sum(np.abs(np.diff(img))< threshold)
    # return similar/img.size


def get_kurtosis(img):
    return kurtosis(img.flatten())


def get_fitness(frame, i, j, msg_size):
    img = frame[i:i+msg_size, j:j+1]
    Energy = get_energy(img)
    Intensity = get_intensity(img)
    Kurtosis = get_kurtosis(img)
    Coverage = get_coverage(img)
    # print(" Energy = {}, Intensity = {}, Kurtosis = {}, Coverage = {}".format(Energy,Intensity,Kurtosis,Coverage))
    Fitness = (Energy + (1 - Intensity) + Kurtosis+Coverage)/4
    # print("Fitness = {}".format(Fitness))

    # return np.var(img)
    return Fitness


def get_index(regions, i, j):
    for region in regions:
        if (region['row'] == i and region['col'] == j):
            return region['index']

    return -1


def absolute(array):
    return [abs(x) for x in array]


def get_alpha(wolves, regions):
    alpha_fitness = -np.inf
    alpha = [0, 0]
    beta_fitness = -np.inf
    beta = [0, 0]
    delta_fitness = -np.inf
    delta = [0, 0]
    for wolf in wolves:
        i = wolf[0]
        j = wolf[1]

        index = get_index(regions, i, j)

        # print("index = ",index)
        if (index >= len(regions)):
            index = len(regions) - 1
        if (index != -1):
            if (alpha_fitness < regions[index]['fitness']):
                delta_fitness = beta_fitness
                delta = beta

                beta_fitness = alpha_fitness
                beta = alpha
                alpha_fitness = regions[index]['fitness']
                alpha = [regions[index]['row'], regions[index]['col']]
        else:
            print("The regions not found: {} {}".format(i, j))

    return (alpha, beta, delta)


def get_robust_regions(frame, height, width, msg_size):
    """Initialising population and the initial wolf population"""
    population = 20
    regions = []
    values = [[x, y*msg_size]
              for x in range(math.floor(height)) for y in range(math.floor(width/msg_size))]
    wolves = random.choices(values, k=20)
    # print(wolves)

    r = 0
    a = 2
    iterations = 20

    """Setting up the grids and finding their fitness functions"""
    for i in range(0, int(height)):
        for j in range(0, int(width), msg_size):
            d = {}
            d['row'] = i
            d['col'] = j
            d['row_end'] = i+msg_size
            r += 1
            d['index'] = r
            d['fitness'] = get_fitness(frame, i, j, msg_size)
            regions.append(d)

    """Get the initial values of alpha,beta and delta from the current population"""
    # print(regions)
    r1 = random.random()
    r2 = random.random()
    G = (2*a*r1) - a
    H = 2*r2
    alpha, beta, delta = get_alpha(wolves, regions)
    # print(alpha,beta,delta)

    # print("Len=",len(regions))
    t = 0
    while (t < iterations):
        i = 0
        for wolf in wolves:

            # P1- Alpha
            a = np.array([2 - t*((2)/iterations), 2 - t*((2)/iterations)])
            r1 = np.random.rand(2)
            r2 = np.random.rand(2)
            G1 = (2*a).dot(r1) - a
            H1 = 2*r2
            K_alpha = absolute(G1.dot(alpha) - wolf)
            p1 = absolute(alpha - H1.dot(K_alpha))
            p1 = np.array(p1)
            if (p1[0] >= height):
                p1[0] = height-1
            if (p1[1] >= width):
                p1[1] = width-1
            # print("r1 = {}, r2 ={}, G1= {}, H1={},alpha = {}, K_alpha={},p1={}".format(r1,r2,G1,H1,alpha,K_alpha,p1))

            # P2- Beta
            a = np.array([2 - t*((2)/iterations), 2 - t*((2)/iterations)])
            r1 = np.random.rand(2)
            r2 = np.random.rand(2)
            G2 = (2*a).dot(r1) - a
            H2 = 2*r2
            K_beta = absolute(G2.dot(beta) - wolf)
            p2 = absolute(beta - H2.dot(K_beta))
            p2 = np.array(p2)

            if (p2[0] >= height):
                p2[0] = height-1
            if (p2[1] >= width):
                p2[1] = width-1
            # print("r1 = {}, r2 ={}, G2= {}, H2={},beta = {}, K_beta={},p2={}".format(r1,r2,G2,H2,beta,K_beta,p2))

            # P3-delta
            a = np.array([2 - t*((2)/iterations), 2 - t*((2)/iterations)])
            r1 = np.random.rand(2)
            r2 = np.random.rand(2)
            G3 = (2*a).dot(r1) - a
            H3 = 2*r2
            K_delta = absolute(G3.dot(delta) - wolf)
            p3 = absolute(delta - H3.dot(K_delta))
            p3 = np.array(p3)
            if (p3[0] >= height):
                p3[0] = height-1
            if (p3[1] >= width):
                p3[1] = width-1
            # print("r1 = {}, r2 ={}, G3= {}, H3={},delta = {}, K_delta={},p3={}".format(r1,r2,G3,H3, delta,K_delta,p3))

            p_next = (p1+p2+p3) * 1/3
            # print(p_next)

            # print()

            """Bringing the values within their borders"""
            remain = int(p_next[1]) % msg_size

            if (remain != 0):
                p_next[1] = int(p_next[1])+msg_size-remain
            else:
                p_next[1] = int(p_next[1])

            p_next[0] = int(p_next[0])
            # print("p_next = {}, remian = {}".format(p_next,remain))
            if (p_next[0] >= height):
                remain = height-1
            if (p_next[1] > width):
                remain = p_next[1] % msg_size
                p_next[1] = p_next[1]-remain-msg_size
            wolves[i] = p_next
            i += 1

        (alpha, beta, delta) = get_alpha(wolves, regions)
        # print("Alpha = {}, Beta ={}, Delta={}".format(alpha,beta,delta))

        t += 1
        # print()

    if (alpha[0]+1 >= height):
        alpha[0] = int(height)-1-1
    if (alpha[1]+msg_size >= width):
        alpha[1] = int(width) - msg_size-1
    print("\n alpha = {}".format(alpha))

    img = frame[alpha[0]:alpha[0]+1, alpha[1]:alpha[1]+msg_size]
    # frame = cv2.rectangle(frame,(alpha[0],alpha[1]), (alpha[0]+msg_size,alpha[1]+1), (255,255,255),2)
    # cv2.imshow('Bounding Rectangle',frame)
    # cv2.waitKey(5000)
    # cv2.imshow('Img',img)
    # cv2.waitKey(5000)
    return ([(alpha[0], alpha[1]), (alpha[0]+1, alpha[1]+msg_size)])


def check_region(robust_regions, frame_no, b):
    for i in robust_regions[frame_no]:
        if (i['start'] == b['start']) and (i['end'] == b['end']):
            return 1
    return 0


def set_coordinates(robust_regions, frame, frame_no, height, width, msg_size):
    coordinates = get_robust_regions(frame, height, width, msg_size)
    b = {}
    b['start'] = (coordinates[0][0], coordinates[1][0])
    b['end'] = (coordinates[1][0], coordinates[1][1])
    if (check_region(robust_regions, frame_no, b)) == 0:
        robust_regions[frame_no].append(b)
    else:
        robust_regions = set_coordinates(
            robust_regions, frame, frame_no, height, width, msg_size)
    return robust_regions


def gwo_region_selection(cap, msg_size, frame_list, no_of_blocks):
    frame_no = 0
    robust_regions = {}
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_no += 1
        if frame_no not in frame_list:
            continue
        robust_regions[frame_no] = []
        for i in range(0, no_of_blocks):
            """coordinates = Get_Robust_Regions(frame,height,width,msg_size)
            b = {}
            b['start'] = (coordinates[0][0],coordinates[1][0])
            b['end'] = (coordinates[0][1],coordinates[1][1])
            if(Check_Re gion(robust_regions,frame_no,b)) == 0:
                robust_regions[frame_no].append(b)
            else:
                coordinates = Get_Robust_Regions(frame,height,width,msg_size)"""
            robust_regions = set_coordinates(
                robust_regions, frame, frame_no, height, width, msg_size)
        # print(robust_regions)
    return robust_regions


def find_summation(next_components):
    s = 0
    for i in next_components:
        s = s+(i*i)
    return s


def find_index_min(block, value):
    l = []
    mini = 1000000
    ind = -1
    for b in block:
        if (b['pca'] < value):
            if (b['pca'] < mini):
                mini = b['pca']
                ind = b['index']
    return ind

def find_min_pca(blocks):
    minpca = 1000000
    ind = -1
    for b in blocks:
        if(b['pca'] < minpca):
            minpca = b['pca']
    return minpca


def find_threshold(y,block_size,height,width,no_of_blocks):
    #threshold = 9.5
    #max_difference = 0.2
    summ = 0
    count = 0
    #while(1):
    for i in range(0, int(height), block_size):
        for j in range(0, int(width), block_size):
            if((i + block_size >= height) or (j + block_size >= width)):
                track = 1
                break

            r = y[i:i+block_size, j:j+block_size]

            #Used for Thresholding method 2
            # greater_sum = 0
            # greater_count = 0
            # lesser_count = 0
            # lesser_sum = 0

            # NOTE: For storing the data instead of taking nXn matrix take 1xn matrix and check
            # NOTE: For storing the data take ceil(root(n))xceil(root(n)) size of block to fill the entire block

            # cv2.imshow('t',r)
            # cv2.waitKey(1000)
            """Applying PCA to find the first principal component"""
            np.seterr(invalid='ignore')
            pca = PCA(n_components=1, svd_solver='full')
            # print(pca)
            # npdata =  np.asarray(r)
            X = np.array(r)
            pca.fit(X)
            first_component = pca.singular_values_
            first_component_sq = first_component**2

            """ Applying PCA to find the remaining principal components"""
            pca = PCA(svd_solver='full')
            Y = np.array(r)
            pca.fit(Y)
            next_components = pca.singular_values_
            # print(next_components)
            summation = find_summation(next_components)

            """Finding the propotion of the first principal component of the image"""
            if (summation != 0):
                propotion_first_component = first_component_sq/summation
            else:
                propotion_first_component = -1

            f = open("lib/modules/selection/region.txt","a")
            f.write("\n REgion {},{} - {},{}: \n{}".format(i,j,i+block_size,j+block_size,propotion_first_component))
            f.close()

            #METHOD 1
            """if (len(blocks) < no_of_blocks):
                block = {}
                block['pca'] = propotion_first_component
                block['row'] = i
                block['col'] = j
                block['index'] = b
                blocks.append(block)
                b += 1
            else:
                # print("Changed")
                # print(blocks)
                ind = Find_Index_Min(blocks, propotion_first_component)
                if (ind != -1):
                    blocks[ind]['pca'] = propotion_first_component
                    blocks[ind]['row'] = i
                    blocks[ind]['col'] = j
                    blocks[ind]['index'] = ind"""
            
            #Thresholding Method 2
            # if(propotion_first_component >= threshold):
            #     greater_sum = greater_sum+propotion_first_component
            #     greater_count = greater_count+1
            # else:
            #     lesser_sum = lesser_sum+propotion_first_component
            #     lesser_count = lesser_count+1
            summ =  summ+propotion_first_component
            count = count+1

        #Thresholding Method 2
        # if((greater_count == 0)and(lesser_count == 0)):
        #     avg_threshold = 5
        # elif (greater_count == 0):
        #     lesser_mean = lesser_sum/lesser_count
        #     avg_threshold = lesser_mean
        # elif (lesser_count == 0):
        #     greater_mean = greater_sum/greater_count
        #     avg_threshold = greater_mean
        # else:
        #     greater_mean = greater_sum/greater_count
        #     lesser_mean = lesser_sum/lesser_count
        #     avg_threshold = greater_mean+lesser_mean/2
    threshold = summ/count
    
    #Threshold Method 2:
    # print("Current threshold = {} and new threshold = {} diff= {}".format(threshold,avg_threshold,abs(threshold-avg_threshold)))
    #     if(abs(threshold - avg_threshold) <= max_difference):
    #         threshold = avg_threshold
    #         break
    #     else:
    #         print("Here")
    #         threshold = avg_threshold
    #         print("Now threshold is: "+str(threshold))
    return threshold


def pca_analysis(y, block_size, height, width, no_of_blocks, frame_no):
    row_start = 0
    if(frame_no == 0):
        row_start = 1
    # if multiple blocks to be selected
    blocks = []
    b = 0

    #threshold = Find_Threshold(y,block_size,height,width,no_of_blocks)
    # print("The threshold is"+str(threshold))
    # f = open("lib/modules/selection/region.txt","a")
    # f.write("\n THreshold selected: \n{}".format(threshold))
    # f.close()

    max_pca = 0
    min_pca = 1000000
    max_row, max_col = 0, 0
    track = 0

    # Dividing the image into blocks and finding the PCA of each block
    for i in range(0, int(height) - block_size, block_size):
        for j in range(row_start, int(width) - block_size, block_size):
            if((i + block_size >= height) and (j + block_size >= width)):
                track = 1
                break

            r = y[i:i+block_size, j:j+block_size]

            # NOTE: For storing the data instead of taking nXn matrix take 1xn matrix and check
            # NOTE: For storing the data take ceil(root(n))xceil(root(n)) size of block to fill the entire block

            # cv2.imshow('t',r)
            # cv2.waitKey(1000)
            """Applying PCA to find the first principal component"""
            np.seterr(invalid='ignore')
            pca = PCA(n_components=1, svd_solver='full')
            # print(pca)
            # npdata =  np.asarray(r)
            X = np.array(r)
            pca.fit(X)
            first_component = pca.singular_values_
            first_component_sq = first_component**2

            """ Applying PCA to find the remaining principal components"""
            pca = PCA(svd_solver='full')
            Y = np.array(r)
            pca.fit(Y)
            next_components = pca.singular_values_
            # print(next_components)
            summation = find_summation(next_components)

            """Finding the propotion of the first principal component of the image"""
            if (summation != 0):
                propotion_first_component = first_component_sq/summation
            else:
                propotion_first_component = -1
                

            if (len(blocks) < no_of_blocks):
                block = {}
                block['pca'] = propotion_first_component
                block['row'] = i
                block['col'] = j
                block['index'] = b
                blocks.append(block)
                b += 1
                if(propotion_first_component < min_pca):
                    min_pca = propotion_first_component
            else:
                if(propotion_first_component > min_pca):
                # print("Changed")
                # print(blocks)
                    ind = find_index_min(blocks, propotion_first_component)
                    if (ind != -1):
                        blocks[ind]['pca'] = propotion_first_component
                        blocks[ind]['row'] = i
                        blocks[ind]['col'] = j
                        blocks[ind]['index'] = ind
                        min_pca = find_min_pca(blocks)

            # if(propotion_first_component > threshold):
            #     if(len(blocks) < no_of_blocks):
            #         block = {}
            #         block['pca'] = propotion_first_component
            #         block['row'] = i
            #         block['col'] = j
            #         block['index'] = b
            #         blocks.append(block)

           # print(pca.singular_values_)
            """if(propotion_first_component > max_pca):
                max_pca = propotion_first_component
                print(max_pca)
                max_row = i
                max_col = j"""
        if(track == 1):
            break

    # print(max_row)
    # print(max_col)
    # print("The coordinates of image block are: ({},{},{},{})".format(max_row,max_row+msg_size,max_col,max_col+msg_size))
    # return (max_row,max_row+msg_size,max_col,max_col+msg_size)
    
    return blocks


def get_regions(blocks, msg_size):
    l = []
    for block in blocks:

        b = {}
        b['start'] = (block['row'], block['col'])
        b['end'] = (block['row']+msg_size-1, block['col']+msg_size-1)
        l.append(b)
    return l


def pca_region_selection(cap, block_size, frame_list, no_of_blocks):
    frame_no = -1
    robust_regions = {}

    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_no += 1
        if frame_no not in frame_list:
            continue

        # Extracting yuv components from the image
        yuv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
        # cv2.imshow('YUV', yuv_img)
        # cv2.waitKey(1000)

        y, u, v = cv2.split(yuv_img)
        # f = open("lib/modules/selection/region.txt","a")
        # f.write("\n FRame number: \n{}".format(frame_no))
        # f.close()
        block = pca_analysis(y, block_size, height, width,
                             no_of_blocks=no_of_blocks,frame_no= frame_no )
        # print(block)
        l = get_regions(block, block_size)
        robust_regions[frame_no] = l
        # print(robust_regions)
    return robust_regions


# def main():

#     # Capturing the video
#     vid = cv2.VideoCapture(
#         'C:/Users/user/Documents/MyFiles/Project/dataset/akiyo_stego.avi')

#     video_fps = vid.get(cv2.CAP_PROP_FPS)
#     total_frames = vid.get(cv2.CAP_PROP_FRAME_COUNT)
#     height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
#     width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)

#     print(
#         f"Frame per sec: {video_fps}\n Total FRame: {total_frames}\n Height: {height} \nWidth: {width}")

#     # Getting data to be embedded
#     msg = input("Enter the message to be embedded: ")
#     msg_size = len(msg)

#     """ NOTE: The data to be embedded can be of different types
#             1. text
#             2. image
#             3. video
#             4. audio"""

#     if (msg_size > width):
#         print("Get another video to embedd")
#         exit()

#     # temporary
#     frame_list = [8, 13, 36, 37, 41, 65, 100, 200, 288]
#     """PCA analysis method"""
#     # robust_regions = PCA_Implementation(vid,msg_size,height,width,frame_list)
#     # print(robust_regions)

#     """Grey Wolf Optimisation"""
#     robust_regions = robust_region = GWO(
#         vid, msg_size, height, width, frame_list)
#     print(robust_regions)

#     """cv2.imshow('Y',y)
#     cv2.waitKey(1000)
#     cv2.imshow('U',u)
#     cv2.waitKey(1000)
#     cv2.imshow('V',v)
#     cv2.waitKey(1000)"""

#     # (max_row,max_row_end,max_col,max_col_end) = pca_analysis(y, msg_size,height,width)

#     """Selected region printed"""
#     # img = y[max_row:max_row_end,max_col:max_col_end]
#     # cv2.imshow('Selected region',img)
#     # cv2.waitKey(10000)

#     vid.release()
#     cv2.destroyAllWindows()


# if __name__ == '__main__':
#     main()
#     """NOTE : combine the frame selection an region selection principles to derive and equation, which will help in optimal selection of frames"""
