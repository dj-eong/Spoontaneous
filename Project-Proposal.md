# Spoontaneous

## Project Proposal

Overview:

Spoontaneous is a recipe webapp made to satiate the spontaneous home cook. Whenever users aren’t sure what to cook or are searching for inspiration, they can simply type in an ingredient and receive a random simple recipe that makes use of said ingredient.

Demographic:

Spoontaneous aims to serve anyone who is looking to cook and try out a new recipe, from first time cooks to experienced chefs expanding their recipe repository.

API:

I plan to use themealdb.com for my external API. This API is an open, crowd-sourced database of recipes and ingredients from around the world. Issues I may run into using the API include unavailable ingredients, unavailable recipes for searched ingredients, and formatting the user-searched ingredient to make it compatible with the API.

Database:

The data I will be storing is user information (username, password, potentially email) as well as their saved recipes. Passwords will need to be encrypted and secure.

Functionality/User Flow:

Users can choose to login/create an account at any time, but may use the site anonymously. The user types in an ingredient, and the website returns either a random recipe that uses the searched ingredient, or returns a message saying no recipe can be found with the ingredient (depending on API results). If the user is logged in, they may save the recipe for future use.

Stretch Goals:

An ambitious stretch goal is to allow users to interact with one another, meaning users can see each other’s profiles and saved recipes. Another stretch goal can be a tick list where users can check off recipes they have completed, and reflect it on their profile.
