FROM rasa/rasa:3.6.21-full

COPY . /app
WORKDIR /app

EXPOSE 5005
CMD ["run", "--enable-api", "--cors", "\"*\"", "--port", "5005", "--debug"]