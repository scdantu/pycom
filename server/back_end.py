import os
import logging
from logging.handlers import TimedRotatingFileHandler
from concurrent.futures import ThreadPoolExecutor

from ipwhois import IPWhois, BaseIpwhoisException
from dns.resolver import NoResolverConfiguration

import flask
from flask_caching import Cache
from flask_parameter_validation import ValidateParameters, Query

from pycom import PyCom, ProteinParams
from pycom.interface import _find_helper  # noqa
from pycom.selector import MatrixFormat
from pycom.sql.constraints_utils import to_bool, to_int

config = {
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300
}

app = flask.Flask(__name__)

app.config.from_mapping(config)
app.json.sort_keys = False
app.json.compact = False

# set up caching
cache = Cache(app)
_find_helper.query_db = cache.memoize(cache_none=True)(_find_helper.query_db)

pycom_db_path = os.environ.get('PYCOM_DB_PATH', '~/docs/pycom.db')
pycom_mat_path = os.environ.get('PYCOM_MAT_PATH', '~/docs/pycom.mat')

pyc = PyCom(db_path=pycom_db_path, mat_path=pycom_mat_path)
valid_protein_params = set(ProteinParams)

# set up logging
log_executors = ThreadPoolExecutor(max_workers=1)

log_dir = os.path.expanduser(os.environ.get('PYCOM_LOG_DIR', '~/docs/logs'))
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_formatter = logging.Formatter('%(asctime)s - %(message)s')
log_handler = TimedRotatingFileHandler(os.path.join(log_dir, 'pycom.log'), when='midnight', backupCount=356*2)
log_handler.setFormatter(log_formatter)
log_handler.suffix = '%Y%m%d'
logger = logging.getLogger('pycom')
logger.addHandler(log_handler)
logger.setLevel(logging.INFO)


def _log_handler(ip, message):
    try:
        ip_info = IPWhois(ip).lookup_rdap()
        country = ip_info.get('network', {}).get('country', None)
        name = ip_info.get('network', {}).get('name', None)
        asn = ip_info.get('asn_description', None)
    except (BaseIpwhoisException, NoResolverConfiguration, ValueError):
        country = None
        name = None
        asn = None

    logger.info(f'{ip} - {country} - {name} - {asn} - {message}')


def log_request():
    """
    This function logs the request parameters and JSON message body, if present.
    These are compressed into one dictionary and logged as a single message.
    """
    parameters = flask.request.args.to_dict()
    json_body = flask.request.get_json(force=True, silent=True)
    if json_body is None:
        json_body = {}

    log_data = {**parameters, **json_body}
    endpoint = flask.request.path
    ip = _get_client_ip(flask.request)

    log_executors.submit(_log_handler, ip, f'{endpoint} - {log_data}')


def _get_client_ip(request):
    """
    This function returns the client IP address, if available.
    The following NGINX configuration should be used:
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_set_header X-Forwarded-Protocol https;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_redirect off;
    """
    if request.access_route:
        return request.access_route[-1]
    else:
        return None


@app.route('/api/', methods=['GET'])
def landing():
    raise AssertionError('/api is not an endpoint. Try /api/find, /api/get-disease-list, '
                         '/api/get-cofactor-list, /api/get-organism-list, /api/get-biological-process-list, '
                         '/api/get-cellular-component-list, /api/get-development-stage-list, /api/get-domain-list, '
                         '/api/get-ligand-list, /api/get-molecular-function-list, /api/get-ptm-list')


@app.route('/api/find', methods=['GET'])
@ValidateParameters()
def find(
        # Search parameters:
        # uniprot_id, sequence, min_length, max_length, min_helix, max_helix, min_turn, max_turn, min_strand,
        # max_strand, organism_id, organism, cath, enzyme, has_substrate, has_ptm, has_pdb, disease, disease_id,
        # has_disease, cofactor, cofactor_id, has_cofactor, biological_process, cellular_component,
        # developmental_stage, domain, ligand, molecular_function, ptm

        # Output parameters:
        # matrix, page, per_page
        page: int = Query(1),
        per_page: int = Query(default=10, min_int=1, max_int=100)
):
    log_request()
    data = flask.request.args.to_dict()

    if flask.request.data not in {b'', None}:
        data_json = flask.request.get_json(force=True, silent=True)
        assert data_json is not None, 'Invalid JSON body'
        data.update(data_json)

    # parse parameters
    load_matrices = to_bool(data.pop('matrix', False), entry='matrix parameter')
    page = to_int(data.pop('page', page), entry='page parameter')
    per_page = to_int(data.pop('per_page', per_page), entry='per_page parameter')

    # validate that no invalid parameters are passed
    invalid_params = set(data) - valid_protein_params
    assert not invalid_params, f'Invalid parameters: {", ".join(invalid_params)}'

    if load_matrices:
        assert per_page <= 10, 'per_page cannot be larger than 10 when loading matrices'

    # Request validated, now build the response #

    entries = pyc.find(data)  # find entries matching the constraints
    selection = pyc.paginate(entries, page=page, per_page=per_page)

    if load_matrices:
        selection = pyc.load_matrices(selection, mat_format=MatrixFormat.JSON)
    else:
        selection = selection.drop(columns=['matrix'])

    if load_matrices:
        app.json.compact = True

    response = flask.jsonify({
        'results': selection.to_dict(orient='records'),
        'page': page,
        'total_pages': len(entries) // per_page + 1,
        'result_count': len(entries),
        'showing': f'{(page - 1) * per_page + 1}-{min(page * per_page, len(entries))}'
    })

    if load_matrices:
        app.json.compact = False

    return response


@app.route('/api/get-disease-list', methods=['GET'])
def get_disease_list():
    """
    Get list of diseases

    :return: list of diseases
    """
    diseases = pyc.get_disease_list()
    return flask.jsonify(diseases.to_dict(orient='records'))


@app.route('/api/get-cofactor-list', methods=['GET'])
def get_cofactor_list():
    """
    Get list of cofactors

    :return: list of cofactors
    """
    cofactors = pyc.get_cofactor_list()
    return flask.jsonify(cofactors.to_dict(orient='records'))


@app.route('/api/get-organism-list', methods=['GET'])
def get_organism_list():
    """
    Get list of organisms

    :return: list of organisms
    """
    organisms = pyc.get_organism_list()
    return flask.jsonify(organisms.to_dict(orient='records'))


@app.route('/api/get-biological-process-list', methods=['GET'])
def get_biological_process_list():
    """
    Get list of biological processes

    :return: list of biological processes
    """
    biological_processes = pyc.get_biological_process_list()
    return flask.jsonify(biological_processes.to_dict(orient='records'))


@app.route('/api/get-cellular-component-list', methods=['GET'])
def get_cellular_component_list():
    """
    Get list of cellular components

    :return: list of cellular components
    """
    cellular_components = pyc.get_cellular_component_list()
    return flask.jsonify(cellular_components.to_dict(orient='records'))


@app.route('/api/get-development-stage-list', methods=['GET'])
def get_development_stage_list():
    """
    Get list of development stages

    :return: list of development stages
    """
    development_stages = pyc.get_developmental_stage_list()
    return flask.jsonify(development_stages.to_dict(orient='records'))


@app.route('/api/get-domain-list', methods=['GET'])
def get_domain_list():
    """
    Get list of domains

    :return: list of domains
    """
    domains = pyc.get_domain_list()
    return flask.jsonify(domains.to_dict(orient='records'))


@app.route('/api/get-ligand-list', methods=['GET'])
def get_ligand_list():
    """
    Get list of ligands

    :return: list of ligands
    """
    ligands = pyc.get_ligand_list()
    return flask.jsonify(ligands.to_dict(orient='records'))


@app.route('/api/get-molecular-function-list', methods=['GET'])
def get_molecular_function_list():
    """
    Get list of molecular functions

    :return: list of molecular functions
    """
    molecular_functions = pyc.get_molecular_function_list()
    return flask.jsonify(molecular_functions.to_dict(orient='records'))


@app.route('/api/get-ptm-list', methods=['GET'])
def get_ptm_list():
    """
    Get list of PTMs

    :return: list of PTMs
    """
    ptms = pyc.get_ptm_list()
    return flask.jsonify(ptms.to_dict(orient='records'))


@app.errorhandler(AssertionError)
def handle_assertion_error(error):
    """Catch assertion errors and return them as JSON,
    with a 400 status code and a link to the documentation."""
    return flask.jsonify({
        'message': str(error),
        'documentation': 'https://pycom.brunel.ac.uk/api/spec/'
    }), 400


@app.errorhandler(404)
def handle_404(_):
    """Catch 404 errors and return them as JSON,
    with a 404 status code and a link to the documentation."""
    return flask.jsonify({
        'message': 'The requested API endpoint does not exist. The main endpoint is '
                   'https://pycom.brunel.ac.uk/api/find. For more information, see the documentation.',
        'documentation': 'https://pycom.brunel.ac.uk/api/spec/'
    }), 404


if __name__ == '__main__':
    app.run(debug=True, port=5351)
