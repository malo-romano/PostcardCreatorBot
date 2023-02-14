FROM python:3.10

COPY app.py .

RUN pip install schedule

CMD ["python", "app.py"]