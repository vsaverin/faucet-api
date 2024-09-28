FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


COPY poetry.lock pyproject.toml /
RUN python3 -m pip install poetry
RUN PATH="$PATH:$HOME/.local/bin" && poetry config virtualenvs.create false
RUN PATH="$PATH:$HOME/.local/bin" && poetry install --no-root

COPY ../ /app
WORKDIR /app

RUN python manage.py migrate --noinput

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]