#!/usr/bin/python

from pybrain.datasets.supervised import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer

import cPickle as pickle


class NeuralNet:
    def __init__(self):
        self.net = None
        self.data_set = None
        self.trainer = None

    def build(self, inputs, hidden, output):
        self.net = buildNetwork(inputs, hidden, output)

    def create_data_set(self, inputs, targets):
        self.data_set = SupervisedDataSet(inputs, targets)

    def add_list_of_data(self, list_of_data, data_class):
        for dt in list_of_data:
            self.data_set.addSample(dt, data_class)

    def train(self):
        self.trainer = BackpropTrainer(self.net, self.data_set)
        error = 10000
        iteration = 0
        while error > 0.001:
            error = self.trainer.train()
            iteration += 1

    def save_training_to_file(self, filename):
        with open(filename, 'w') as f:
            pickle.dump(self.net, f)

    def load_net_from_file(self, filename):
        with open(filename, 'r') as f:
            self.net = pickle.load(f)
