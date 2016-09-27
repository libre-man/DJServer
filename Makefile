setup:
	pip3 install -r requirements.txt
	python3 setup.py install

test:
	pytest -v --showlocals tests

style:
	find server tests -name \[a-zA-Z_]*.py -exec pep8 --ignore=E402 {} +

coverage:
	pytest -v --cov-config=.coveragerc --cov=server tests/
