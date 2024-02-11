FROM python:3.12

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi \

ARG FLASK_SECRET_KEY
ENV FLASK_SECRET_KEY FLASK_SECRET_KEY

COPY . /app

CMD ["poetry", "run", "python", "app.py"]
