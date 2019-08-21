# Tasty Things

##### This project is a fictional recipe website made to demonstrate my data centric development skills.

# UX

This project is web application that allows users to add their own recipe in order to share it with
others, and also it allows users to search, update or delete existing recipes.

**User Stories:**  
* As user, I want to be able to find and read recipes 
  > this can be achived with a simple click on the green button found on every recipe 
* As user, I want to be able to search for recipes
  > this can be achived with a click on **Search Recipe** found on the navbar
* As user, I want to be able to update recipes
  > this can be achived by opening a recipe, and then **click** on the **Update** button
* As user, I want to be able to delete recipes
  > this can be achived by opening a recipe, and then **click** on the **Delete** button
* As user, I want to be able to see when a recipe has been updated last time
  > this is shown on every recipe just under the **Cooking Time** only if the recipe has been modified

# Features
### Existing Features

**Add Recipe**  - allow users to add their own recipe  
**Update Recipe** - -allow users to modify a recipe  
**Last Update** - display when a recipe has been modified last time  
**Delete Recipe** - allow users to remove a recipe  
**Search Recipe** - allow users to search for recipes by category

### Features Left To Implement

**Register and Login** - this will create more personal experience

**Like and Unlike** - this will allow users to share their opinions about a recipe

**Filters** - this will privide users with a better experience

# Technology Used

##### Structure and Functionality
**HTML5** - was used to structure the project  
**CSS3** - was used to style the project  
**jQuery** - was used for frontend functionality 
**Python 3** - was used for backend functionality  
**Flask**  - was used as micro framework for backend functionality  
**MongoDB** - was used for projects' database  
**Materialize** - was used for projects' responsivity

##### Development

This project has been developed using **AWS Cloud9** IDE


# Testing

**This project has been tested manually:**

* `open a recipe` - go to Home page - click on the green button found on any recipe - it will open the recipe
* `add a recipe` - from Home page - click **Add Recipe** - try to submit an empty form - it won't work as all fields are required    
  * fill in am fields - press **Submit** - it return to Home page and recipe has been added
* `edit a recipe` - open a recipe - click on the **Edit** button - modify the relevant fields - press **Update Recipe**
* `last update` - after flollowing the steps mentioned above at `edit a recipe`, it will automatically display the date when a recipe has been nodified
> NOTE: `Last Update` field is blank by default, it will only display the date WHEN and IF a recipe has been updated

* `delete a recipe` - open a recipe - click on the **Delete** button - it will remove that recipe and return to `Home Page`
* `search` - from any page - click on **Search Recipe** - type in the category - click **Search** - it will retrive results based on the recipe category




**Testing on Desktop Browsers & Mobile Devices:**   

|BROWSER | VERSION | COMPATIBILITY |
|:--------:|:---------:|:---------------:|
|GOOGLE CHROME|LATEST| 100%|
|MOZILLA FIREFOX|LATEST|100%|
|OPERA|LATEST|100%|
|SAFARI| LATEST|100%|

|DEVICE | VERSION | COMPATIBILITY |
|:--------:|:---------:|:---------------:|
|IPHONE|X, XS, XS MAX|100%|
|SAMSUNG|S7 PLUS, S9, S10|100%|

# Deployment

This project has been deployed to **Heroku**.
A live version can be found [here](https://tasty-things.herokuapp.com/).

# Credits

Some of the recipes has been copied from [BBC GOOD FOOD](https://www.bbcgoodfood.com/)  
Some of the page elements (e.g. navbar, footer..etc) has been taken from [Materialize](https://materializecss.com/getting-started.html).










