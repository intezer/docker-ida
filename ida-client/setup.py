from setuptools import setup
import pip.download
from pip.req import parse_requirements

install_requires = [str(ir.req) for ir in parse_requirements('requirements.txt', session=pip.download.PipSession())]

setup(name='ida_client',
      version='0.1',
      description='Communicate with an IDA container via HTTP',
      url='https://github.com/Intezer/docker-ida',
      author='Intezer',
      author_email='info@intezer.com',
      packages=['ida_client'],
      zip_safe=False,
      install_requires=install_requires)
