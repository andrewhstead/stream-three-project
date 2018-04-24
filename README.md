# Code Institute Stream Three Project

This is a project website for the Code Institute Full Stack Web Development course Stream Three. The project is a
website for a sports league, and has been constructed around a fictional baseball league, the data for which was
generated using the game "Out of the Park Baseball 18". The site is built using the Django framework and incorporates
elements which are common to sports league websites, such as news stories, game results and fixtures, information about
teams, and the ability for fans to interact and purchase premium content or merchandise.

Out of the Park Baseball was used to create a league consisting of eight teams, playing a 60-game league season each
year. The league was created for a 2000 season, thus enabling archive data to be included and a league history added to
the site.

## Contents
1. [Planning](#planning)
2. [Front End Development](#front-end-development)
	* [Responsive Design](#responsive-design)
	* [Use of Custom JavaScript](#use-of-custom-javascript)
	* [External JavaScript Libraries](#external-javascript-libraries)
	* [Other External Sources](#other-external-sources)
3. [Back End Development](#back-end-development)
	* [Home App](#home-app)
	* [News App](#news-app)
	* [Games App](#games-app)
	* [Teams App](#teams-app)
	* [Store App](#store-app)
	* [Forum App](#forum-app)
	* [Users App](#users-app)
4. [Deployment](#deployment)
5. [Testing](#testing)

## Planning

An important part of planning for the site was researching existing websites for sports league to see what kind of
content would typically be included. I was then able to make decisions about what I would be able to incorporate. Once
those decisions had been made, a number of wireframes were created using the 'Pencil' software to give an idea of how
the pages should be laid out both on narrow and wide screen sizes. I had to decide what data would be needed in the
database to enable me to include the content that I wanted, as well as how this should be divided up into distinct apps
within the Django project.

## Front End Development

### Responsive Design

The site was designed according mobile-first principles, with most of the functionality set up using the default layout
for devices with a width of 400 pixels or fewer. A break point is set at 800 pixels, with a maximum width on the page
content set at 1200 pixels. For devices wider than this, the header and footer continue to expand to fill the viewport
but there will be whitespace at either side of the content, which is centred on the page. The site is designed
  for a minimum screen width of 310 pixels.

The site's main navigation bar is visible at all times on devices wider than 800 pixels, while on narrow devices it is
hidden by default and can be toggled on and off by the user as required. This toggle is implemented through a simple
jQuery function.

On many pages of the site a sidebar is incorporated on larger devices to enable the user to view the most important
statistical information easily. This includes the most recent game results and the next scheduled fixtures, as well as
the current league standings. This information is incorporated into a separate template which is included in the
required pages, with a context processor being used to ensure that the relevant data is available to any template on the
 site. This sidebar is not included on narrower devices, as it would be visible only after a significant amount of
 scrolling rather than 'above the fold' as it is on wider screens.

In some sections of the site, this statistical data is replaced by alternative sidebar content. In the store, this
sidebar contains links which enable the user to view items related to a particular team. When viewing blogs, the sidebar
 shows a list of all site users who are registered as bloggers. Finally, in the forum the additional information shows
 the user then ten most recent posts, enabling them to link directly to the relevant thread.

### Use of Custom JavaScript

The site makes use of both jQuery and plain JavaScript. Plain JavaScript is used to remove success or failure messages
after five seconds on the screen, while there is also a script which allow the user to confirm any request to delete
content from the site. This applies to blog posts, forum posts, comments and items in shopping carts. Without this it
would be possible to accidentally delete content with one click.

Major use of JavaScript is made on the Home Page with the scrolling news headline effect. The seven most recent
news headlines are included with a banner image, and each is represented underneath by a blue dot. The latest item is
displayed by default, and every ten seconds the image transitions to the next item. The blue dots highlight the
currently displayed item. The user is able to select any item using the blue dots, and when a selection is made the ten
second counter is restarted.

### External JavaScript Libraries

Several simple jQuery functions are used to provide additional functionality. On devices below 800 pixels in width, the
main site navigation menu is hidden by default and can be displayed as a drop down from the header by clicking the menu
icon. This can then be toggled on and off using jQuery. A similar effect is used to allow users to hide comments on news
 stories or blog posts should they so desire. Further use of jQuery allows the user to scroll through the league sponsor
  logos on the home page. Those images are contained in a div which runs off  the page to the right, with the overflow
  hidden. The jQuery allows the div to be moved to the left or right as required.

### Other External Sources

In addition to the data generated by Out of the Park Baseball and the incorporation of the jQuery library, additional
sources were also used to add to the content of the site. Public domain stock images were sourced from
[PublicDomainPictures.net](http://www.publicdomainpictures.net), while external websites were also used to generate an
outline [Privacy Policy](https://privacypolicytemplate.net/) and [Terms and Conditions](https://termsandconditionsgenerator.com/) document for the site. Django's flatpages app was used to store these two
documents and links to them were placed in the site footer to be available from any page.

## Back End Development

### Home App

The simple 'Home' app contains the template for the site's Home Page, as well as a model which enables site users,
whether registered or not, to send messages to the site administrators. This is done by means of a form which saves the
message, along with the user's name and email address, to the database.

### News App

This app contains all the templates for rending news stories on the site. It also contains the templates which allow
site users with the relevant permission to add blog posts, as a blog post is treated as a specific category of news
story.

The app contains three models, the most important of which is that for the news stories themselves. There is a model for
 the category of the story, as well as one for comments which allows logged in users to comment on a particular story.
 The models file also contains a function which defines a list of registered 'bloggers', which is used to render a
 sidebar in wider screen displays which shows all the available blogs.

News can be viewed as a whole or on pages specific to each team. On each of these pages, pagination is used to
ensure that a maximum of 20 headlines are seen on screen at any one time. On any of these templates, the most recent
story is always displayed at the top with a banner image. These images, which are set using the 'cover_image' field in
the news item model, are optional and if one is not set for a particular story, then a default image for the relevant
category will be shown instead. Data from the news app is used elsewhere on the site, with recent stories being
incorporated on both the home page and also on the home pages for each individual team.

Team news is set up by 'tagging' one more more teams in a particular story by means of a many-to-many relationship. It
is not necessary to include any teams in the story, but the story will appear on the team news pages for any which are
selected. With the exception of authorised bloggers, all other news stories must be posted through the Administration
area by an authorised site administrator. Bloggers can add, edit and delete their posts through the site's front end,
with the project's superuser also having the ability to moderate posts in the same way. This is done through a single
form, used for either the creation of a new post or the editing of an existing one.

The only other form in this app is the one which allows for the posting and editing of comments. The user who posted the
 comment or the administration superuser are permitted to edit a given comment. Comments can be deleted, and  JavaScript
  is used to confirm that the user does indeed wish to delete the comment.

### Games App

The games app contains all the information about past results and scheduled fixtures. It includes templates for
displaying both data about individual games and also generating the league standings. The app includes two models - one
of which is to set up a list of seasons, in order to be able to allocate a game to a particular season and thus generate
 standings for that year. This setting is used to generate templates for the 'Archive' section, where a league-wide
 overview and team-specific details are available for each season.

The other model is the main game model, which sets a number of important details about a game. It is possible to
allocate to each game a date, a start time, a game 'type' (pre-season, regular or play-off game) and also the status of
the game, i.e. whether it has already been played or not. The model gives the opportunity to set the score details and
attendance for the game, as well as giving some games a setting of 'premium'. The premium setting is used to generate a
list of games which subscribers would have access to be able to stream live.

Equally important with the models file is a function which generates league standings. This takes all the games in a
specified season (taken as a parameter by the function) and includes the results of each one in the playing record of
the two teams involved. Calculation of the playing record involves adding to the number of games played and either wins
or losses, depending on the result of the game. The game score is added to the team's 'runs for' or 'runs against'
totals, while separate records are also created for home games and away games.

The standings function is used to create three different templates - one for the simple standings view used in the sidebar on many pages, another for more
detailed statistics on the main standings page and a third for archive standings of past seasons. A separate template
was created for this in order to ensure that the archive standings did not interfere with the current standings in the
sidebar on larger screens.

Templates in the games app allow a information to be presented in a variety of ways. The default scores page as linked
from the main menu shows the scores on the most recent game date, and the fixtures on the next scheduled game date. It
is this information which is included alongside the league standings in the sidebar. Users can then view results from
longer ago or statistics from further into the future, with pagination used to display three game dates at a time in
each case. There is also a template which renders a full list of either results or fixtures for the current season.

The main league standings page makes use of the only form in the games app, which allows the user to select a season to
easily view the standings for that year. In the scores and standings views, if a logged in user has taken the
opportunity to set a particular team as their 'favourite' then that team will be highlighted in the standings and in the
 games listed in the sidebar.

In order to make the last and next game dates and league standings available to templates across the site, a context
processor is used to set up this information. This is done because the need to prevent errors when there are no results
or fixtures available leads to a relatively complex function and it is included here to avoid repetition of large
amounts of code.

### Teams App

The teams app creates both the information about the teams in the league and also the details of the league's overall
structure. Two models exist, the first of which defines the 'Conferences' within the league. This splits the teams into
two sections (North and South) and is required both for listing the teams in some templates and also for generating the
standings in the correct way. Each team is allocated to one conference by use of a foreign key.

The main teams model gives each team a geographic name (i.e. the city in which they are based) and a nickname - put
together, these two fields create the team's full name. Each team also has an abbreviated name for use in templates
where space is more limited. Teams are given two different logos and three different team jerseys as images, all of
which are used in various places around the project. Because every page on the site needs to have access to an
alphabetical list of the teams in order to generate the logo links at the top of the page header, a context processor is
 used to make this data available site-wide.

The teams app requires only two templates, one of which is an index page which lists each team in turn (sorted into
conferences) and gives an overview of the available information about that team. The second template is the team's
'home' or 'profile' page, which gives more detail about that team. This template draws in data such as news stories,
forum discussions and game data to give a team specific overview. The most recent and next scheduled game for the team
is shown, as are the standings for that team's conference. Here, it is the team being displayed which is highlighted in
the standings rather than the user's favourite team (if set).

Templates for other pages linked from the team index page, such as the team-specific news, discussion forum or
merchandise store are created within the relevant apps.

### Store App

The store app includes all the e-commerce functionality of the project. It contains two different types of
functionality, the ability to purchase merchandise and the ability to subscribe to the site as a 'premium' user in order
 to see premium content.

In terms of premium content, this allows a registered site user to subscribe to one of four different prices plans (1,
3, 6 or 12 months at a time) and upgrade their account. It also allows a new user to both register and subscribe at the
same time. For users who are registering for the first time, the user registration form from the users app is imported
to be used alongside the subscription form. The subscription form is derived from the payment form for the
merchandise store, with an extra field included to allow the user to choose their preferred payment plan before
endering card details to complete the upgrade. The payments are handled by Stripe and the user has the ability to
  cancel their plan at any time to prevent another payment from being taken. If this is done, then access is retained
  until the end of the current billing period.

All the models in the store app relate to ordering merchandise. There is a model which defines each product which a user
 might wish to purchase, for example a replica home jersey for a given team. Another model then allows for a number of
 different size options for each product. These must be tracked separately in order to keep accurate records of stock
 levels for each size. When a user views a particular product, a form allows them to add the product to their shopping
 cart. A list of available sizes for that product is shown, along with a field to select a quantity. In order to be able
  to add items, the user must be logged in to the site.

When the user adds a product for the first time, their shopping cart is created with a status of 'Pending'. If a user
already has a pending cart when they try to add an item, it will be placed in that existing cart. If the user has no
pending cart, a new one is set up for them. The user has the opportunity to change the quantity of each individual items
 in their cart or to delete items. If deleting an item would leave a cart empty, the cart is also deleted and the user
 will then be allocated a new one the next time they add a product.

As items are added and deleted or quantities changed, the stock level of the specific size option is altered
 accordingly. This is done to ensure that items are  allocated as soon as they go into a cart and cannot be bought by
 any other user unless they are first removed. The running total of the user's order is calculated each time an item is
 added or deleted, with a calculation being made to check whether the new total exceeds £50. This is done to allow postage charges to be removed for orders above that
 amount.

Payment works in much the same was as the subscription for premium content. The user is however also required to enter a
 delivery address. In the users app the user may have already set a default address, although this is not compulsory. If
  an address is set, it will appear by default in the address form, although the user can change it if they wish. A
  checkbox is provided to give the user the option to set the address they have entered as 'default'. If they choose
  this option, the address will be stored on their profile. Otherwise, it is allocated only to their current shopping
  cart. The same payment form is used to send card details to Stripe and the user is then given confirmation that their
  order was placed. When this is done, the status of the cart is changed from 'Pending' to 'Received'. This means that
  if the user then tries to add more items, a new cart will be created for them.

### Forum App

The forum app is a relatively straight forward message board facility, allowing site users to create threads and
contribute posts to existing threads. The app contains four models. The first of these, the section model, divides the
forum up allowing the individual boards to be categorised. The board model allocates each subject to a particular
section, and the boards are separated on this basis on the forum home page. When a new thread is created, it is then
allocated to the board within which it was created. Likewise, when a new post is added it is allocated to the correct
thread. Both the thread model and the post model allocate a user, allowing posts to be credited to the right person and
keeping a track of who originally created the thread.

Additionally, the thread model records when it was created and also the time of the most recent post. This is updated
whenever a new post is added and is also recalculated when a post is deleted, in case the deleted post was the last one.
 This ensures that the recorded time and date is always that of the most recent remaining post. The post model functions
  in much the same way as the comment model in the news app. The use who has posted the comment, or the admin superuser,
   are able to edit the comment or delete it. JavaScript is used to confirm that the user does indeed wish to delete the
    comment. Two forms are used to create the threads and the posts. When a new thread is being created, both forms are
    used - one to create the thread and the other to create the initial post.

In the template files for the forum app, users can see an overview of all boards with a count of threads and posts in
each, while for each individual board a list of threads is shown with details of which user opened the thread and when
the last post was made. Pagination is used to limit the number visible at a time to 10. This is also done within each
individual thread to limit the number of posts per page in the same way. A post counter is used in each post to show
where it fits into the overall discussion. Posts are shown in chronological order with the oldest appearing first, so
that the discussion can be read in order, but threads are listed with the most recently updated at the top so that the
user can see where the newest discussions are taking place.

Recent discussions can also be seen in the sidebar on larger sized screens, where the ten most recent posts are listed
and linked.

### Users App

The users app contains a single model which overrides the default Django user model. It incorporates all the same fields
 as the default model, but adds a number of additional fields to provide more information about the user. These are all
 optional fields, allowing the user to control how much information they provide beyond the basic name, username, email
 address and password. Fields in the user record can by changed at any time by the user editing their profile.

Users have the option to choose a team as their favourite, giving customised news on the home page and highlighting
the chosen team in the league standings and the scores in the sidebar. Users can also set a profile picture which is
displayed if they comment on a news item or contribute to a thread in the forum. If the user has no picture set but does
 have a favourite team chosen, the logo of their chosen team will be used in place of a profile picture. If neither are
 set, a default picture will be used instead.

The user model also contains fields for a default address, which can be used when ordering items through the store. This
 can not be set by the user on registration but can be added using the profile editing facility. Fields regarding
 subscription status are blank by default unless the user has subscribed to premium content on registration. Otherwise
 they will be set when the account is upgraded. A Stripe ID is used to identify the author and the date when the user's
 subscription is due to end is set here. There is also a setting for whether or not the user's subscription will renew
 automatically, which it may not if the user has chosen to cancel.

Another important field is the ability to set a profile to private, as logged in users can view each other's profiles. A profile is public by default, but a user can choose to hid all but their user name. It is
 important to note that even in a public profile, information such as the user's e-mail address, order history and
 subscription status will remain private. These are visible to the user themselves, but not to other users.

The registration and profile editing forms are both model forms based on the user model. Separate forms are required
because additional authentication is not required to edit a profile once the user has logged in. Another form is used to
 give the user the option to change their password. This requires the user to provide their current password and then
 choose and confirm a new one, before re-authenticating and logging the user in again with their new password. The login
  form is also defined in the user app, requiring the user to provide their username and password.

A user's profile page gives a great deal of information about them and their account. Their username and real name are
shown, although the real name is not included when the user is viewing their own profile. Dates of registration and last
 login are included, as the registered e-mail address. The user can view the status of their account, whether standard
 or premium, and a link to upgrade is provided for standard users. For premium users, the next automatic renewal date is
  shown alongside a link to cancel this if required. As with other cancellations or deletions on the site, JavaScript
  is used to prompt for confirmation before completing the cancellation. Users can also view their purchase history from
   the store through their own profile page.

When visiting the profile of another user, it is possible to see if that person is an authorised blogger and link to
their blog page if so. Counts are shown of the user's contributions to the site in terms of forum threads and posts as
well as comments on news stories. The most recent five such contributions are linked from the profile page. Because
different information is required depending on whether the user is viewing their own profile or somebody else's, two
separate views are used to render the profile template.

## Deployment

A GitHub repository was created for the project right at the beginning of development, then once the basic structure of
 the site was in place the project was then further deployed to Heroku. This was done to enable easy testing on
 different devices, particularly mobile devices running the Android operating system. Although not every commit to
 GitHub was deployed to Heroku, the Heroku app was updated regularly when significant new functionality or design was
 added in order to facilitate continued manual testing.

## Testing

Much of the site development was done on a Windows PC using the Chrome browser, and making use of the developer tools to
 view at different screen sizes and troubleshoot any problems which may occur. Testing the project was done by a mixture
  of automatic and manual methods. Automatic tests were written within the Django project to test the URLs and views, as
   well as testing validation for all the forms which are included on the site. In total, this testing covers 67% of all
    the lines of code in the project. Further testing was done manually, using different browsers such as Firefox and
    difference operating systems in terms of using Android devices. The project was tested by navigating the links
    on the site and entering a variety of data into the forms, ensuring that the site navigation worked as intended and
    that the forms were accepted with correct inputs and rejected when wrong entries were made, such as passwords which did not match
    on registration.