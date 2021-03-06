FROM python:3.6.9

COPY . /usr/src/app
WORKDIR /usr/src/app

# Server port
EXPOSE 8000

RUN apt-get update

# update project source code if necessary (use by default https protocol)
RUN git remote set-url origin https://github.com/prise-3d/Thesis-WebExpe-Django.git
RUN git pull origin master

# Install dependencies and prepare project
RUN python --version
RUN pip install -r requirements.txt
RUN python manage.py makemigrations
RUN python manage.py migrate
RUN echo $WEBEXPE_PREFIX_URL
RUN WEBEXPE_PREFIX_URL=$WEBEXPE_PREFIX_URL
RUN WEB_API_PREFIX_URL=$WEB_API_PREFIX_URL

# create super user admin automatically
RUN bash create_admin.sh

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]