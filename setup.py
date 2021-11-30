from setuptools import find_packages, setup

setup(
    name="OpenFisca-France-Fiscalite-Miniere",
    version="1.2.0",
    author="OpenFisca Team",
    author_email = "contact@openfisca.fr",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: Information Analysis",
        ],
    description="French mining tax system for OpenFisca",
    keywords = 'benefit microsimulation social tax',
    license="http://www.fsf.org/licensing/licenses/agpl-3.0.html",
    url = "https://github.com/openfisca/openfisca-france-fiscalite-miniere",
    include_package_data = True,  # Will read MANIFEST.in
    data_files = [
        (
            "share/openfisca/openfisca-france-fiscalite-miniere",
            ["CHANGELOG.md", "LICENSE", "README.md"],
            ),
        ],
    install_requires = [
        "OpenFisca-Core[web-api] >= 34.0.0, < 35.0.0",
        ],
    extras_require = {
        "dev": [
            "autopep8 >= 1.5.0, < 1.6.0",
            "flake8 >= 3.7.0, < 3.8.0",
            "flake8-print",
            "flake8-2020",
            "flake8-aaa",
            "flake8-annotations-complexity",
            "flake8-broken-line",
            "flake8-bugbear",
            "flake8-builtins",
            "flake8-comprehensions",
            "flake8-debugger",
            "flake8-eradicate",
            "flake8-executable",
            "flake8-import-order",
            "flake8-logging-format",
            "flake8-mutable",
            "flake8-pep3101",
            "flake8-polyfill",
            "flake8-print",
            "flake8-pyi",
            "flake8-rst-docstrings",
            "flake8-string-format",
            "flake8-tidy-imports",
            'mypy >= 0.700, < 0.800',
            "pytest >= 5.0.0, < 6.0.0",
            ]
        },
    packages=find_packages(exclude = [
        "openfisca_france_fiscalite_miniere.tests*",
        ]),
    )
