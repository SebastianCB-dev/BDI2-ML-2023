# BDI-II

Welcome to the improved version of the BDI-II project! This README provides an overview of the project and instructions for installation and configuration.

## Project Overview

The BDI-II project is currently in progress and aims to enhance the existing BDI-II model. The project utilizes machine learning techniques to analyze and interpret data related to the Beck Depression Inventory-II (BDI-II), a widely used self-report instrument for measuring depression severity.

## Model

The project incorporates the following machine learning model:

![Model-ML-BDI-II](https://images2.imgbox.com/4a/db/CDNDXpw3_o.png)

## Installation

To install the necessary libraries, follow these steps:

1. Open your terminal or command prompt.
2. Navigate to the project directory.
3. Run the following command:

```console
pip install -r requirements.txt
```

This command will install the required libraries, including:
- Selenium
- python-dotenv
- psycopg2

## Configuration

Before running the project, you need to set up some environment variables. Follow the steps below to configure the necessary variables:

### Instagram Credentials

1. Obtain your Instagram credentials (username and password).
2. Open the `.env` file in the project directory.
3. Set the values of the following variables:
   - IG_USERNAME='' (Replace the empty quotes with your Instagram username)
   - IG_PASSWORD='' (Replace the empty quotes with your Instagram password)

### Database PostgreSQL URL

1. Obtain the URL for your PostgreSQL database.
2. Open the `.env` file in the project directory.
3. Set the value of the `POSTGRES_URL` variable to your PostgreSQL URL.

```
POSTGRES_URL=postgresql://username:password@host:port/database
```

* You have to run the scripts in the `DB` directory to create the tables.

### Database Credentials

1. Provide the necessary credentials for your database.
2. Open the `.env` file in the project directory.
3. Set the value of the `POSTGRES_URL` variable to your database credentials.

## Notes

Here are some additional notes regarding the project:

- Each microservice within the project has its own Dockerfile for building the corresponding image.
- If you intend to run the microservices in production mode, make sure to modify the `production.Unix.sh` file with your own credentials.

## Possible Issues

You will probably be able to get the following issues:

1. ChromeDriver issues:
   - Validate that you ChromeDriver's version is the same that you Google Chrome's version.
   - Make sure that the ChromeDriver's path is correctly typed.

2. Environment Variables issues:
   - Actually you have to stablish 3 environment variables (IG_USERNAME, IG_PASSWORD and POSTGRES_URL) to the correctly functionality

3. The program broke suddenly.
   - This could be happen because it is a scraper and maybe you have to change some script to get the correct HTML's elements.

## Acknowledgment

We would like to extend our appreciation to @drojas159 for contributing valuable Web Scraping scripts to the project.

Feel free to reach out if you have any questions or need further assistance.

Enjoy using BDI-II!
