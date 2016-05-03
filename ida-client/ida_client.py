# System imports
import itertools

# Third party imports
import requests


class Client:
    """
    Used for sending commands to one or more IDA containers over HTTP.
    """

    def __init__(self, urls):
        """
        >>> client = Client(['http://host-1:4001', 'http://host-2:4001'])
        :param urls: List of addresses of IDA containers including the published port
        """
        if urls is None or not any(urls):
            raise ValueError('Invalide "urls" value')
        self._urls = itertools.cycle(urls)

    def send_command(self, command, timeout=None) -> bool:
        """
        Send a command to an IDA container via HTTP
        :param command: The command to send, should start with idal or idal64
        :param timeout: A timeout given for the command (optional)
        :returns True if the command ran successfully, else false
        """
        data_to_send = dict(command=command)
        if timeout is not None:
            data_to_send['timeout'] = timeout

        response = requests.post('%s/ida/command' % next(self._urls), data=data_to_send)
        return response.status_code == 200

    def send_multiple_commands(self, commands, timeout=None):
        """
        Send a batch of commands to an IDA container via HTTP
        :param commands: An iterable of commands to send to the container
        :param timeout: A timeout given for the command (optional)
        :returns An array of booleans, one for each command, saying if the command succeeded or not
        """
        results = []
        for command in commands:
            results.append(self.send_command(command, timeout))

        return results
