FROM python:3.10
WORKDIR /
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT python main.py