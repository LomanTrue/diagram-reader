FROM python:3.10-slim-bullseye AS build

WORKDIR /app

RUN python --version && which python

RUN pip install --upgrade pip

RUN apt-get update && apt-get install -y \
        build-essential \
        libglib2.0-0 \
        libgl1 \
        libsm6 \
        libxext6 \
        libxrender-dev \
        wget \
        git \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --prefix=/install numpy

RUN pip install --no-cache-dir --prefix=/install \
        torch torchvision \
        --index-url https://download.pytorch.org/whl/cpu

RUN pip install --no-cache-dir --prefix=/install \
    paddlepaddle==3.2.0 \
    paddlex \
    paddleocr==3.3.3 \
    -f https://www.paddlepaddle.org.cn/whl/linux/cpu/avx/stable.html \
    --timeout 120

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

COPY app app
COPY models models

FROM python:3.10-slim-bullseye

WORKDIR /app

RUN apt-get update && apt-get install -y \
        libglib2.0-0 \
        libgl1 \
        libsm6 \
        libxext6 \
        libxrender1 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=build /install /usr/local

COPY app app
COPY models models

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
