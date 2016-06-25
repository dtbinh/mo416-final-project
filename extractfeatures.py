import numpy as np
import cv2
from matplotlib import pyplot as plt

# http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_orb/py_orb.html
def extract_features(img):
    orb = cv2.ORB()
    kp = orb.detect(img, None)
    key_points, _ = orb.compute(img, kp)
    features_list = []
    for el in key_points:
        features_list.append((el.angle, el.class_id, el.octave, el.response, el.size))

    return features_list


def extract_hist_features(img):
    color = ('b', 'g', 'r')
    feats = []
    for i in range(3):
        histr = cv2.calcHist([img], [i], None, [256], [0, 256])
        values = []
        # histogram is a list of list (weird!)
        # and each list has a value
        for el in histr:
            values.append(el[0])
        feats = feats + values

    return feats


if __name__ == "__main__":
    img2 = cv2.imread('/home/hoshiro/Pictures/test-img/traffic-light.png', cv2.CV_LOAD_IMAGE_COLOR)  # trainImage
    features = extract_hist_features(img2)
    print features
