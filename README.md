# Spoontaneous

Link: [Spoontaneous](https://spoontaneous.onrender.com/)

## What is Spoontaneous?

Spoontaneous is a recipe webapp made to satiate the spontaneous home cook. Whenever users aren’t sure what to cook or are searching for inspiration, they can simply type in an ingredient and receive a random easy recipe that makes use of said ingredient.

## Features

Spoontaneous is a very simple webapp, with two main functionalities:

1. Search an ingredient and get a random recipe in return
   
   I chose to make the interaction very clean and straightforward, as the goal is to provide quick inspiration for cooking. The random feature favors anyone looking to be spontaneous with their next meal.

2. Make an account and save/unsave recipes
   
   When coming across a recipe that they really like, or may want to try out later, the save feature is crucial.

## Usage

To run Spoontaneous locally, follow these steps:

1. Make sure you have [Python v3.7.9](https://www.python.org/downloads/release/python-379/) and [PostgreSQL](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads) installed

   1.5 (Optional) Create a [virtual environment](https://packaging.python.org/en/latest/tutorials/installing-packages/#creating-and-using-virtual-environments) and activate it

2. Install all of Spoontaneous' dependencies/requirements by running the following command in your terminal
```
$ pip install -r requirements.txt
```

3. Create your local database and title it `spoontaneous`
```
$ createdb spoontaneous
```

4. Set your DATABASE_URL environment variable and run the application!
```
$ DATABASE_URL=postgresql:///spoontaneous flask run
```


## User Flow

Users can choose to login/create an account at any time, but may use the site anonymously. The user types in an ingredient, and the website returns either a random recipe that uses the searched ingredient, or returns a message saying no recipe can be found with the ingredient (depending on API results). If the user is logged in, they may save the recipe for future use. Users can access their saved recipes list, look at each saved recipe in detail, and unsave them if they wish.

## API

The API used is [themealdb.com](https://themealdb.com/api.php). This API is an open, crowd-sourced database of recipes and ingredients from around the world.

## Tech Stack

Front-End:
- HTML
- CSS
- JavaScript
- Axios
- Bootstrap

Back-End:
- Python
- Flask
- PostgreSQL
