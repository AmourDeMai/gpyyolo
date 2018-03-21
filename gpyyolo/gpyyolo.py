import argparse

from util.log import Log
from model import Model


LOG = Log.get_logger(log_level='i')


def main():
    parser = argparse.ArgumentParser(
        description='Object detection task: train|inference', prog='model')
    parser.add_argument('-task', dest='task', help='train|inference')
    args = parser.parse_args()

    model = Model()
    if args.task == 'train':
        model.train()
    elif args.task == 'inference':
        model.inference()
    else:
        LOG.error('Wrong params')


if __name__ == '__main__':
    main()