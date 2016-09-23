setup:
	pip3 install -r requirements.txt
	pip3 install coverage
	pip3 install pytest
	pip3 install pep8
	python3 setup.py install

test:
	pytest tests

style:
	find ./server -name \*.py -exec pep8 {} +

coverage:
	coverage run server
	coverage report
