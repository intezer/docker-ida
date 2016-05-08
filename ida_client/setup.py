from setuptools import setup

setup(name='ida_client',
      version='0.1',
      description='Sends commands IDA containers over HTTP',
      url='https://github.com/intezer/docker-ida',
      author='Intezer',
      author_email='info@intezer.com',
      py_modules=['ida_client'],
      zip_safe=False,
      install_requires=['requests'])
