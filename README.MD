# Machine Learning model based on natural language processing to recognize depressive symptomatology on Instagram comments (SPA🇨🇴-ENG🏴󠁧󠁢󠁥󠁮󠁧󠁿) 

Welcome to the improved version of the BDI-II project! This README provides an overview of the project and instructions for installation and configuration.

You can find the old project [here](https://github.com/SebastianCB-dev/BDI2-ML).

1. [Project Overview 📝](#project-overview)
2. [What is new? 🤔](#what-is-new-)
3. [Structure 🤖](#structure-)
4. [Web Scraping 🕸️](#web-scraping-)
   - [Introduction 📜](#introduction-)
   - [To have in mind 👁️](#to-have-in-mind-)
   - [Installation (Web Scraping) 🛠️](#installation-web-scraping-)
   - [Configuration](#configuration)
   - [Instagram Credentials](#instagram-credentials)
   - [Database PostgreSQL URL](#database-postgresql-url)
   - [Database Credentials](#database-credentials)
   - [Notes](#notes)
   - [Possible Issues](#possible-issues)
   - [ChromeDriver issues](#chromedriver-issues)
   - [Environment Variables issues](#environment-variables-issues)
   - [The program broke suddenly](#the-program-broke-suddenly)
9. [Project Contributors](#project-contributors)
10. [Acknowledgment](#acknowledgment)

## Project Overview 📝

The project is currently in progress and aims to enhance the existing BDI-II repository and model. The project utilizes machine learning techniques to analyze and interpret Instagram comments and compare them with each Beck Depression Inventory-II (BDI-II) item, a widely used self-report instrument for measuring depression severity.

## What is new? 🤔

The idea of this project is to include the English language (create a new model) and divide the responsibilities into small parts known as microservices.

## Structure 🤖

The project incorporates the following machine learning model:

![Model-ML-BDI-II](https://images2.imgbox.com/7f/61/ou4pnlOO_o.png)

## Web Scraping 🕸️

### Introduction 📜
This project uses Web Scraping to obtain the comments from Instagram posts. Using selenium, the program is able to log in to Instagram and get the users' username then it goes to the users' profile and get the posts' links. After that, the program goes to each post and get the comments. Finally, the program saves the comments in a database.

### To have in mind 👁️
- It is possible that the web scraping program does not work correctly due to the HTML's elements change constantly.
- The program is not able to get the comments from private accounts. (At least the user accept the request which is send by the four microservice)
- The web driver is set to work with Chrome, if you want to use another browser you have to change the web driver and make the necessary changes in the code.
- The program is set to work with the Spanish language (at least for the moment)

## Installation (Web Scraping) 🛠️

To install the necessary libraries, follow these steps:

1. Open your terminal or command prompt.
2. Navigate to the project directory (microservice that you want to execute).
3. Run the following command:

```console
pip install -r requirements.txt
```

This command will install the required libraries, including:
- Selenium
- python-dotenv
- psycopg2
- bs4

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
   - This could be happen due it is a scraper and maybe you have to change some script to get the correct HTML's elements.

### Project Contributors

- [Joan Sebastián Carrillo Barón](https://github.com/SebastianCB-dev)
- [Fabián Andres Rojas García](https://github.com/fabianroga)
- [Juan David Mejia Morales](https://github.com/JuanDavision1)
- [Daniela Rojas](https://github.com/drojas159)

## Acknowledgment

We would like to extend our appreciation to Holman Diego Bolivar Barón for being our tutor.

Feel free to reach out if you have any questions or need further assistance.

Enjoy using this project!
