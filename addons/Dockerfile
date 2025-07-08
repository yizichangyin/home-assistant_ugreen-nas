FROM python:3.13-slim-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl wget gnupg ca-certificates fonts-liberation \
    libnss3 libatk-bridge2.0-0 libxss1 libasound2 \
    libxcomposite1 libxdamage1 libxrandr2 libgbm-dev \
    libgtk-3-0 libdrm2 \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt \
 && playwright install --with-deps

COPY . .

RUN chmod +x run.sh

EXPOSE 4115

CMD ["./run.sh"]