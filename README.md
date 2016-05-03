# IDA in Docker
Run [IDA Pro by Hex Rays] (https://www.hex-rays.com/products/ida/) disassembler in [Docker] (https://www.docker.com/) containers.
Ideal for automating, scaling and distributing the use of IDAPython scripts to perform large-scale reverse engineering tasks.

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

    *Note: It is recommended to push the built image to a __private__ Docker Hub repository ([Pushing a repository to Docker Hub] (https://docs.docker.com/engine/userguide/containers/dockerrepos/#pushing-a-repository-to-docker-hub)). Otherwise you have to build the image on every machine*

## Start an IDA Service Container
IDA service container receives remote IDA commands over HTTP and executes them. To start a container, run this command:
```
$ sudo docker run -v <host_shared>:/shared -p <host_port>:4000 -it ida <cores>
```

- `<host_shared>` is a local directory on the host containing the files you want IDA to work with. Scripts, files to disassemble, etc.

   *Note: If you use [Docker Toolbox] (https://www.docker.com/products/docker-toolbox) on Windows, you might experience some issues parsing paths. Use `//` in the beginning of the paths (see [discussion on stackoverflow] (http://stackoverflow.com/questions/33312662/docker-toolbox-mount-file-on-windows#answers))*
- `<host_port>` is the port that the container᾿s HTTP interface is published to the host (see [Publish port] (https://docs.docker.com/engine/reference/commandline/run/#publish-or-expose-port-p-expose))
- `<cores>` is the number of IDA worker processes. This number should be up to 4 workers per core in the host. Default is 8.

*Note: In order to run multiple containers on the same host, publish each container to a different host port*

## Usage

Start two IDA containers as daemon:

```
$ sudo docker run -v ida-docker/example_volume:/shared -p 4001:4000 -d ida 4
$ sudo docker run -v ida-docker/example_volume:/shared -p 4002:4000 -d ida 4
```


Then install `ida_client`:

On **Windows**:
```
$ pip install "git+https://github.com/intezer/docker-ida#egg=ida_client&subdirectory=ida-client"
```

On **Linux/Mac OS X**:
```
$ pip install 'git+https://github.com/intezer/docker-ida#egg=ida_client&subdirectory=ida-client'
```

Then in python terminal:
```
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
>>> commands = ['idal -Sida_python_script.py -A %s' % file for file in files]
>>>
>>> client.send_multiple_commands(commands, timeout=600)
[True, True]
```

## Advanced Usage
- Add additional python libraries to the repository's `ida/requirements.txt` before building the image.

  The [Sark](https://github.com/tmr232/Sark) library is already installed for rapid IDAPython scripting.
- For IDA 64 bit files:

    ```
    >>> client.send_command('idal64 -Sida_python_script.py -A sample_x64.exe', timeout=600)
    True
    ```
- You can use any of the [IDA command line arguments](https://www.hex-rays.com/products/ida/support/idadoc/417.shtml) (except for GUI-related switches)

## Notes
Tested with IDA 6.9
