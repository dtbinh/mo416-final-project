from neuralnet import NeuralNet
from extractfeatures import *
import cv2

if __name__ == "__main__":
    red = cv2.imread('/home/hoshiro/Pictures/test-img/red-light.jpg', cv2.CV_LOAD_IMAGE_COLOR)
    yellow = cv2.imread('/home/hoshiro/Pictures/test-img/yellow-light.jpg', cv2.CV_LOAD_IMAGE_COLOR)
    green = cv2.imread('/home/hoshiro/Pictures/test-img/green-light.jpg', cv2.CV_LOAD_IMAGE_COLOR)

    features_red = extract_hist_features(red)
    features_yellow = extract_hist_features(yellow)
    features_green = extract_hist_features(green)

    neural_net = NeuralNet()
    neural_net.build(len(features_red), len(features_red) / 2, 1)
    neural_net.create_data_set()
    neural_net.add_list_of_data([features_red], 1)
    neural_net.add_list_of_data([features_yellow], 2)
    neural_net.add_list_of_data([features_green], 3)
    neural_net.train()

    print neural_net.apply_over_data(features_yellow)
