#!/usr/bin/env python3
import argparse
import logging
import signal
import sys
from aiy.assistant.grpc import AssistantServiceClientWithLed
from aiy.board import Board


def volume(string):
    value = int(string)
    if value < 0 or value > 100:
        raise argparse.ArgumentTypeError('Volume must be in [0...100] range.')
    return value


def main():
    logging.basicConfig(level=logging.DEBUG)
    signal.signal(signal.SIGTERM, lambda signum, frame: sys.exit(0))

    parser = argparse.ArgumentParser(description='Assistant service with Button')
    parser.add_argument('--language', default='es-MX')
    parser.add_argument('--volume', type=volume, default=100)
    args = parser.parse_args()

    with Board() as board:
        assistant = AssistantServiceClientWithLed(board=board,
                                                  volume_percentage=args.volume,
                                                  language_code=args.language)
        while True:
            logging.info('Press button to start conversation...')
            board.button.wait_for_press()
            logging.info('Conversation started!')
            assistant.conversation()


if __name__ == '__main__':
    main()
