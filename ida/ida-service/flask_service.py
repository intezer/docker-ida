import logging
import socket
import os

import pexpect
from flask import Flask, request, jsonify

logs_directory = '/shared/logs'
if not os.path.isdir(logs_directory):
    os.makedirs(logs_directory)
logging.basicConfig(level='INFO', format='%(asctime)s [%(levelname)s] %(message)s',
                    filename='%s/%s-ida-service.log' % (logs_directory, socket.gethostname()),
                    filemode='a')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

file_extenstions_to_clean = ['id0', 'id1', 'id2', 'idb', 'nam', 'til']


@app.errorhandler(Exception)
def on_error(exception):
    logger.error(exception)
    response = jsonify(error=exception)
    response.status_code = 500
    return response


def _extract_filename_from_command(command):
    split_command = command.split(' ')

    if '-A' not in split_command or split_command[-1] == '-A':
        return None

    return split_command[split_command.index('-A') + 1]


def _remove_ida_created_files(file_name):
    base_name = os.path.splitext(file_name)[0]
    for file_extension in file_extenstions_to_clean:
        file_to_remove = "%s.%s" % (base_name, file_extension)
        if os.path.isfile(file_to_remove):
            os.remove(file_to_remove)


@app.route('/ida/command', methods=['POST'])
def execute_command():
    logger.info('Got incoming request')
    if 'command' not in request.form:
        return jsonify(error="Missing parameter 'command'"), 422

    command = request.form['command']
    file_name = _extract_filename_from_command(command)
    if file_name is not None and not os.path.isfile(file_name):
        logger.warn("Couldn't find file %s", file_name)

    if not command.startswith('idal ') and not command.startswith('idal64 '):
        return jsonify(error="'idal' and 'idal64' are the only valid commands"), 422

    try:
        logger.info('Executing %s', command)
        timeout = None if 'timeout' not in request.form else int(request.form['timeout'])
        _, exit_code = pexpect.run(command, timeout=timeout, withexitstatus=True)
    except pexpect.TIMEOUT:
        return jsonify(error='request to ida timed out'), 408
    finally:
        if file_name is not None:
            _remove_ida_created_files(file_name)
            logger.info('Removed ida leftover files')

    if exit_code == 0:
        logger.info('Command %s finished executing successfully', command)
    else:
        logger.warn("Command %s didn't finish correctly, IDA returned exit code %s", command, exit_code)

    if exit_code != 0:
        return jsonify(error='ida finish with status code %s' % exit_code), 500
    else:
        return jsonify(message='OK'), 200


if __name__ == '__main__':
    app.run()
