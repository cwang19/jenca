# JenCa Design

## Languages Used
JenCa relies heavily on HTML, CSS, and Bootstrap for the front-end. JavaScript was also used to make the website more interactive (color-coding and the pie chart). The back-end depends on Flask, Python, and SQL databases.
Bootstrap was chosen to complement HTML and CSS because of its clean look and mobile compatibility. It helped JenCa reach its goal of being aesthetic and pleasant to use. JavaScript helped to animate and create the pie chart, which aided users who wished to view their budget less numerically and more visually. Flask and Python were used in conjunction with HTML because of the ability to incorporate variables and simple functions into HTML; this enabled us to create updated tables. Finally, SQL databases were crucial to storing information about users and transactions in a way that could be easily queried using Python and the CS50 SQL library.

## application.py
The majority of the project relies on the ```application.py``` file, which contains all the functions and routes and links the pages together.
Below is a brief overview of each function, its purpose, and its significance:

```register```: this registers new users. It checks for errors in user registration (if a budget greater than 0 was set; if a unique username was chosen; and if a password with at least 5 characters with 1 number, and 1 special character matching the password confirmation was entered). The password must meet these conditions for improved security. If all of these conditions were met, a new user is created by entering the information into a SQL database named ```users```. The user ID is automatically generated, a hash of the password is entered, and the budget is inserted as well.

```login```: this method allows users to log in to the website. It ensures a username and password were submitted, ensures that this match is found in the users database, and remembers which user has logged in.

```index```: this controls the main page of JenCa: the dashboard. It queries the ```users``` database for the initial monthly budget. It also calculates the first and last day of the current month based on the current date. This used the Python ```datetime``` library for calculations; this ensures that the monthly history and overall display on the monthly dashboard is accurate. Next, the pie chart and tables are defined. The data for the chart is formatted here in application.py, and later passed to ```index.html``` where JavaScript was used to create and animate the pie chart and its labels. This chart, while challenging to make, helps improve the usability and comprehensibility of the site by visually representing one's budget. The colors were designated to be relatively light and pastel to complement the color scheme of the website. To query the labels and values for slices in the pie chart and the tables underneath, a SQL query for the categories was run. From this query, the category and total amount spent in each category are graphed and tabulated; the tables also show the five most recent transactions in each category of spending via ```index.html```. Finally, to account for monthly variations in spending (i.e., if users inputted a temporarily increase in spending in one month (a "raise"), the monthly budget is updated to represent the budget of the current month, as opposed to the typical monthly budget. Similarly, logged raises in the monthly budget are properly excluded from a category of spending.

```newexpense```: this allows a user to log a new expense or an increase in montly budget. It queries the form and checks for errors (if a category was selected, if a cost greater than 0 was inputted, and if a description and date were included). Provided that these conditions are met, the expense is logged by inserting these values into the ```expenses``` SQL database.

```change_budget```: as opposed to the "raise" option, this function permanently changes a user's monthly budget (until they decide to change it again). In other words, changing the monthly budget here carries over into changing budgets in subsequent months as well. This queries the form for the submission of valid and matching new budget values and confirmations, and then updates the budget for that user in the ```users``` SQL database.

```month_history```: this takes in a parameter, ```category```. Like in ```index```, ```register``` first calculates the first and last day of the month. If the catgeogry exists, it will calculate the history of expenses in the given category (the parameter) and return all transactions and details.

```history```: this is similar to ```month_history```, but instead of only choosing one category, this selects all categories and displays transaction histories for all categories in the current month.

```full_history```: this is also similar to the ```month_history``` and ```history```, but this expands upon ```history``` to return all transactions in all categories in all time.
For clarity, ```month_history``` = 1 category, 1 month; ```history``` = all categories, 1 month, and ```full_history``` = all categories, all months.

```logout```: finally, this allows a user to log out.

## SQL database
jenca.db was the name of the SQL database used in this project. It contains two tables (upon downloading the project, the tables will not contain any records):

```users```: this table tracks the users and registration. It is updated by ```register``` and ```change_budget```. It contains the following non-null fields: id (an automatically incremented integer), username (text), budget (number), and hash (a hash of the password: text). The budget can be changed after its initial value (chosen when a user registers for the first time) to account for potential salary increases or a desire to save more money per month.

```expenses```: this table links to ```users``` by the user id. It contains the fields user_id (an integer corresponding to the ```users``` table); the description, category, and notes (text); the cost (number) and the date (date of purchase: date). These fields were chosen because they encompass major aspects of logging expenses. Additionally, while "raises" are logged in this table as well, variations in monthly budgets (that do not carry over to the next month) enable users to have greater flexibility over each month's budget and add additional income amounts.
The database is queried to be displayed on the dashboard, as well as in the history tables. It's also used to track users and their profiles.

## Templates
The HTML templates are stored in the ```templates``` folder, and there is also a ```static``` folder containing images and a CSS file.
There are a variety of different HTML templates for each part of the site; they all extend ```layout.html``` to minimize
code repetition. Here is a brief walkthrough of each HTML file:

```apology.html```: displays error messages (as defined in ```application.py```).

```changebudget.html```: allows users to modify their monthly budget for each subsequent month.

```full_history.html```: shows all-time history for each category.

```history.html```: shows history of a specific category in the current month.

```index.html```: creates the dashboard, which contains a monthly overview jumbotron (including monthly spending statistics and a pie chart created with Javascript that tracks how much of one's budget goes into each category of spending).

```layout.html```: defines the general template from which the other templates extend; defines the navigation bar.

```login.html```: creates the user log in site.

```month_history.html```: shows history of all categories in the current month.

```new_expense.html```: allows users to log a new expense or a raise.

```register.html```: allows new users to register for an account.

We incorporated multiple different ways to view histories to enable users to filter transaction histories as they pleased. We decided that the filters of category and time were most important, so we chose to implement those.

## Bootstrap and CSS
Bootstrap was used for designing the UI; components like the jumbotron, cards, and tables were very useful. Additionally, we attempted to implement a relatively consistent color scheme to help our website's aesthetics. Color-coding the categories, both in the pie chart, category tables, and the description of whether or not one was over budget for the month, helped to reinforce the color scheme and help the website be more visually appealing to users.

## Information handling
Information was passed from ```application.py``` to the ```templates``` folder and vice versa. This was crucial to allowing the website to update automatically in real time, and this also enabled the code to be less redundant. Moreover, information would be passed to JavaScript; in particular, with the inclusion of the pie graph on the dashboard, values would be changed and updated live to make the pie chart accurate. Rather than pasting a static image of a chart in HTML by designing the graph in Python, saving the chart, and passing the static file to ```index.html```, instead, a more interactive and animated chart was created with JavaScript.