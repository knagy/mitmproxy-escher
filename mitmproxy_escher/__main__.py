from argparse import ArgumentParser
from mitmproxy_escher import Config, SignerFactory, SignRequest


def start():
    parser = ArgumentParser()
    parser.add_argument('-c', '--config', help='path to config file')
    args = parser.parse_args()

    config = Config(args.config)
    signer = SignerFactory(config)
    return SignRequest(signer)


if __name__ == '__main__':
    print(__file__)
