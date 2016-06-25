import numpy as np
import cv2

# http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_orb/py_orb.html
def extract_features(img):
    orb = cv2.ORB()
    kp = orb.detect(img, None)
    key_points, _ = orb.compute(img, kp)
    features = []
    for el in key_points:
        features.append((el.angle, el.class_id, el.octave, el.response, el.size))

    return features


if __name__ == "__main__":
    img2 = cv2.imread('/home/hoshiro/Pictures/test-img/box_in_scene.png', 0)  # trainImage
    features = extract_features(img2)
    print features
