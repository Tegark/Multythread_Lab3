# Setting base image
FROM frolvlad/alpine-gxx

# Installing python and pip
RUN apk add --update python python-dev py-pip   

# Upgrading pip
RUN pip install --upgrade pip

# Installing Python modules for application to run correctly
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

# Copying application code to cource directory
COPY app.py /usr/src/app/

# Exposing the port number the container should expose
EXPOSE 5000
EXPOSE 5555

# Starting the application
CMD ["python", "/usr/src/app/app.py"]