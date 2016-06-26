#!/usr/bin/env python
from neuralnet import NeuralNet
from extractfeatures import *
import cv2


def load_img_and_extract_feat(path):
    img = cv2.imread(path, cv2.CV_LOAD_IMAGE_COLOR)
    return extract_hist_features(img)


if __name__ == "__main__":

    base_path_red = "Images/Semaforo_vermelho/renamed/%04d.png"
    base_path_yellow = "Images/Semaforo_amarelo/renamed/%04d.png"
    base_path_green = "Images/Semaforo_verde/renamed/%04d.png"
    #
    data_set_red = []
    for i in range(1, 293):
    # for i in range(1, 50):
        path = base_path_red % i
        data_set_red.append(load_img_and_extract_feat(path))

    data_set_yellow = []
    for i in range(1, 184):
    # for i in range(1, 50):
        path = base_path_yellow % i
        data_set_yellow.append(load_img_and_extract_feat(path))

    data_set_green = []
    for i in range(1, 180):
    # for i in range(1, 50):
        path = base_path_green % i
        data_set_green.append(load_img_and_extract_feat(path))

    print len(data_set_red[0])

    neural_net = NeuralNet()
    neural_net.build(len(data_set_red[0]), len(data_set_red[0])/3, 1)
    neural_net.create_data_set()
    neural_net.add_list_of_data(data_set_red, 1)
    neural_net.add_list_of_data(data_set_yellow, 2)
    neural_net.add_list_of_data(data_set_green, 3)
    neural_net.train()
    neural_net.save_to_file("trained_net.bin")

    print neural_net.apply_over_data(data_set_red[0])
    print neural_net.apply_over_data(data_set_yellow[0])
    print neural_net.apply_over_data(data_set_green[0])

    # neural_net = NeuralNet()
    # neural_net.load_from_file("trained_net_0_15.bin")

    print neural_net.apply_over_data(load_img_and_extract_feat(base_path_red % 292))
    print neural_net.apply_over_data(load_img_and_extract_feat(base_path_yellow % 183))
    print neural_net.apply_over_data(load_img_and_extract_feat(base_path_green % 179))

    print neural_net.apply_over_data(load_img_and_extract_feat(base_path_red % 1))
    print neural_net.apply_over_data(load_img_and_extract_feat(base_path_yellow % 2))
    print neural_net.apply_over_data(load_img_and_extract_feat(base_path_green % 3))