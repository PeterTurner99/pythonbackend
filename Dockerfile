FROM python:3.11-slim-bullseye

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends gcc && \
	pip install --no-cache-dir -r requirements.txt && \
	apt-get purge -y --auto-remove gcc && \
	rm -rf /var/lib/apt/lists/*

COPY . .

CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8080" ]