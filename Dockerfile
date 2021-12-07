FROM python:3.7

RUN pip install --upgrade pip
WORKDIR /app
COPY Makefile /app/Makefile
RUN make install-prod
RUN make install-api


CMD ["openfisca", "serve", "--country-package", "openfisca_france_fiscalite_miniere", "--bind", "0.0.0.0"]
