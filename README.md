# Docker IDA
Run [IDA Pro by Hex Rays](https://www.hex-rays.com/products/ida/) disassembler in [Docker](https://www.docker.com/) containers.
Ideal for automating, scaling and distributing the use of IDAPython scripts to perform large-scale reverse engineering tasks.


![alt tag](https://raw.githubusercontent.com/intezer/docker-ida/master/media/docker-ida.png)

Our blog: http://www.intezer.com/blog/

## Requirements
- Machine with Docker installed. [Install Docker](https://docs.docker.com/engine/installation/)
- IDA Pro Linux version installation file (.run) and a valid license for running multiple instances. [Get IDA Pro](https://www.hex-rays.com/products/ida/)

## Installation
1. Clone `docker-ida` repository:

    ```
    $ git clone https://github.com/intezer/docker-ida
    ```

2. Copy IDA Pro installation file to the repository's `ida` directory:

    ```
    $ cp <ida-installation-file-path> docker-ida/ida/ida.run
    ```

3. Build IDA docker image:

    ```
    $ sudo docker build -t ida --build-arg IDA_PASSWORD=<password> docker-ida/ida
    ```

    *Note: It is recommended to push the built image to a __private__ Docker Hub repository ([Pushing a repository to Docker Hub](https://docs.docker.com/engine/userguide/containers/dockerrepos/#pushing-a-repository-to-docker-hub)). Otherwise you have to build the image on every machine*

## Start an IDA Service Container
IDA service container receives remote IDA commands over HTTP and executes them. To start a container, run this command:
```
$ sudo docker run -v <host_shared>:/shared -p <host_port>:4000 -it ida -c <cores> -t <timeout>
```

- `<host_shared>` is a local directory on the host containing the files you want IDA to work with. Scripts, files to disassemble, etc.

   *Note: If you use [Docker Toolbox](https://www.docker.com/products/docker-toolbox) on Windows, you might experience some issues parsing paths. Use `//` in the beginning of the paths (see [discussion on stackoverflow](http://stackoverflow.com/questions/33312662/docker-toolbox-mount-file-on-windows#answers))*
- `<host_port>` is the port you tell the host you would like to use to connect to the specific docker container. (see [Publish port](https://docs.docker.com/engine/reference/commandline/run/#publish-or-expose-port-p-expose))
- `<cores>` is the number of IDA worker processes. This number should be up to 4 workers per core in the host. Default is 8.
- `<timeout>` is the server timeout for each request. Default is 30.

*Note: In order to run multiple containers on the same host, publish each container to a different host port*

## Usage

**On The server:**

- Start two IDA containers as daemon:

    ```
    $ sudo docker run -v /path/to/current/folder/docker-ida/example_volume:/shared -p 4001:4000 -d ida -c 4
    $ sudo docker run -v /path/to/current/folder/docker-ida/example_volume:/shared -p 4002:4000 -d ida -c 4
    ```

**On The client:**

2. Install `ida_client` Python library:

    On Windows:
    ```
    $ pip install "git+https://github.com/intezer/docker-ida#egg=ida_client&subdirectory=ida_client"
    ```

    On Linux / Mac OS X:
    ```
    $ pip install 'git+https://github.com/intezer/docker-ida#egg=ida_client&subdirectory=ida_client'
    ```
    *Note: pip version must be 8.1.1 or higher*

3. Send commands to the containers using the Python library:
    ```python
    >>> import ida_client
    >>>
    >>> client = ida_client.Client(['http://localhost:4001', 'http://localhost:4002'])
    >>>
    >>> client.send_command('idal -Sextract_file_functions.py -A zlib.dll.sample', timeout=600)
    True
    >>>
    >>> files = ['zlib.dll.sample', 'Win32OpenSSL.sample']
    >>>
    >>> # Building list of commands to send at once
    >>> commands = ['idal -Sextract_file_functions.py -A %s' % file for file in files]
    >>>
    >>> client.send_multiple_commands(commands, timeout=600)
    [True, True]
    ```

## Advanced Usage
- Add additional python libraries to the repository's `ida/requirements.txt` before building the image.

  The [Sark](https://github.com/tmr232/Sark) library is already installed for rapid IDAPython scripting.
- For IDA 64 bit files:

    ```python
    >>> client.send_command('idal64 -Sida_python_script.py -A sample_x64.exe', timeout=600)
    True
    ```
- You can use any of the [IDA command line arguments](https://www.hex-rays.com/products/ida/support/idadoc/417.shtml) (except for GUI-related switches)

## Troubleshooting
If the script doesn't run correctly:
- Examine the log files in the volume `<host_shared>/logs/`. Each container has a different log file named `<container-name>-ida-service.log`
- Make sure the IDAPython script is Python 2.7 compatible, Python 3.x is not supported in IDAPython.
- Make sure to add Python libraries to the `requirements.txt` **before** building the docker image. When `requirements.txt` changes, the docker image and containers can always be rebuilt.
- Make sure the paths to the IDAPython scripts and files to disassemble in the send command are relative to the `<host_shared>` volume.

## Notes
- Tested with IDA 6.9
- You are required to read the [IDA License Agreement](https://www.hex-rays.com/products/ida/ida_eula.pdf) prior to using this project.
- More information on our blog post: http://blog.intezer.com/docker-ida
