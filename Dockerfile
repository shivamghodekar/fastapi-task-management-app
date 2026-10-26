
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/data \
    && useradd -m appuser \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["fastapi", "run", "main.py", "--port", "8000", "--host", "0.0.0.0"]




##-------------------------------------------------------------------------
# FROM python: 3:12-slim

# WORKDIR /Task Management App

# COPY requirement.txt .
# RUN pip install -r requirement.txt


# COPY Task Management App ./Task Management App

# RUN mkdir -p /Task Management App/data \
#     && useradd -m appuser \
#     && chown -R appuser:appuser /Task Management App


# USER appuser

# EXPOSE 8000

# CMD ["fastapi", "dev main.py", "--port", "8000", "--host", "0.0.0.0"]