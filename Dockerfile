FROM python:3-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV MONGO_URI=${MONGO_URI}
EXPOSE 5000

CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]