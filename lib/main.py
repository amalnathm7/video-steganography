import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_dir)
from modules.embedding.data_embedding import data_embedding
from modules.extraction.data_extraction import data_extraction

if __name__ == '__main__':
    print("Video Steganography")
    data_embedding()
    data_extraction()