FROM python:3.11-slim

WORKDIR /app

COPY protocol.py server.py client.py metrics.py ./

# psutil para métricas de sistema
RUN pip install --no-cache-dir psutil

EXPOSE 5000

CMD ["python", "server.py"]
