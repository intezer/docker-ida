import pexpect
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


@app.errorhandler(Exception)
def on_error(exception):
    print(exception)
    response = jsonify(error=exception)
    response.status_code = 500
    return response


@app.route('/ida/command', methods=['POST'])
def execute_command():
    print('Got incoming request')
    if 'command' not in request.form:
        return jsonify(error="Missing parameter 'command'"), 422

    command = request.form['command']
    if not command.startswith('idal ') and not command.startswith('idal64 '):
        return jsonify(error="'command' should start with 'idal' or 'idal64"), 422

    try:
        print('Executing %s' % command)
        _, exit_code = pexpect.run(command, timeout=request.form.get('timeout'), withexitstatus=True)
    except pexpect.TIMEOUT:
        return jsonify(error='Timeout executing the command'), 408
    
    print('Finish executing command with status %s' % exit_code)
    
    if exit_code != 0:
        return jsonify(error='Command finished with status code %s' % exit_code,status_code=500)
    else:
        return jsonify(message='OK', status_code=200)

if __name__ == '__main__':
    app.run()
