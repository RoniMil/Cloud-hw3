FROM python:3.10.10-alpine
WORKDIR ./app
RUN pip install flask
RUN pip install flask_restful
RUN pip install requests
COPY dishes_meals.py .
EXPOSE 8000
ENV FLASK_APP=dishes_meals.py
ENV FLASK_RUN_PORT=8000

# examine whether the "--host=0.0.0.0" flag is neccessary
CMD ["flask", "run", "--host=0.0.0.0"]