FROM python:3.12-alpine
WORKDIR /app
EXPOSE 80
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD [ "gunicorn", "--bind", "0.0.0.0:80", "main:create_app()" ]