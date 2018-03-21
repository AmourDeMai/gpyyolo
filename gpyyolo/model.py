import cv2
import glob
import json
import numpy as np
import os
import pyyolo
from util.log import Log

LOG = Log.get_logger(log_level='i')


class Model(object):

    def __init__(self):
        LOG.info('init model...')
        conf_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 'conf.json')
        assert os.path.exists(conf_file), '{} config file not exists, please' \
                                          'copy it from conf.json.tmpl'
        with open(conf_file) as f:
            self.params = json.load(f)

    def _init_model(self):
        LOG.info('init general python yolo model')
        pyyolo.init(self.params['darknet_path'], self.params['datacfg'],
                    self.params['cfgfile'], self.params['weightfile'])

    @staticmethod
    def _init_frame():
        LOG.info('init frame')
        cv2.namedWindow('frame', cv2.WINDOW_NORMAL)

    @staticmethod
    def draw_rects(image, detects):
        """
        :param detects: list of detect,
                        [{'class': 'person', 'left', 'right', 'top', 'bottom',
                        'prob'}]
        :param image:
        """

        for detect in detects:
            cv2.putText(
                image,
                detect['class'] + "  %.2f %%" % (detect['prob'] * 100),
                (detect['left'] + 6, detect['top'] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            cv2.rectangle(
                image,
                (detect['left'], detect['top']),
                (detect['right'], detect['bottom']), (0, 0, 255), 1)

    def train(self):
        # TODO
        pass

    def _inference_image(self, image):
        frame = image.transpose(2, 0, 1)
        c, h, w = frame.shape
        data = frame.ravel() / 255.0
        data = np.ascontiguousarray(data, dtype=np.float32)

        detects = pyyolo.detect(w, h, c, data, self.params['thresh'],
                                self.params['hier_thresh'])

        return detects

    def inference(self):
        if self.params.get('show_window', True):
            Model._init_frame()

        self._init_model()

        for image_path in glob.glob(os.path.join(self.params['test_dir'], '*')):
            image = cv2.imread(image_path)
            if image is None:
                continue
            if image.shape[:2] != (self.params['height'],
                                   self.params['width']):
                image = cv2.resize(image, (self.params['width'],
                                           self.params['height']))
            detects = self._inference_image(image)
            Model.draw_rects(image, detects)

            if self.params.get('show_window', True):
                cv2.imshow('frame', image)

            cv2.waitKey(5000)


if __name__ == '__main__':
    model = Model()
    # model.train()
    model.inference()

