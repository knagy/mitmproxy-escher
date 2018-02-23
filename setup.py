from setuptools import setup

setup(
    name='mitmproxy-escher',
    description='Sign mitmproxy requests with Escher',
    version='0.1.2',
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
        'mitmproxy>=2.0,<3.0',
    ],
    zip_safe=True,
)
