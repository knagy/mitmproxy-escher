from configparser import ConfigParser
from escherauth_go.escher_signer import EscherSigner
from fnmatch import fnmatch
from mitmproxy import ctx


class Config:
    def __init__(self, config_file):
        self._config_file = config_file

    def get(self):
        config = ConfigParser()
        config.optionxform = str
        files = config.read(self._config_file)

        if files:
            ctx.log.info('[Escher] Config file "{}" loaded'.format(self._config_file))
        else:
            ctx.log.error('[Escher] Could not load config file "{}"'.format(self._config_file))

        return config


class SignerFactory:
    def __init__(self, config: Config):
        self._config = config

    def get_for_host(self, host):
        config = self._config.get()

        for section in config.sections():
            if not fnmatch(host, section):
                continue

            ctx.log.info('[Escher] found "{}" section for host "{}"'.format(section, host))
            return EscherSigner(**config[section])

        ctx.log.info('[Escher] no section found for host "{}"'.format(host))


class SignRequest:
    def __init__(self, signer: SignerFactory):
        self._signer = signer

    def request(self, flow):
        signer = self._signer.get_for_host(flow.request.pretty_host)
        if not signer:
            return

        headers = signer.signRequest(
            flow.request.method,
            flow.request.path,
            flow.request.text,
            {'Host': flow.request.host_header}
        )

        for k, v in headers.items():
            flow.request.headers[k] = v
