from setuptools import setup
import pip.download
from pip.req import parse_requirements

install_requires = [str(ir.req) for ir in parse_requirements('requirements.txt', session=pip.download.PipSession())]

setup(name='ida_client',
      version='0.1',
      description='Sends commands IDA containers over HTTP',
      url='https://github.com/intezer/docker-ida',
      author='Intezer',
      author_email='info@intezer.com',
      py_modules=['ida_client'],
      zip_safe=False,
      install_requires=install_requires)
