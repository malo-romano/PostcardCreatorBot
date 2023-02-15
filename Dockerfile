FROM python:3.10

COPY app.py imagemanager.py postcardmanager.py settings.py ./

RUN pip install schedule Pillow geopy postcard-creator

CMD ["python", "app.py"]