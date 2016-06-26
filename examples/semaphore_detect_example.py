#!/usr/bin/env python

from stage_recognizer import StageRecognizer
import cv2

if __name__ == "__main__":

    stage_recognizer = StageRecognizer("../trained_net_0_15.bin")

    # Determine stage from single image
    img = cv2.imread("../Images/Semaforo_amarelo/renamed/0004.png", cv2.CV_LOAD_IMAGE_COLOR)
    color, precision = stage_recognizer.recognize_image(img)

    print color, precision

    base_path_red = "../Images/Semaforo_vermelho/renamed/%04d.png"
    base_path_yellow = "../Images/Semaforo_amarelo/renamed/%04d.png"
    base_path_green = "../Images/Semaforo_verde/renamed/%04d.png"

    misses = 0
    weaks = 0
    for i in range(1, 293):
        path = base_path_red % i
        img = cv2.imread(path, cv2.CV_LOAD_IMAGE_COLOR)
        color, precision = stage_recognizer.recognize_image(img)

        if color != "red":
            misses += 1
            print path
        if precision == "weak":
            weaks += 1

    print "red misses:", misses
    print "red weaks:", weaks
    print "------------------------"

    misses = 0
    weaks = 0
    for i in range(1, 184):
        path = base_path_yellow % i
        img = cv2.imread(path, cv2.CV_LOAD_IMAGE_COLOR)
        color, precision = stage_recognizer.recognize_image(img)

        if color != "yellow":
            misses += 1
            print path
        if precision == "weak":
            weaks += 1

    print "yellow misses:", misses
    print "yellow weaks:", weaks
    print "------------------------"

    misses = 0
    weaks = 0
    for i in range(1, 180):
        path = base_path_green % i
        img = cv2.imread(path, cv2.CV_LOAD_IMAGE_COLOR)
        color, precision = stage_recognizer.recognize_image(img)

        if color != "green":
            misses += 1
            print path
        if precision == "weak":
            weaks += 1

    print "green misses:", misses
    print "green weaks:", weaks
    print "------------------------"
