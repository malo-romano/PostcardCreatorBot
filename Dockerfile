FROM python:3.10

COPY app.py .

RUN pip install schedule Pillow geopy postcard-creator

CMD ["python", "app.py"]