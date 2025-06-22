FROM python:3.13-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl wget gnupg ca-certificates fonts-liberation \
    libnss3 libatk-bridge2.0-0 libxss1 libasound2 \
    libxcomposite1 libxdamage1 libxrandr2 libgbm-dev \
    libgtk-3-0 libdrm2 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && playwright install --with-deps

COPY . .

EXPOSE 4115

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4115"]
