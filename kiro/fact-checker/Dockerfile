FROM public.ecr.aws/docker/library/python:3.11-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN pip install uv && uv pip install --system -r pyproject.toml

COPY app ./app
COPY run.py ./
COPY instance ./instance

EXPOSE 8080

CMD ["gunicorn", "-b", "0.0.0.0:8080", "run:app"]
