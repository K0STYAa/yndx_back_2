FROM python:3.10

COPY . .
RUN pip install -r requirements.txt

WORKDIR /
ENTRYPOINT python main.py
CMD ["python", "-u", "main.py"]