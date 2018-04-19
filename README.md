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

## Front End Development

### Responsive Design

The site was designed according mobile-first principles, with most of the functionality set up using the default layout
for devices with a width of 400 pixels or fewer. Break points are set at 400 and 800 pixels, with a maximum width on the
 page content set at 1200 pixels. For devices wider than this, the header and footer continue to expand to fill the
 viewport but there will be whitespace at either side of the content, which is centred on the page. The site is designed
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

### Page Styling

### Use of Custom JavaScript

## Back End Development

### Django Apps

### Forms

## External JavaScript Libraries

## Use of Data

## Deployment

## Testing

## Issues