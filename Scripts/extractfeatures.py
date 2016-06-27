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
        features_list += [el.angle, el.class_id, el.octave, el.response, el.size]

    return features_list


def extract_hist_features(img):
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


def extract_hist_features_2(img):
    # hist = cv2.calcHist([img], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    hist = cv2.calcHist([img], [0, 1, 2], None, [8, 8, 8], [0, 64, 0, 64, 0, 64])
    return hist.flatten()


def extract_mean_std_feat(img):
    means, stds = cv2.meanStdDev(img)
    return np.concatenate([means, stds]).flatten()


def extract_counter_feat(img):
    red_mask = mask_red(img)
    yellow_mask = mask_yellow(img)
    green_mask = mask_green(img)
    return [cv2.countNonZero(red_mask), cv2.countNonZero(yellow_mask), cv2.countNonZero(green_mask)]


def mask_red(img):
    upper = np.array([122, 69, 255])
    lower = np.array([0, 0, 128])
    mask = cv2.inRange(img, lower, upper)
    return mask


def mask_yellow(img):
    upper = np.array([102, 255, 255])
    lower = np.array([0, 102, 102])
    mask = cv2.inRange(img, lower, upper)
    return mask


def mask_green(img):
    upper = np.array([100, 255, 133])
    lower = np.array([0, 72, 0])
    mask = cv2.inRange(img, lower, upper)
    return mask


if __name__ == "__main__":
    img2 = cv2.imread('../Images/Semaforo_verde/renamed/0001.png', cv2.CV_LOAD_IMAGE_COLOR)  # trainImage

    features = extract_counter_feat(img2)
    #
    # print len(features)
    # print features.shape
    print features
    # print features[0]
