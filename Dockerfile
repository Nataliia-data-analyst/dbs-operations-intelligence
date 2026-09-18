FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY server ./server

RUN pip install --no-cache-dir .

ENV MCP_TRANSPORT=streamable-http
ENV PORT=8000

CMD ["python", "-m", "server.main"]