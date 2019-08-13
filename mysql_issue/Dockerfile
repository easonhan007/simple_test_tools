FROM python:3.6

LABEL maintainer="easonhan@itest.info"

RUN pip install flask PyMySQL

EXPOSE 80
ADD app.py /app.py

CMD ["python", "/app.py"]
