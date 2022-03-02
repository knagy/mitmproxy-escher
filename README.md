# mitmproxy-escher

Sign [mitmproxy](https://mitmproxy.org/) requests with [Escher](https://escherauth.io/).

![Screenshot](screenshot.png?raw=true)

## Installation

```
pip3 install mitmproxy-escher
```

Note: this module does not work with mitmproxy's pre-built self-contained binaries.

## Configuration

Required parameters are apiKey, apiSecret and credentialScope. Section names can contain wildcard characters.

```
[*.example.org]
apiKey=KEY
apiSecret=SECRET
credentialScope=credential/scope
hashAlgo=SHA256
algoPrefix=EMS
vendorKey=EMS
authHeaderName=X-EMS-Auth
dateHeaderName=X-EMS-Date
```

## Usage

Start `mitmproxy` with the addon:

```
mitmproxy -s "$(python3 -m mitmproxy_escher)" --set escher_config=/path/to/config.ini
```

Make requests through the proxy:

```
curl -k -x localhost:8080 https://httpbin.org/headers
```
