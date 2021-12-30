import logging
import os

import numpy as np
import cv2 as cv
from data import DATA_DIR

TEST_IMG_DIR = os.path.join(DATA_DIR, 'img/test')
TRAIN_IMG_DIR = os.path.join(DATA_DIR, "img/train")
VALIDATION_IMG_DIR = os.path.join(DATA_DIR, "img/validation")


def load_image(filepath: str, flags=cv.IMREAD_UNCHANGED) -> np.ndarray:
    try:
        print(filepath)
        with open(filepath) as f:
            # Do something with the file
            return cv.imread(filepath, flags)
    except IOError:
        logging.error("File not accessible")
