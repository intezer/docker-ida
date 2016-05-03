FROM intezer/ida-base

ARG IDA_INSTALLATION_FILE=ida.run
ARG IDA_PASSWORD

COPY $IDA_INSTALLATION_FILE /installation/
COPY requirements.txt /installation/

# Installing requirements for image
RUN pip2 install -r /installation/requirements.txt

# Install IDA
RUN mkdir /ida
# Copy IDA service
ADD ida-service/flask_service.py /usr/local/bin/
ADD ida-service/ida_service.sh /usr/local/bin/
# ida.run is the IDA installation executable file
RUN chmod +x \
    /installation/$IDA_INSTALLATION_FILE \
    /usr/local/bin/ida_service.sh

# Run IDA installation - echo keyboard input including installation password and "yes" commands
RUN printf "\n\n\n\n\n\ny\n$IDA_PASSWORD\n/ida\ny\ny\n" | /installation/ida.run

# Create a special file in order to prevent IDA to ask for license acceptance before executing IDA
RUN touch /ida/license.displayed

RUN mkdir /shared
WORKDIR /shared

ENV PATH /ida:$PATH
ENV TERM xterm
ENV PYTHONPATH /usr/local/lib/python2.7/dist-packages:/usr/local/lib/python2.7/site-packages:/usr/lib/python2.7/:$PYTHONPATH

ENTRYPOINT ["/usr/local/bin/ida_service.sh"]
