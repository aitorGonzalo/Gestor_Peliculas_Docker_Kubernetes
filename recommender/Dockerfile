FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install Flask mysql-connector-python flask-cors werkzeug

# Activa el modo de depuración en Flask
ENV FLASK_APP=recommender.py
ENV FLASK_ENV=development

EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
