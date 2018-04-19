# Code Institute Stream Three Project

This is a project website for the Code Institute Full Stack Web Development course Stream Three. The project is a
website for a sports league, and has been constructed around a fictional baseball league, the data for which was
generated using the game "Out of the Park Baseball 18". The site is built using the Django framework and incorporates
elements which are common to sports league websites, such as news stories, game results and fixtures, information about
teams, and the ability for fans to interact and purchase premium content or merchandise. The site is presented as it
would look midway through a season, with data generated up to early July in the 2018 season.

## Contents
1. [Planning](#planning)
2. [Front End Development](#front-end-development)
3. [Back End Development](#back-end-development)
4. [External Libraries](#external-libraries)
5. [Use of Data](#use-of-data)
6. [Deployment](#deployment)
7. [Testing](#testing)
8. [Issues](#issues)

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

### Use of Custom JavaScript

The site makes use of both jQuery and plain JavaScript. Plain JavaScript is used to remove success or failure messages after five seconds on the screen, while there is also a
script which allow the user to confirm any request to delete content from the site. This applies to blog posts, forum
posts, comments and items in shopping carts. Without this it would be possible to accidentally delete content with one
click.

Major use of JavaScript is made on the Home Page with the scrolling news headline effect. The seven most recent
news headlines are included with a banner image, and each is represented underneath by a blue dot. The latest item is
displayed by default, and every ten seconds the image transitions to the next item. The blue dots highlight the
currently displayed item. The user is able to select any item using the blue dots, and when a selection is made the ten
second counter is restarted.

### External JavaScript Libraries

Several simple jQuery functions are used to provide additional functionality. On devices below 800 pixels in width, the
main site navigation menu is hidden by default and can be displayed as a drop down from the header by clicking the menu icon. This can then be toggled on and off using jQuery. A similar effect is
used to allow users to hide comments on news stories or blog posts should they so desire. Further use of jQuery allows
the user to scroll through the league sponsor logos on the home page. Those images are contained in a div which runs off
 the page to the right, with the overflow hidden. The jQuery allows the div to be moved to the left or right as required.

## Back End Development

### Django Apps

### Forms

## Use of Data

## Deployment

## Testing

## Issues