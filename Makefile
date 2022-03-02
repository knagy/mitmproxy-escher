venv:
	python3 -m venv venv

install:
ifndef VIRTUAL_ENV
	@echo 'Please activate the virtual environment'
else
	python -m pip install --upgrade pip
	pip install -r requirements.txt -r requirements-dev.txt
endif

test:
ifndef VIRTUAL_ENV
	@echo 'Please activate the virtual environment'
else
	python -m unittest discover
endif

codestyle:
ifndef VIRTUAL_ENV
	@echo 'Please activate the virtual environment'
else
	pycodestyle mitmproxy_escher
endif
