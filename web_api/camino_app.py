# https://github.com/openfisca/openfisca-core/blob/34.7.7/openfisca_core/scripts/openfisca_command.py
# https://github.com/openfisca/openfisca-core/blob/34.7.7/openfisca_web_api/scripts/serve.py
# https://naysan.ca/2021/07/04/flask-101-serve-csv-files/
import os
import sys
from configparser import ConfigParser
from flask import jsonify, request, send_file

from openfisca_core.scripts import build_tax_benefit_system
from openfisca_core.scripts.openfisca_command import get_parser

from openfisca_web_api.app import create_app
from openfisca_web_api.scripts.serve import read_user_configuration
from openfisca_web_api.errors import handle_import_error

try:
    from gunicorn.app.base import BaseApplication
    from gunicorn import config
except ImportError as error:
    handle_import_error(error)


DEFAULT_PORT = '5000'
HOST = '127.0.0.1'
DEFAULT_WORKERS_NUMBER = '3'
DEFAULT_TIMEOUT = 120


class OpenFiscaWebAPIApplication(BaseApplication):

    def __init__(self, options):
        self.options = options
        super(OpenFiscaWebAPIApplication, self).__init__()

    def load_config(self):
        for key, value in self.options.items():
            if key in self.cfg.settings:
                self.cfg.set(key.lower(), value)

    def load(self):
        tax_benefit_system = build_tax_benefit_system(
            self.options.get('country_package'),
            self.options.get('extensions'),
            self.options.get('reforms')
            )
        app = create_app(
            tax_benefit_system,
            self.options.get('tracker_url'),
            self.options.get('tracker_idsite'),
            self.options.get('tracker_token'),
            self.options.get('welcome_message')
            )

        DEFAULT_WELCOME_MESSAGE = "hello"
        welcome_message = None

        @app.route('/calculate_matrice')
        def get_calculate_matrice():
            # Checking that the month parameter has been supplied
            if not "matrice" in request.args:
                return "ERROR: value for 'matrice' is missing"
            # Also make sure that the value provided is numeric
            try:
                matrice = int(request.args["matrice"])
            except:
                return "ERROR: value for 'matrice' should be between 1000 and 9999"

            config = ConfigParser()
            config.read("config.ini")
            csv_dir  = os.path.abspath(config['SIMULATIONS']["OUTPUTS_DIRECTORY"])
            # csv_file = "2019_%02d_weather.csv" % matrice
            csv_file = "matrice_drfip_guyane_production_2019_20201216-224144.csv"
            csv_path = os.path.join(csv_dir, csv_file)
    
            # Also make sure the requested csv file does exist
            if not os.path.isfile(csv_path):
                return "ERROR: file %s was not found on the server" % csv_path
            # Send the file back to the client
            return send_file(csv_path, as_attachment=True, attachment_filename=csv_file)

        return app

def main(parser):
    configuration = {
        'port': DEFAULT_PORT,
        'bind': '{}:{}'.format(HOST, DEFAULT_PORT),
        'workers': DEFAULT_WORKERS_NUMBER,
        'timeout': DEFAULT_TIMEOUT,
        }
    configuration = read_user_configuration(configuration, parser)
    OpenFiscaWebAPIApplication(configuration).run()


def run():
    parser = get_parser()
    sys.exit(main(parser))

if __name__ == '__main__':
    run()