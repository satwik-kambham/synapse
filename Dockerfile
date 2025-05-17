FROM nvidia/cuda:12.9.0-cudnn-devel-ubuntu24.04

RUN apt update && \
    apt install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    curl \
    ffmpeg \
    espeak-ng \
    && apt clean

ADD https://astral.sh/uv/0.7.3/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

ADD . /app
WORKDIR /app
RUN uv sync --locked
RUN uv pip install pip

# CMD ["/bin/bash"]
CMD ["uv", "run", "flask", "--app", "main.py", "run"]
