FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY src/pyproject.toml ./
RUN pip install --no-cache-dir tomli && \
    python -c "import tomli; deps = tomli.load(open('pyproject.toml', 'rb'))['project']['dependencies']; print('\n'.join(deps))" > requirements.txt && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ .

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

EXPOSE 3000

CMD ["python", "server.py"]