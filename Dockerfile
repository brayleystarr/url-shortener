# fetch python base image from docker registry 
FROM python:3.12.3-slim 

# set working directory within container
WORKDIR /url-shortener

# push dependency list
COPY requirements.txt ./

# install dependencies
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt
    
# push application code 
COPY app ./app/

# start application 
CMD uvicorn app.main:app --host 0.0.0.0 --port 8000
    
