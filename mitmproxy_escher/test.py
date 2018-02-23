from . import Config, SignerFactory, SignRequest
from unittest import TestCase
from unittest.mock import MagicMock, patch


@patch('mitmproxy_escher.ctx')
@patch('mitmproxy_escher.ConfigParser')
class TestConfig(TestCase):
    def setUp(self):
        self.subject = Config('/path/to/config.ini')

    def test_it_loads_the_config_file(self, parser, ctx):
        self.subject.get()

        parser.return_value.read.assert_called_once_with('/path/to/config.ini')

    def test_it_returns_the_parser(self, parser, ctx):
        result = self.subject.get()

        self.assertEqual(parser.return_value, result)

    def test_it_does_not_transform_the_option_names(self, parser, ctx):
        result = self.subject.get()

        self.assertEqual(str, result.optionxform)


@patch('mitmproxy_escher.ctx')
@patch('mitmproxy_escher.EscherSigner')
class TestSignerFactory(TestCase):
    def setUp(self):
        self.subject = SignerFactory()

    def test_it_returns_none_if_there_is_no_matching_config(self, signer, ctx):
        result = self.subject.get_for_host(self.get_config(), 'www.example.net')

        self.assertEqual(None, result)

    def test_it_configures_the_escher_signer_for_the_host(self, signer, ctx):
        self.subject.get_for_host(self.get_config(), 'www.example.org')

        signer.assert_called_once_with(
            apiKey='KEY',
            apiSecret='SECRET',
            credentialScope='credential/scope'
        )

    def test_it_returns_the_configured_escher_signer(self, signer, ctx):
        result = self.subject.get_for_host(self.get_config(), 'www.example.org')

        self.assertEqual(signer.return_value, result)

    def get_config(self):
        config = MagicMock()
        config.sections.return_value = ['*.example.org']
        config.__getitem__.return_value = {
            'apiKey': 'KEY',
            'apiSecret': 'SECRET',
            'credentialScope': 'credential/scope',
        }

        return config


class TestSignRequest(TestCase):
    def setUp(self):
        self.signer = MagicMock()

        self.factory = MagicMock()
        self.factory.get_for_host.return_value = self.signer

        self.subject = SignRequest(self.factory)

    def test_it_adds_the_config_file_option_to_the_loader(self):
        loader = MagicMock()

        self.subject.load(loader)

        loader.add_option.assert_called_once_with(
            name='escher_config',
            typespec=str,
            default='',
            help='path to escher config file'
        )

    def test_it_does_nothing_if_no_config_set(self):
        self.subject.request(self.get_flow())

        self.signer.signRequest.assert_not_called()

    @patch('mitmproxy_escher.ctx')
    def test_it_does_nothing_if_no_signer_found(self, ctx):
        ctx.options.escher_config = '/path/to/config.ini'

        self.factory.get_for_host.return_value = None

        self.subject.configure({'escher_config'})
        self.subject.request(self.get_flow())

        self.signer.signRequest.assert_not_called()

    @patch('mitmproxy_escher.ctx')
    def test_it_signs_the_request(self, ctx):
        ctx.options.escher_config = '/path/to/config.ini'

        self.subject.configure({'escher_config'})
        self.subject.request(self.get_flow())

        self.signer.signRequest.assert_called_once_with('POST', '/path', 'body', {'Host': 'example.com'})

    @patch('mitmproxy_escher.ctx')
    def test_it_adds_the_extra_headers_to_the_request(self, ctx):
        ctx.options.escher_config = '/path/to/config.ini'
        self.signer.signRequest.return_value = {'X-Ems-Auth': 'test1', 'X-Ems-Date': 'test2'}

        flow = self.get_flow()

        self.subject.configure({'escher_config'})
        self.subject.request(flow)

        self.assertEqual('test1', flow.request.headers['X-Ems-Auth'])
        self.assertEqual('test2', flow.request.headers['X-Ems-Date'])

    def get_flow(self):
        flow = MagicMock()
        flow.request.method = 'POST'
        flow.request.host_header = 'example.com'
        flow.request.pretty_host = 'example.com'
        flow.request.path = '/path'
        flow.request.text = 'body'
        flow.request.headers = {'Host': 'example.com'}

        return flow
