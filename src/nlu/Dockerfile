FROM rasa/rasa:3.6.21-full

COPY . /app
WORKDIR /app

RUN chmod +x start.sh

EXPOSE 5005
CMD ["./start.sh"]