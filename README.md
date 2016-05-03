# IDA in Docker
Build and run [IDA Pro by Hex Rays] (https://www.hex-rays.com/products/ida/) disassembler in [Docker] (https://www.docker.com/) containers.
Ideal for automating, scaling and distributing the use of IDAPython scripts.

## Requirements
- Machine with Docker installed. [Install Docker] (https://docs.docker.com/engine/installation/)
- IDA Pro Linux version installation file (.run) and valid password. [Get IDA Pro] (https://www.hex-rays.com/products/ida/)

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

    *Note: It is recommended to push the built image to a __private__ Docker Hub repository. [Pushing a repository to Docker Hub] (https://docs.docker.com/engine/userguide/containers/dockerrepos/#pushing-a-repository-to-docker-hub)*

## Start an IDA Service Container
IDA service container receives remote IDA commands over HTTP and executes them. To start a container, run this command:
```
$ sudo docker run -v <host_shared>:/shared -p <host_port>:4000 ida ida-service <cores>
```

- `<host_shared>` is a local directory on the host containing the files you want IDA to work with. Scripts, files to disassemble, etc.
- `<host_port>` is the port that the container᾿s HTTP interface is published to the host (see [Publish port] (https://docs.docker.com/engine/reference/commandline/run/#publish-or-expose-port-p-expose))
- `<cores>` is the number of IDA worker processes. This number should be up to 4 workers per core in the host. Default is 8.

*Note: To run multiple containers on the same host publish each container to a different host port*

## Usage
Let's assume we started 2 IDA containers, on `host-1` and `host-2` both published to port 4000.

We can access them from any machine using the `ida_client` python module:
```
$ pip install git+https://github.com/intezer/docker-ida#egg=ida_client&subdirectory=ida-client
```

Then:
```
>>> import ida_client
>>>
>>> client = ida_client.Client(['host-1:4000', 'host-2:4000'])
>>> 
>>> client.send_command('idal -Sida_python_script.py -A sample.exe', timeout=600)
True
>>>
>>> files = ['sample_a.exe', 'sample_b.exe', 'sample_c.exe']
>>>
>>> # Building list of commands to send at once
>>> commands = ['idal -Sida_python_script.py -A {}'.format(file) for file in files]
>>>
>>> client.send_multiple_commands(commands, timeout=600)
[True, True, True]
```

The sent commands will be executed on the IDA service containers.

## Advanced Usage
- Add additional python libraries to the repository's `ida/requirements.txt` before building the image
- For IDA 64 bit files:

    ```
    >>> client.send_command('idal64 -Sida_python_script.py -A sample_x64.exe', timeout=600)
    True
    ```
- You can use any of the [IDA command line arguments](https://www.hex-rays.com/products/ida/support/idadoc/417.shtml) (except for GUI-related switches)

## Notes
Tested with IDA 6.9
