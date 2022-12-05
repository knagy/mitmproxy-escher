import logging
from configparser import ConfigParser
from escherauth_go.escher_signer import EscherSigner
from fnmatch import fnmatch
from mitmproxy import ctx, http


class Config:
    def __init__(self, config_file):
        self._config_file = config_file

    def get(self):
        config = ConfigParser()
        config.optionxform = str

        if config.read(self._config_file):
            logging.info('[Escher] Config file "{}" loaded'.format(self._config_file))
        else:
            logging.error('[Escher] Could not load config file "{}"'.format(self._config_file))

        return config


class SignerFactory:
    def get_for_host(self, config, host):
        for section in config.sections():
            if not fnmatch(host, section):
                continue

            logging.info('[Escher] found "{}" section for host "{}"'.format(section, host))
            return EscherSigner(**config[section])

        logging.info('[Escher] no section found for host "{}"'.format(host))


class SignRequest:
    def __init__(self, factory: SignerFactory):
        self._factory = factory
        self._config = None

    def load(self, loader):
        loader.add_option(
            name='escher_config',
            typespec=str,
            default='',
            help='path to escher config file'
        )

    def configure(self, updates):
        if 'escher_config' not in updates or not ctx.options.escher_config:
            return

        self._config = Config(ctx.options.escher_config)

    def request(self, flow: http.HTTPFlow) -> None:
        if not self._config:
            return

        signer = self._factory.get_for_host(self._config.get(), flow.request.pretty_host)
        if not signer:
            return

        headers = signer.signRequest(
            flow.request.method,
            flow.request.path,
            flow.request.text,
            {'Host': flow.request.host_header}
        )

        for k, v in headers.items():
            if flow.request.is_http2:
                k = k.lower()
            flow.request.headers[k] = v


addons = [
    SignRequest(SignerFactory())
]
