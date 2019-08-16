FROM python:3.6

LABEL maintainer="easonhan@itest.info"

RUN pip install flask PyMySQL Faker

EXPOSE 80
ADD app.py /app.py
ADD data_builder.py /data_builder.py

CMD ["python", "/app.py"]
