FROM python:3.10-slim

LABEL vendor=neon.ai \
    ai.neon.name="neon-messagebus"

ENV OVOS_CONFIG_BASE_FOLDER=neon
ENV OVOS_CONFIG_FILENAME=neon.yaml
ENV OVOS_DEFAULT_CONFIG=/opt/neon/neon.yaml
ENV XDG_CONFIG_HOME=/config

EXPOSE 8181

RUN apt-get update && \
    apt-get install -y \
    jq \
    curl \
    gcc \
    python3-dev \
    swig \
    libssl-dev

COPY . /neon_messagebus
WORKDIR /neon_messagebus

RUN pip install --no-cache-dir wheel \
    && pip install --no-cache-dir .[docker]

COPY docker_overlay/ /

HEALTHCHECK CMD "/opt/neon/healthcheck.sh"
CMD ["neon-messagebus", "run", "--hp", "8000"]
