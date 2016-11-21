setup:
	pip3 install -r requirements.txt

test:
	python3 sdaas/manage.py test

style:
	find server tests -name \[a-zA-Z_]*.py -exec pep8 --ignore=E402 {} +
