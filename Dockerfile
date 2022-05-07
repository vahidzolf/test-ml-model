FROM python:3.6-slim
COPY ./app.py /deploy/
COPY ./requirements.txt /deploy/
COPY ./iris_trained_model.pkl /deploy/
WORKDIR /deploy/
RUN pip install -r requirements.txt
RUN apt install sqlite
EXPOSE 5000
ENTRYPOINT ["python", "app.py"]
