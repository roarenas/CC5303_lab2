FROM python:3.15-rc-slim
WORKDIR /app
RUN apt-get -y update
RUN apt -y install curl
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN chown nobody:nogroup /app

COPY --chown=nobody:nogroup lab1.py ./

ENV PORT=8000
EXPOSE 8000

CMD ["python","lab1.py"]