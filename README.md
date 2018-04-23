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
	* [News App](#news-app)
	* [Games App](#games-app)
	* [Teams App](#teams-app)
	* [Store App](#store-app)
	* [Forum App](#forum-app)
	* [Users App](#users-app)
4. [Use of Data](#use-of-data)
5. [Deployment](#deployment)
6. [Testing](#testing)
7. [Issues](#issues)

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
outline [Privacy Policy](https://privacypolicytemplate.net/) and [Terms and Conditions](https://termsandconditionsgenerator.com/) document for the site.

## Back End Development

In addition to a 'Home' app which contains the template for the site's Home Page plus an HTML include for use across the
 site, there are six further apps which make up the project.

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
 comment or the administration superuser are permitted to edit a given comment.

### Scores App

### Teams App

### Store App

### Forum App

### Users App

## Use of Data

## Deployment

A GitHub repository was created for the project right at the beginning of development, then once the basic structure of
 the site was in place the project was then further deployed to Heroku. This was done to enable easy testing on
 different devices, particularly mobile devices running the Android operating system. Although not every commit to
 GitHub was deployed to Heroku, the Heroku app was updated regularly when significant new functionality or design was
 added in order to facilitate continued manual testing.

## Testing

Testing the project was done by a mixture of automatic and manual methods. Automatic tests were written within the
Django project to test the URLs and views, as well as testing validation for all the forms which are included on the
site. In total, this testing covers 67% of all the lines of code in the project. Further testing was done manually, by
navigating the links on the site and entering a variety of data into the forms, ensuring that the site navigation worked
 as intended and that the forms were accepted with correct inputs and rejected when wrong entries were made, such as
 passwords which did not match on registration.

## Issues