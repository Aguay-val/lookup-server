FROM python:3-alpine

WORKDIR /usr/src/app

# Tell Python to not generate .pyc
ENV PYTHONDONTWRITEBYTECODE 1
# Turn off buffering
ENV PYTHONUNBUFFERED 1
ENV MONGO_URI=${MONGO_URI}
ENV MONGO_LIMIT=${MONGO_LIMIT}
ENV SEARCH_LIMIT=${SEARCH_LIMIT}

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn"  , "-b", "0.0.0.0:5000", "app:app"]
