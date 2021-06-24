
API_PORT=5000

all: test

uninstall:
	pip freeze | grep -v "^-e" | xargs pip uninstall -y

clean:
	rm -rf build dist
	find . -name '*.pyc' -exec rm \{\} \;

deps:
	pip install --upgrade pip twine wheel

install: deps
	@# Install OpenFisca-France-Fiscalite-Miniere for development.
	@# `make install` installs the editable version of OpenFisca-France.
	@# This allows contributors to test as they code.
	pip install --editable .[dev] --upgrade

install-prod:
	pip install openfisca-france-fiscalite-miniere

install-api: deps
	pip install openfisca-core[web-api]

build: clean deps
	@# Install OpenFisca-France-Fiscalite-Miniere for deployment and publishing.
	@# `make build` allows us to be be sure tests are run against the packaged version
	@# of OpenFisca-France-Fiscalite-Miniere, the same we put in the hands of users and reusers.
	python setup.py bdist_wheel
	find dist -name "*.whl" -exec pip install --upgrade --force-reinstall {}[dev] \;

check-syntax-errors:
	python -m compileall -q .

format-style:
	autopep8 `git ls-files | grep "\.py$$"`

check-style:
	flake8 `git ls-files | grep "\.py$$"`

check-types:
	mypy openfisca_france_fiscalite_miniere

test: clean check-syntax-errors check-style check-types
	openfisca test openfisca_france_fiscalite_miniere/tests --country-package openfisca_france_fiscalite_miniere

serve:
	openfisca serve --country-package openfisca_france_fiscalite_miniere -p ${API_PORT}
