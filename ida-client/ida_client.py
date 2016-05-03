# System imports
import itertools

# Third party imports
import requests


class IdaClient:
    def __init__(self, urls):
        if urls is None or not any(urls):
            raise Exception('Cannot create IdaClient with no urls')
        self._urls = itertools.cycle(urls)

    def send_command(self, command, timeout=None) -> bool:
        res = requests.post('%s/ida/command' % self._urls.__next__(), data=dict(command=command, timeout=timeout))
        return res.status_code == 200

    def execute_multiple_command(self, commands, timeout=None):
        results = []
        for command in commands:
            results.append(self.send_command(command, timeout))

        return results
