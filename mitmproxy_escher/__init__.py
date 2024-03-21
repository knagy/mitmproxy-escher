import logging
from configparser import ConfigParser
from escherauth import Escher
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
            return Escher(
                config[section]['apiKey'],
                config[section]['apiSecret'],
                config[section]['credentialScope'],
                {
                    'hash_algo': config[section].get('hashAlgo', 'SHA256'),
                    'algo_prefix': config[section].get('algoPrefix', 'EMS'),
                    'vendor_key': config[section].get('vendorKey', 'EMS'),
                    'auth_header_name': config[section].get('authHeaderName', 'X-EMS-Auth'),
                    'date_header_name': config[section].get('dateHeaderName', 'X-EMS-Date'),
                }
            )

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

        signed_request = signer.sign_request({
            'method': flow.request.method,
            'url': flow.request.path,
            'host': flow.request.host_header,
            'body': flow.request.text,
        })

        for k, v in signed_request['headers']:
            if flow.request.is_http2:
                k = k.lower()
            flow.request.headers[k] = v


addons = [
    SignRequest(SignerFactory())
]
