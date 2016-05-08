import logging
import socket

import pexpect
from flask import Flask, request, jsonify

logging.basicConfig(level='INFO', format='%(asctime)s [%(levelname)s] %(message)s',
                    filename='/shared/%s-ida-service.log' % socket.gethostname(),
                    filemode='w+')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


@app.errorhandler(Exception)
def on_error(exception):
    logger.error(exception)
    response = jsonify(error=exception)
    response.status_code = 500
    return response


@app.route('/ida/command', methods=['POST'])
def execute_command():
    logger.info('Got incoming request')
    if 'command' not in request.form:
        return jsonify(error="Missing parameter 'command'"), 422

    command = request.form['command']
    if not command.startswith('idal ') and not command.startswith('idal64 '):
        return jsonify(error="'idal' and 'idal64' are the only valid commands"), 422

    try:
        logger.info('Executing %s', command)
        timeout = None if 'timeout' not in request.form else int(request.form['timeout'])
        _, exit_code = pexpect.run(command, timeout=timeout, withexitstatus=True)
    except pexpect.TIMEOUT:
        return jsonify(error='request to ida timed out'), 408
    logger.info('Finish executing command with status %s', exit_code)
    if exit_code != 0:
        return jsonify(error='ida finish with status code %s' % exit_code), 500
    else:
        return jsonify(message='OK'), 200


if __name__ == '__main__':
    app.run()
