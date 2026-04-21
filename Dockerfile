FROM python:3.11-slim

# install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    unixodbc \
    unixodbc-dev

# install MS ODBC driver 18
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
 && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
 && apt-get update \
 && ACCEPT_EULA=Y apt-get install -y msodbcsql18

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

CMD ["python", "-m", "uvicorn", "pjm_APIlayer:app", "--host", "0.0.0.0", "--port", "10000"]