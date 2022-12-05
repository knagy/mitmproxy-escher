from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / 'README.md').read_text()

setup(
    name='mitmproxy-escher',
    description='Sign mitmproxy requests with Escher',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='3.0.0',
    url='https://github.com/knagy/mitmproxy-escher',
    author='Nagy Krisztián',
    author_email='knagy@deadlime.hu',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Security',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: Proxy Servers',
    ],
    packages=[
        'mitmproxy_escher',
    ],
    install_requires=[
        'escherauth-go>=0.1,<1.0',
        'mitmproxy>=9.0.0,<10.0.0',
    ],
    zip_safe=True,
)
