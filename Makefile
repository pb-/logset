test:
	pipenv run flake8
	pipenv run py.test -v
.PHONY: test
