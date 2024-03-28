FROM python:3.11

WORKDIR /wd

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["streamlit", "run", "app.py"]