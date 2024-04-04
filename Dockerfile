ARG BUILD_FROM=hassioaddons/base-python:5.2.0
# hadolint ignore=DL3006
FROM ${BUILD_FROM}

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Copy Python requirements file
COPY requirements.txt /tmp/
COPY webserver.py /

# Copy data for add-on
COPY run.sh /

# Install requirements for add-on
RUN pip install -r /tmp/requirements.txt

RUN chmod a+x /run.sh
CMD [ "/run.sh" ]