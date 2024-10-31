FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install Flask mysql-connector-python
EXPOSE 5000
CMD ["python", "recommender.py"]
