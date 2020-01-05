sparrow - a twitter clone.
It is a Flask-Web-App in which users can register and posts(only text). The users can search different users and view there profile. The only thing user can edit is their 'status'. The app has a feed which shows post according to the time and date they were posted. The app doesn't have following/followers functionality

My original intention was to copy all the good things that a different social media platform has and encapsulate them in one. I planned to use -
    1> Posts of twitter
    2> Upvotes of Reddit
    3> Follow Feature of Instagram
    4> Feed like Facebook
But it didn't go as I planned.  

sparrow uses Python's built-in sqlite3 as it's database.

All the routes:-
   1 /
   2 /register
   3 /home
   4 /login
   5 /logout
   6 /feed
   7 /people
   8 /user
   9 /status
   10 /edit

All the templates:-
  1 feed.html
  2 find_people.html
  3 index.html
  4 layout.html
  5 login.html
  6 register.html
  7 status.html
  8 user.html


==> I used finance pset's 'layout.html' to make the layout of the app. I modified to fit with my App

==> I used flask sessions for user-login. "login_required()" is a decorator function. I don't know how it really works. I used the flask documentation to implement it. I used "passlib" library to generate encrypted hashes for password.

==>I used "flask_avatars" to generate unique images for each user according to their email. The "flask_avatars" generate gravtar's identicon, unique for each user. The hashlib library is used to generate the hash for email.

==>"register.html" asks user about : Name, Username(unique for each user), password, email, dob. These are submitted by a form to "/register" route. The "/register" route checks whether one or more input form the form are empty or not, if empty it flashes messages. It then generate password hash and email-hash for gravatar. The information is saved in 'info' table of users database. It creates a unique table of username of the user for storing post and then redirects "index.html" where the user is now asked to login

==>"login.html" asks user for the username and password. The data is submitted using a form to the "/login" route. This route first clears session and then checks if either fields are filled or not. Then if the password matches the username we start the session for the user and redirect to "index.html". The route uses "passlib" library 'verify()' function to verify the password

==>"index.html" shows the profile of user and the posts that user has posted. We obtain the information of the current user form 'info' table and all the post of user from table named after the user and pass it to "index.html". We use "jinja2" for generate the profile. "index.html" also has a 'Edit Status' button which redirects to "status.html" where user can edit their status.

==>"feed.html" has a 'text area' element that is connected to a form that posts data to the '/feed' route and a 'post area' which shows posts of each user from the data received from '/feed' route. The data sent and received to the '/feed' route is stored in 'status' table.

==>"find_people.html" has a 'search area' to search registered user and a table that lists username, gravtar, email and "view button". The post request is used in 'search area' and get request is used to generate the table of users.
    Each row of the table has a form that post data
to '/user' route which and displays the profile of user whose "view button" is clicked in "user.html"

==>For the icon I used the favicon's sparrow emoji

==> I deployed the app in heroku. I used sqlite3 because of which the app resets after some time to the original state as it was deployed originally. I thought of learning SQLalchemy, Postgresql to implement them instead of sqlite3 but that was a little overwhelming.


Although I was not able to implement what I thought and planned but I learned a lot of things during the making of this project:
  1> Responsive Web Pages(using media tag in CSS)
  2> Gravtar
  3> Not to use Disk-based Database like sqlite3 for such projects
  4> A lot of cool things about front-end
  5> Use of libraries
  6> How to Google Search for Errors
  7> Deploying a flask app on Heroku
