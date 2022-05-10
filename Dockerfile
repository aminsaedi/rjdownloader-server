FROM python

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --upgrade setuptools
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./main.py" ]
EXPOSE 8080 
