FROM alpine:3.17.0

RUN apk update && apk add --update --no-cache \
    bash \
    curl \
    jq \
    && rm -rf /var/cache/apk/*

WORKDIR /app

# installs aws CLI for role assumption
RUN apk add --no-cache \
    python3 \
    py3-pip \
    && pip3 install --upgrade pip \
    && pip3 install --no-cache-dir \
    awscli \
    && rm -rf /var/cache/apk/*

# installs driftctl
RUN curl -L https://github.com/snyk/driftctl/releases/latest/download/driftctl_linux_amd64 -o /bin/driftctl \
    && chmod +x /bin/driftctl

COPY .driftignore .
COPY run-driftctl.sh .
COPY driftctl2asff.py .
RUN chmod +x run-driftctl.sh

ENTRYPOINT ["/app/run-driftctl.sh"]
