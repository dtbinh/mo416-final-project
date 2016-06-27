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
        self.inputs = None
        self.targets = None

    def build(self, inputs, hidden, output):
        self.inputs = inputs
        self.targets = output
        self.net = buildNetwork(inputs, hidden, output, bias=True)

    def create_data_set(self):
        self.data_set = SupervisedDataSet(self.inputs, self.targets)

    def add_list_of_data(self, list_of_data, data_class):
        for dt in list_of_data:
            self.data_set.addSample(dt, data_class)

    def train(self):
        self.trainer = BackpropTrainer(self.net, self.data_set, learningrate=0.01)
        error = 10000
        iteration = 0
        while error > 0.001:
            error = self.trainer.train()
            print "Iteration: {0} Error {1}".format(iteration, error)
            iteration += 1

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            pickle.dump(self.net, f)

    def load_from_file(self, filename):
        with open(filename, 'r') as f:
            self.net = pickle.load(f)

    def apply_over_data(self, data):
        return self.net.activate(data)
