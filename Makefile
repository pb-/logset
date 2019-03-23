develop:
	FLASK_APP=logset.server FLASK_ENV=development LOGSET_STORE=data pipenv run flask run
.PHONY: develop

test:
	FLASK_DEBUG=1 FLASK_TESTING=1 LOGSET_STORE=$(shell mktemp -d /tmp/logset-test-XXXXXXX) pipenv run py.test -v
.PHONY: test
