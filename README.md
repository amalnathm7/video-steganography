# Advancing Video Steganography: Achieving High-Capacity Multimedia Data Hiding with Enhanced Quality and Security

## Abstract

Video steganography is a technique that involves hiding secret messages within a video while minimising any noticeable changes or distortions. The proposed work aims to embed multimedia data inside a video in a secure and inconspicuous manner using different phases such as input preprocessing, frame selection, region selection, and data embedding. To enhance the security of input data, AES encryption technique is used as a preprocessing step. To embed the encrypted data into the cover video with minimal distortion, key frames are selected using the Histogram Difference Frame Selection (HDFS) method. The number of key frames to be selected is determined based on the size of the input data. Robust regions are identified among the chosen key frames by applying Principal Component Analysis (PCA) technique as they offer better resistance to distortions caused by embedding data. Afterwards, the encrypted data, encryption key, data size, and initialization vector are embedded into the robust regions using the adaptive LSB332 technique which involves the modification of least significant bits of the pixel values. To ensure the receiver can accurately extract embedded information from the video, the indices of the key frames and robust regions are further embedded in random frames generated using a seed function. Experiments were conducted on different cover videos and input datasets to evaluate the performance of the proposed methodology using different quantitative metrics such as PSNR, SSIM, NCC, BER, etc. The results show that the proposed work outperforms the state-of-the-art methods in video steganography. 

## Proposed Methodology

The main purpose of the proposed methodology is to allow the embedding of multimedia data in a cover video. The proposed system preprocesses the secret input data before embedding it inside robust regions selected within optimal frames of the cover video. The resulting stego video is then transmitted to the receiver, who extracts the hidden data using inverse operations. This systematic approach ensures secure data hiding and extraction within the cover video for reliable transmission through any communication channel. The following figure represents the general flow diagram of the proposed methodology which consists of five different phases: Input Preprocessing, Frame Selection, Region Selection, Data Embedding and Data Extraction. 

<img width="1643" alt="Design" src="https://github.com/amalnathm7/video-steganography/assets/64605131/430f50b7-8086-48fe-b6bd-7c45337b4244">

In the first phase, the multimedia input data, whether text, image, audio, or video, undergoes encryption using the AES symmetric encryption method to ensure the confidentiality of the input data. Simultaneously, the size of the encrypted data is calculated and stored for subsequent phases. This information becomes crucial for determining the number of key frames to be selected and for embedding the data into the cover video. The second phase involves calculating the total number of frames in the cover video. Key frames are then selected using a histogram difference calculation between consecutive frames. Frames with the largest histogram difference are chosen as key frames. The number of key frames selected corresponds to the size of the input data. In the third phase, robust regions within the selected key frames are identified. The Principal Component Analysis (PCA) method is employed to determine these regions, which are less prone to visual changes caused by the embedding process. This ensures a higher level of visual quality in the resulting stego video. The fourth phase is dedicated to the actual embedding process. The encrypted input data, along with the encryption key, data size, and initialization vector, is embedded into the robust regions using the adaptive LSB332 technique. This technique modifies the least significant bits of the RGB values of pixels within the selected regions. By doing so, the data is hidden within the video while minimising noticeable visual artefacts. Additionally, the indices of the key frames and robust regions are embedded within random frames selected using a seed function. This step enhances the security of the embedded data and facilitates its accurate extraction at the receiver's end. The following figure illustrates the detailed flowchart of the proposed methodology.

![Flow Chart](https://github.com/amalnathm7/video-steganography/assets/64605131/8615c47f-688d-478c-8af7-d036053d2444)

## Conclusion and Future Scope

This research proposed a steganographic methodology for embedding various types of multimedia files into cover videos while preserving the visual integrity and minimising perceptible distortions. From the analysis of the experimental results, several key conclusions can be drawn. Firstly, the comparison between the cover frame and the stego frame, as well as their respective histograms, demonstrated that the proposed methodology successfully concealed the input files within the cover frames without introducing noticeable visual distortions or alterations. The similarity between the histograms further indicated that the distribution of pixel values remained largely unchanged, emphasising the preservation of the original visual content.

Additionally, the evaluation of performance metrics for different input sizes revealed that as the size of the embedded text data increased, there was a gradual decrease in PSNR value. For instance, the percentage decrease of the PSNR values for embedding text input of size 5 MB to 10 MB is only 7.1%, suggesting that the distortion in the stego video did not rapidly worsen with larger amounts of embedded text data. Furthermore, the SSIM and NCC values close to unity, along with a constant BER value of zero, indicated a consistent high level of structural similarity, correlation, and accurate extraction of the embedded text from the stego video. Similar trends were observed when applying the proposed methodology to image, audio, and video inputs. 

The comparison with several state-of-the-art techniques demonstrated the superiority of the proposed methodology where it showcased improved results such as PSNR values ranging above 60 dB, 50 dB and 40 dB for input data with sizes nearly 100 KB, 1 MB and 10 MB respectively. The consistent performance across different file types with a 45.1% embedding capacity, along with the ability to maintain visual integrity and minimise perceptible distortions, sets the proposed methodology apart from most of the existing techniques.

In terms of future scope, several areas can be explored to further enhance the proposed methodology. Firstly, it is advisable to investigate the potential of deep learning algorithms for video steganography. Deep learning, particularly utilising neural networks, has shown significant advancements in various domains and could be leveraged to optimise the embedding and extraction process in video steganography. By exploring deep learning algorithms on large-scale video datasets, it is expected that the proposed methodology can be further refined, potentially leading to improved performance, enhanced security, and increased capacity for embedding multimedia data within cover videos. Furthermore, the robustness of the proposed methodology against various content-preserving operations like compression, cropping, resizing or transcoding can further improve the resilience of the methodology. Additionally, the research shall be extended to accommodate real-time applications, such as live video streaming, where embedding and extraction processes need to be performed in a dynamic and time-sensitive manner.

## Installation and Use

To install the proposed video steganography technique, please follow the instructions below:

1. Open a terminal or command prompt and navigate to your desired projects directory:
   ```shell
   cd path/to/your/projects/directory
   ```

2. Clone the video steganography repository from GitHub:
   ```shell
   git clone https://github.com/amalnathm7/video_steganography.git
   ```

3. Open the project in your preferred IDE.

4. Ensure that you have Python3 and pip3 installed, preferably Python 3.9.6 (or a compatible version).

5. Open the terminal within your IDE and install the required dependencies by running the following command:
   ```shell
   pip3 install -r requirements.txt
   ```

6. You shall run _data_embedding.py_ for embedding data and _data_extraction.py_ for extracting data. Otherwise, you can run _main.py_ file to perform both embedding and extraction together. Ten sample cover videos are used in the research for embedding text, image, audio and video files of seven different sizes. 

7. You shall run _experiments.py_ to calculate the PSNR, SSIM, NCC and BER values and write it into an _output.csv_ file. 

8. Now you are ready to use the proposed video steganography technique in your project.

## Detailed Report

The detailed report can be found here: 

## Authors

## Authors

<div align="left">
    <a href="https://github.com/amalnathm7"><img src="https://avatars.githubusercontent.com/u/64605131?v=4" width="100" height="100"></a>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    <a href="https://github.com/Meenakshi-2604"><img src="https://avatars.githubusercontent.com/u/62795103?v=4" width="100" height="100"></a>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    <a href="https://github.com/CodeitM"><img src="https://avatars.githubusercontent.com/u/70884500?v=4" width="100" height="100"></a>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    <a href="https://github.com/sinad-shibin"><img src="https://avatars.githubusercontent.com/u/59430074?v=4" width="100" height="100"></a>
</div>

<div align="left">
    <strong>Amal Nath M.</strong>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    <strong>Meenakshi Nair</strong>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    <strong>Mili Murali</strong>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    <strong>Sinadin Shibin</strong>
</div>


