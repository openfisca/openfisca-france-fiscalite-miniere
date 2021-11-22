# https://github.com/openfisca/openfisca-core/blob/34.7.7/openfisca_core/scripts/openfisca_command.py
# https://github.com/openfisca/openfisca-core/blob/34.7.7/openfisca_web_api/scripts/serve.py
# https://naysan.ca/2021/07/04/flask-101-serve-csv-files/
import os
import sys
from configparser import ConfigParser
from flask import abort, jsonify, make_response, request, send_file
from pandas import read_csv

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


        def handle_invalid_request(message):
            json_response = jsonify({
            'error': 'Invalid request: {}'.format(message),
                })
            abort(make_response(json_response, 400))


        @app.route('/calculate_matrice', methods=['POST'])
        def get_calculate_matrice():
            # Checking that the matrice parameter has been supplied
            if not "matrice" in request.args:
                handle_invalid_request("value for 'matrice' is missing")
            
            matrice = request.args["matrice"]
            if matrice != "1121" and matrice != "1122":
                handle_invalid_request("value for 'matrice' should be 1121 or 1122")

            config = ConfigParser()
            config.read("config.ini")
            
            if not {'fileA', 'fileE', 'fileT'}.issubset(request.files.keys()):
                handle_invalid_request("wrong arguments list. 3 files should be given as inputs: 'fileA' for activités/'fileE' for entreprises/'fileT' for titres")
                # TODO donner un exemple de solution
            
            fileT = request.files['fileT']
            print("fileT:", fileT)

            fileE = request.files['fileE']
            print("fileE:", fileE)

            fileA = request.files['fileA']
            print("fileA:", fileA)
            
            data_titres = read_csv(fileT)  # DataFrame
            data_entreprises = read_csv(fileE)
            data_activites = read_csv(fileA)

            # TODO appeler estime_taxes_redevances
            
            csv_dir  = os.path.abspath(config['SIMULATIONS']["OUTPUTS_DIRECTORY"])
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
