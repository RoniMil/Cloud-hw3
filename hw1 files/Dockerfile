FROM python:3.10.10-alpine
WORKDIR ./app
RUN pip install flask
RUN pip install flask_restful
RUN pip install requests
COPY hw1.py .
EXPOSE 8000
ENV FLASK_APP=hw1.py
ENV FLASK_RUN_PORT=8000
CMD ["flask", "run", "--host=0.0.0.0"]