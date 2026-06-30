FROM mcr.microsoft.com/devcontainers/python:3.12-bookworm

RUN apt-get update && apt-get install -y curl git build-essential && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
 && apt-get update && apt-get install -y nodejs

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY package.json package-lock.json /tmp/frontend/
WORKDIR /tmp/frontend
RUN npm ci

RUN python -m playwright install chromium && python -m playwright install-deps chromium

WORKDIR /workspaces
