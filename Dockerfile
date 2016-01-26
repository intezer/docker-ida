FROM buildpack-deps
COPY ida.run /tmp/
COPY requirements.txt /tmp/

# Add 32 bit architecture support for IDA
RUN dpkg --add-architecture i386 && apt-get -y update

# Replace the python version in the original image with a 32-bit version, so when we install external libraries -
# IDAPython (32bit) could import them
RUN apt-get -y install python2.7-minimal:i386
RUN apt-get -y install python2.7:i386
# Create a symlink for python for convenience (instead of typing python2.7)
RUN link /usr/bin/python2.7 /usr/bin/python

# Install necessary libraries for IDA and IDAPython to work
RUN apt-get -y install --fix-missing lsb-core lib32gcc1 libc6-i686:i386 libstdc++6:i386 libglib2.0-0:i386 libfreetype6:i386 libsm6:i386 libxrender1:i386 libfontconfig:i386 libxext6:i386 libssl-dev:i386 libpython2.7:i386
RUN wget http://ftp.us.debian.org/debian/pool/main/o/openssl/libssl0.9.8_0.9.8o-4squeeze14_i386.deb -P /tmp
RUN dpkg -i /tmp/libssl0.9.8_0.9.8o-4squeeze14_i386.deb

# Install pip for python 2.7
RUN wget https://bootstrap.pypa.io/get-pip.py -P /tmp
RUN /usr/bin/python2.7 /tmp/get-pip.py

# Install Sark library for IDAPython
RUN pip2 install -r /tmp/requirements.txt
RUN pip2 install -U git+https://github.com/tmr232/Sark.git#egg=Sarks

# Install IDA
RUN mkdir /ida
# Copy IDAPython helper script to IDA installation folder
COPY idal.py /ida/
COPY idal64.py /ida/
# ida.run is the IDA installation executable file
RUN chmod +x /tmp/ida.run
# Run IDA installation - echo keyboard input including installation password and "yes" commands
# NOTICE: YOU HAVE TO CHANGE "[YOUR_IDA_INSTALLATION_PASSWORD_HERE]" TO YOUR LEGIT IDA INSTALLATION PASSWORD
RUN printf "\n\n\n\n\n\ny\n[YOUR_IDA_INSTALLATION_PASSWORD_HERE]\n/ida\ny\ny\n" | /tmp/ida.run
# Create a special file in order to prevent IDA to ask for license acceptance before executing IDA
RUN touch /ida/license.displayed

ENV PATH /ida:$PATH
ENV TERM xterm
ENV PYTHONPATH /usr/local/lib/python2.7/dist-packages:/usr/local/lib/python2.7/site-packages:/usr/lib/python2.7/:$PYTHONPATH
