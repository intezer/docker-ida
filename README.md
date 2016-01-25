# IDA-Dockerized
Dockerized version of IDA Pro by Hex Rays.
By wrapping IDA with an ultra-fast, minimal command line interface, this project is especially suitable for automating the use of IDAPython scripts and batch analysis.

This docker image is configured to have everything you need for a working IDA machine, ready to run scripts:
* IDA Pro (Linux version) automatically installed with all its dependencies
* pip install - Easily install external python libraries that integrate into the IDAPython engine
* [sark](https://github.com/tmr232/Sark) - The excellent library by Tamir Bahar is preinstalled, to simplify IDAPython scripting
* Special wrapper script in order to quickly run IDA without ANY screen output

## Requirements
Legit IDA Pro (Linux version) with its installation password

## Setup
* Clone this repository
* IMPORTANT: Add your IDA Pro installation file (.run) to the repository root folder, naming it: ida.run
* IMPORTANT: Insert your IDA installation password in the Dockerfile (see instructions in Dockerfile)
* docker build -t ida .

## Simple Usage
    docker run -it -v "$PWD":/project -w /project ida idal.py -Sexamples/hello.py -A /project/file_to_reverse.exe
    
This command runs the IDAPython script "examples/hello.py" on the file "file_to_reverse.exe".

The command creates a volume in the docker container for the current directory and place it in "/project" path in the container.  That way you can use the current directory as a source for the sample you want to reverse, the script you want to run, and to get output files out of IDA.

## Advanced Usage
For IDA 64 bit files:
```
docker run -it -v "$PWD":/project -w /project ida idal64.py -Sexamples/hello.py -A /project/file_to_reverse.exe
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
    docker run -it -v "/$PWD":/project -w //project ida idal.py -Sexamples/hello.py -A //project/file_to_reverse.exe
```
Or for 64 bit files:
```
    docker run -it -v "/$PWD":/project -w //project ida idal64.py -Sexamples/hello.py -A //project/file_to_reverse.exe
```

## Notes
Tested only with IDA 6.9, but should work with some previous versions as well
