FROM python:3.9-slim
MAINTAINER Jake House "jhouse@uoregon.edu"
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
RUN chmod 644 /app/*.py
EXPOSE 5000
CMD ["python", "flask_brevets.py"]