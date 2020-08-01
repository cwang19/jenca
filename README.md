# JenCa Documentation

## Check out the website here!
http://jenca.herokuapp.com/

## General Overview and Compiling
JenCa was created in the CS50 IDE. To run the project, open a new terminal in the CS50 IDE and navigate to the ```jenca/``` directory. Within the ```jenca/``` directory, run the command ```flask run``` to start Flask's built-in web server. The JenCa web application will open in a new tab.

## Registering and logging in
After opening JenCa, users will initially be directed to a login page, with a link to a register page as well.
If you already have an account, enter your username and password in the login form to access your dashboard.
If not, create a new account on the ```register``` page. You will be prompted for a username (different from any existing usernames), a password (that's at least 5 characters long and contains at least 1 number and 1 special character) as well as an identical password confirmation, and a monthly budget (which must be greater than 0). After successfully registering for an account, users will be redirected back to the ```login``` page, where they can input their credentials and log in.
If there is an error at any point, the web app will respond by directing the user to the ```apology``` page, which will display a corresponding error message.
If you want to log out after logging in, select the ```Log Out``` link in the upper right corner.

## Dashboard
After successfully logging in, users will first be directed to the ```dashboard```. In the navigation bar, users will see the tabs they can immediately switch to: Dashboard, Log Expense/More Money, Change Budget, History, and Log Out.
At the top of the page is a jumbotron with a monthly overview. The jumbotron is originally grey in background color, but as soon as the user overdraws on their balance, it will turn a shade of red.
There is a link ("Monthly History") that will direct users to a page with a table containing all expenses (in all categories) they logged within the previous month. Below the link, there are three statistics: their total monthly budget, the total amount they spent in the current month, and how much money remains in the budget for this month.
To the right of these statistics is a pie chart. Each slice of the pie (i.e., each category) is represented by a different pastel color. Hovering over a slice of the chart will indicate which category that slice refers to and how much money was spent in that category. The pie chart will update as the user logs transactions and as the months change.
Scrolling down will display tables for each category of expense the user has logged. New users or users who have not inputted any expenses from the current month will therefore not see any categories or expenses because there are none. There will be at most two category tables per row. Each category table is titled with the category and subtitled with the amount of money spent in that category this month.
Beneath each category header is a log of the five most recent transactions in the past month in that category (date, cost, and description), as well as an account of how much of one's budget has been spent on that catgeory this month. These category tables are also color coded based on what percentage of your budget you are spending in that category. The larger the percentage of your budget is spent in that category, the deeper the saturation of green. Furthermore clicking on the "View More" link in each card will link to the monthly log of expenses in that specific category (showing a table of transaction history in that category from the current month).

## Logging expenses and changing one month's budget
In order to log an expense, click on the ```Log Expense/More Money``` tab in the navigation bar. This will link users to a page where they can input a category (from a dropdown), cost of the expense, the item purchased or business where the transaction occured (or a very brief description of where the expense came from), additional notes about the expense, and the date of purchase. Assuming all fields are filled correctly, clicking the ```Submit``` button will allow users to return to the dashboard, where the pie chart and that category of description are edited correspondingly.
However, if you received an increase in money for one month (maybe you found $20 on the ground or your friend gave you a $25 gift card for your birthday) or you'd simply like to increase your monthly budget for one month, you may select the "Raise" option. This category is excluded from the expense categories on the dashboard and only changes your budget for the current month and the amount of money you have left in this month (i.e., the "Initial Budget" and "Amount Left" categories).

## Changing all monthly budgets
To overwrite the initial budget amount you chose while registering, select the ```Change Budget``` tab in the navigation bar. Input a new monthly budget (any value greater than $0 per month) and a confirmation. If the values match and are valid, your subsequent monthly budgets will all have the new value.

## History
Selecting the history tab will show a table of all transactions made in all categories in all time (not limited to the past month). The table will describe the category, description, amount spent, date, and notes.
Note: raises will appear here as well.
