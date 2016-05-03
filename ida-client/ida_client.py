# System imports
import itertools

# Third party imports
import requests


class Client:
    """
    This class is used to communicate with a container of IDA via HTTP
    """

    def __init__(self, urls):
        """
        :param urls: The addresses of the containers hosts with the port used to publish the container
        e.g: [http://host-1:4001, http://host-2:4001]
        """
        if urls is None or not any(urls):
            raise Exception('Cannot create IdaClient with no urls')
        self._urls = itertools.cycle(urls)

    def send_command(self, command, timeout=None) -> bool:
        """
        Send a command to an IDA container via HTTP
        :param command: The command to send, should start with idal or idal64
        :param timeout: A timeout given for the command (optional)
        :returns True if the command ran successfully, else false
        """
        res = requests.post('%s/ida/command' % next(self._urls), data=dict(command=command, timeout=timeout))
        return res.status_code == 200

    def execute_multiple_command(self, commands, timeout=None):
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
