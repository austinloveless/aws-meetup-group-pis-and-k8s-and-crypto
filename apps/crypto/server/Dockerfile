FROM python:3.8	

# Create app directory
WORKDIR /app

# Install app dependencies
COPY src/requirements.txt ./

RUN pip install -r requirements.txt

# Bundle app source
COPY src /app

ENV API_KEY=figure_out_how_to_get_this_from_$API_KEY

EXPOSE 8080
CMD [ "python", "server.py" ]	