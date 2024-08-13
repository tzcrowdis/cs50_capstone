# tzcrowdis Capstone Project

# Distinctiveness and Complexity

This project is a price comparison site. The idea is to consolidate information from the web on video game pricing all into one place. It's sort of like the website Kayak but instead of focusing on the travel market it focuses on the video game market.

## Django models
As a user you can search for games whether you are registered or not. If you register a User model will be created and you will be granted the ability to "track" games. Tracking stores the most relevant info (title and price) from each site in the database as a TrackedGame model which links back to the User through a foreign key. These results are displayed for the logged in user in a Tracked page. It shows the stored results and provides a link that will rerun the search.

## Search
To search the websites I used the libraries requests, beautiful soup, and selenium. Steam only required requests and beautiful soup as its site is mostly static but GOG and MyAbandonware required selenium as much of the information is dynamically loaded.

In each website I would insert the users input from my site form then add that to their websites search url. Then I would have to understand how they load search results to go to the games page. From the game page I pulled a thumbnail of the game, the title, the price, and the description of the game. Since each page has a different layout, grabbing the information from each required a thorough evaluation of each websites code and search methodologies.

I also had to handle multiple cases. For instance, if a game is discounted it displays its price in a different div, so my backend has to gracefully handle such differences that may throw errors.

### Sorting
Before returning the collected results I sort them with a bubble sort alogithm. I chose bubble sort because it's easy to implement and the search space is relatively small, as it's only the number of websites we search, so inefficiency isn't an issue.

## User Interface / Styling
This is where a large portion of the complexity comes in. The idea behind the layout is to resemble portals into the respective websites. The Steam result is meant to resemble Steams UI, the GOG result is meant to resemble GOGs UI, and so on. So, there wasn't just one UI styling theme but four, three for the searched websites and one for the this website. 

The way the websites handle buttons, images, pricing, and descriptions was different for each. For instance, GOG is unique from the others as it uses the thumbnail image as a background which has shadows applied to it from the box containing the other information.

Then for my website, I went with black and white as I wanted it to fall in the background when results load. I applied three main animations to my site. First, the loading animation, simple three dots that blink in order from left to right. Then a fade in and up to each of the results that is delayed based on the order of results. Finally, three square outlines that grow and fade out behind the results, delayed based on result order, intended to emphasive that the results are a portal into another website.

### Page Navigation
Once results load you can scroll between them or optionally use the keyboards up and down arrow keys which takes you to the result above or below. This required one javascript function to track the scroll position and change the key functionality and another to handle the key presses.

## Mobile Responsiveness
To accomodate mobile users the results are centered and designed to shrink horizontally without interefering with any other elements. The top navigation bar doesn't overlap with the search bar, which doesn't overlap with the results. The page navigation in the bottom right overlaps the results but does so purposefully with a transparent background besides the still visible buttons.

# File Contents

## views.py
### index
Displays nothing if no query given or calls the search function and returns the results to index.html.

### tracked
Gets all TrackedGame objects filtered on the current user and sends them to tracked.html.

### track_untrack
Depending on the status of the request it either saves a new TrackedGame object or deletes one with matching query and user.

### check_tracked
Searches the database to determine if a query is tracked or not by the user.

### login/logout/register
Standard functions.

## search.py
Contains the bubble sort algorithm adapted for the dictionaries that store the result data. Sorts ascending by price and forces MyAbandonware to the end as it's a special case.

Then the three functions that search each site (steam_search, abandonware_search, and gog_search).

Also, has a small function to remove escape sequences from the results pulled.

## models.py
User model, AbstractUser.

TrackedGame model stores the query, the results for each site, and a foreign key for the user.

## game_search.js
On the DOM Content Loaded it hides and displays certain aspects of the site. If results are present it will run a couple functions, one to insert each of the results carefully designed html. Then one to set all of the results animation delays based on their order. Finally if the user is logged in it sets the tracked button status.

Next there's page_nav_manager which changes the arrow buttons depending on the scroll bar location.

A tracked_results function sends data to track_untrack in views.py to handle tracking a query. Lots of error handling as results aren't always displayed.

## game_search.css
Contains all styling. Categorized roughly by all page styles (search styling, navigation, buttons, etc.), steam style, abandonware style, gog style, then animations.

## layout.html
Contains the navigation bar (login, register, tracked pages), the search bar, the page navigation box, the loading animation, and the track button.

Every other page inherits from layout.

## index.html
Iterates through the results given to it, putting them into generic divs due to sorting (later altered by a javascript function to add particular formatting), and places anchors for arrow key page navigation depending on loop iteration number.

## tracked.html
Recieves the list of tracked games from the back end, iterates through them, displays them in seperate tables for each search. They are flex boxes centered vertically in a column.

## register.html
Form that allows the user to register. Contains username, email, password, and password confirmation.

## login.html
Form that asks for username and password for the user to login.

# How to Run

There are no unique instructions. It should be similar to running any Django app.

1. Activate your virtual environment.
2. Navigate to the directory storing the files.
3. Type "python manage.py runserver".

# Additional Information

The search process can be slow, please give results up to 20 seconds to load.
