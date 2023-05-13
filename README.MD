# BDI-II

This is an improved version of the BDI-II project.

It is in progress.

## Model

![Model-ML-BDI-II](https://images2.imgbox.com/4a/db/CDNDXpw3_o.png)

To install the libraries, run the following command in the terminal:
```console
    pip install -r requirements.txt
```

Libraries used:
* Selenium 
* python-dotenv
* psycopg2

Command Docker Postgres:
```console
    docker run --name postgres-bdi-ii -dp 5432:5432 -e POSTGRES_USER= -e POSTGRES_PASSWORD= postgres:14.7-alpine
```

## Notes:

- Every microservice has its own dockerfile to build the image.
- Change the production.Unix.sh file to run the microservices in production mode with your own credentials.

   

#### Acknowledgment
@drojas159 for contributing with Web Scraping scripts.
