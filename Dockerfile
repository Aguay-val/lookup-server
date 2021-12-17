FROM python:3-alpine

WORKDIR /app

# Tell Python to not generate .pyc
ENV PYTHONDONTWRITEBYTECODE 1
# Turn off buffering
ENV PYTHONUNBUFFERED 1
ENV MONGO_URI=${MONGO_URI}

EXPOSE 5000

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
