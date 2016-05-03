# IDA in Docker
Build and run [IDA Pro by Hex Rays] (https://www.hex-rays.com/products/ida/) disassembler in [Docker] (https://www.docker.com/) container.
Especially suitable for automating, scaling and distributing the use of IDAPython scripts.

## Requirements
- Machine with Docker installed. [Install Docker] (https://docs.docker.com/engine/installation/)
- IDA Pro Linux version installation file (.run) and valid password. [Get IDA Pro] (https://www.hex-rays.com/products/ida/)

## Installation
1. Clone docker-ida repository :

    ```
    $ git clone https://github.com/intezer/docker-ida 
    ```

2. Copy IDA Pro installation file to the `ida` folder:

    ```
    $ cp <ida-installation-path>/.run docker-ida/ida/ida.run
    ```

3. Build IDA image:

    ```
    $ docker build -t ida --build-arg IDA_PASSWORD=<password> docker-ida/ida
    ```

    *Note: It is recommended to push the built image to a **private** Docker Hub repository. [Pushing a repository to Docker Hub] (https://docs.docker.com/engine/userguide/containers/dockerrepos/#pushing-a-repository-to-docker-hub)*

## Start an IDA Service Instance
```
docker run -v <host_shared>:/shared -p <host_port>:4000 ida-service <cores>
```

`<host_shared>` is a local directory containing the files you want IDA to work with (scripts, files to disassemble, ect.).
`<host_port>` is the port that the container᾿s http interface is published to the host. ???
`<cores>` is the number of cores this IDA instance will work with, by default is set to 4. *It is recommended to use max number as the number of cores on the machine.*

*Note: To run multiple containers on the same host publish each container to a different host port*

*Note: If you wish to create several containers on the same machine, you need to give each instance a different port and use cores responsibly*


Here we're using [docker data volumes] (https://docs.docker.com/engine/userguide/containers/dockervolumes/) in order to share files and scripts with the docker container and get results back



---


# IDA in Docker
Build and run [IDA Pro by Hex Rays] (https://www.hex-rays.com/products/ida/) disassembler in [Docker] (https://www.docker.com/) container.
Especially suitable for automating the use of IDAPython scripts and batch analysis.

[//]: # (i fill this is not nececery)
This docker image is configured to have everything you need for a working IDA machine, ready to run scripts:
* IDA Pro (Linux version) automatically installed with all its dependencies
* pip install - Easily install external python libraries that integrate into the IDAPython engine
* [Sark](https://github.com/tmr232/Sark) - The excellent library by Tamir Bahar is preinstalled, to simplify IDAPython scripting
* Special wrapper script in order to quickly run IDA without ANY screen output

## Requirements
IDA Pro Linux version installation file (.run) and valid password. [Get IDA Pro] (https://www.hex-rays.com/products/ida/)
Docker installed. [Install Docker] (https://docs.docker.com/engine/installation/)

## Setup
* Clone docker-ida `git clone https://github.com/Intezer/docker-ida`
* Copy IDA Pro installation file `cp <ida-installation-path>/.run docker-ida/ida/ida.run`
* Build ida image `docker build -t ida --build-arg password=<password> docker-ida/ida`

## Simple Usage
Running the IDAPython script "examples/export_functions.py" on the file "file_to_reverse.exe":
`cp <path>/file_to_reverse.exe .` copy the file y
`docker run -v $PWD:/shared -w /shared ida idal.py -Sexamples/export_functions.py -A file_to_reverse.exe`
`cat functions.txt`
Here we're using [docker data volumes] (https://docs.docker.com/engine/userguide/containers/dockervolumes/) in order to share files and scripts with the docker container and get results back from the docker container.

## Advanced Usage
For IDA 64 bit files:
```
docker run -it -v "$PWD":/project -w /project ida idal64.py -Sexamples/hello.py -A file_to_reverse.exe
```

You can use any of the [IDA command line arguments](https://www.hex-rays.com/products/ida/support/idadoc/417.shtml), except for GUI-related switches:
```
docker run -it -v "$PWD":/project -w /project ida idal.py [arg1] [arg2] [arg3]
```

You could also run IDA in the awful TVision terminal-GUI mode if you really want to.  Just open a shell using:
```
docker run -it -v "$PWD":/project -w /project ida bash
```
And run the regular IDA binary (idal or idal64), it's already in the PATH:
```
idal arg1 arg2...
idal64 arg1 arg2...
```

## Installing external libraries
Just add the library you wish to the "requirements.txt" file before you build the Dockerfile

## IDA-Dockerized in Windows
In Windows, docker has its problems parsing paths, so you'll need to add some '/' like this:
```
docker run -it -v "/$PWD":/project -w //project ida idal.py -Sexamples/hello.py -A file_to_reverse.exe
```
Or for 64 bit files:
```
docker run -it -v "/$PWD":/project -w //project ida idal64.py -Sexamples/hello.py -A file_to_reverse.exe
```

## Notes
Tested only with IDA 6.9, but should work with some previous versions as well



# ===================================

# IDA in Docker
Everything you need to build and run [IDA Pro by Hex Rays] (https://www.hex-rays.com/products/ida/) in [Docker] (https://www.docker.com/).
Especially suitable for automating the use of IDAPython scripts and batch analysis.

This docker image is configured to have everything you need for a working IDA machine, ready to run scripts:
* IDA Pro (Linux version) automatically installed with all its dependencies
* pip install - Easily install external python libraries that integrate into the IDAPython engine
* [Sark](https://github.com/tmr232/Sark) - The excellent library by Tamir Bahar is preinstalled, to simplify IDAPython scripting
* Special wrapper script in order to quickly run IDA without ANY screen output

## Requirements
Legit IDA Pro (Linux version) with its installation password

## Setup
* Clone this repository
* IMPORTANT: Add your IDA Pro installation file (.run) to the repository root folder, naming it: ida.run
* IMPORTANT: Insert your IDA installation password in the Dockerfile (see instructions in Dockerfile)
* docker build -t ida .

## Simple Usage
    docker run -it -v "$PWD":/project -w /project ida idal.py -Sexamples/hello.py -A file_to_reverse.exe
    
This command runs the IDAPython script "examples/hello.py" on the file "file_to_reverse.exe".

The command creates a volume in the docker container for the current directory and place it in "/project" path in the container.  That way you can use the current directory as a source for the sample you want to reverse, the script you want to run, and to get output files out of IDA.

## Advanced Usage
For IDA 64 bit files:
```
docker run -it -v "$PWD":/project -w /project ida idal64.py -Sexamples/hello.py -A file_to_reverse.exe
```

You can use any of the [IDA command line arguments](https://www.hex-rays.com/products/ida/support/idadoc/417.shtml), except for GUI-related switches:
```
docker run -it -v "$PWD":/project -w /project ida idal.py [arg1] [arg2] [arg3]
```

You could also run IDA in the awful TVision terminal-GUI mode if you really want to.  Just open a shell using:
```
docker run -it -v "$PWD":/project -w /project ida bash
```
And run the regular IDA binary (idal or idal64), it's already in the PATH:
```
idal arg1 arg2...
idal64 arg1 arg2...
```

## Installing external libraries
Just add the library you wish to the "requirements.txt" file before you build the Dockerfile

## IDA-Dockerized in Windows
In Windows, docker has its problems parsing paths, so you'll need to add some '/' like this:
```
docker run -it -v "/$PWD":/project -w //project ida idal.py -Sexamples/hello.py -A file_to_reverse.exe
```
Or for 64 bit files:
```
docker run -it -v "/$PWD":/project -w //project ida idal64.py -Sexamples/hello.py -A file_to_reverse.exe
```

## Notes
Tested only with IDA 6.9, but should work with some previous versions as well
