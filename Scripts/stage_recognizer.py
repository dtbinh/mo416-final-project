from neuralnet import NeuralNet
from extractfeatures import extract_counter_feat


class StageRecognizer():
    def __init__(self, trained_net_path):
        self.net = NeuralNet()
        self.net.load_from_file(trained_net_path)

    def recognize_image(self, img):
        net_return = self.net.apply_over_data(extract_counter_feat(img))
        stage_number = int(round(net_return))
        stage = ''
        precision = 'strong'

        if stage_number == 1:
            stage = 'red'
            if abs(stage_number - 1) > .15:
                precision = 'weak'

        elif stage_number == 2:
            stage = 'yellow'
            if abs(stage_number - 1) > .15:
                precision = 'weak'

        elif stage_number == 3:
            stage = 'green'
            if abs(stage_number - 1) > .15:
                precision = 'weak'

        return stage, precision
