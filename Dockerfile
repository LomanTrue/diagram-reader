FROM python:3.10-slim-bullseye AS build

WORKDIR /app

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

RUN pip install --upgrade pip

RUN pip install --no-cache-dir torch==2.1.0 torchvision==0.16.0 \
    --index-url https://download.pytorch.org/whl/cpu

RUN pip install --no-cache-dir ultralytics --no-deps

COPY requirements.txt .
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

COPY app app
COPY models models

FROM python:3.10-slim-bullseye

WORKDIR /app

RUN apt-get update && apt-get install -y \
        tesseract-ocr \
        tesseract-ocr-eng \
        tesseract-ocr-rus \
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
