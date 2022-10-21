![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

Welcome MandyHole,

This is the Code Institute student template for deploying your third portfolio project, the Python command-line project. The last update to this file was: **August 17, 2021**

## Reminders

* Your code must be placed in the `run.py` file
* Your dependencies must be placed in the `requirements.txt` file
* Do not edit any of the other files or your code may not deploy properly

## Creating the Heroku app

When you create the app, you will need to add two buildpacks from the _Settings_ tab. The ordering is as follows:

1. `heroku/python`
2. `heroku/nodejs`

You must then create a _Config Var_ called `PORT`. Set this to `8000`

If you have credentials, such as in the Love Sandwiches project, you must create another _Config Var_ called `CREDS` and paste the JSON into the value field.

Connect your GitHub repository and deploy as normal.

## Constraints

The deployment terminal is set to 80 columns by 24 rows. That means that each line of text needs to be 80 characters or less otherwise it will be wrapped onto a second line.

-----
Happy coding!


Open Day Planner

Overview

This site is designed specifically to help my colleagues and me to better plan the marketing of certain events we offer through our work. Adding the type and date of the event will result in a Google spreadsheet for the event (containing a Tasks planner and other worksheets to update) as well as a series of calendar reminders that get entered in at a date relative to the date of the event itself. Whilst the main content is overall designed to be specific to my work, for the purpose of this project a few modications were made to 1 maintain anonymity and 2 not have calendar entries and spreadsheets added by external site users; for example, instead of adding attendees from my work, the user needs to enter their email address instead.

Should someone else want to use it to plan their event, modifications to the types of events allowed, panda dataframes, and calendar descriptions/timeframes would enable them to create their own useful planning system.


being rehomed
not have the training they need to live up to their potential.
Different sections of the website shown on mobile, desktop and tablet (portrait and landscape view)

Features

Existing Features

Favicon: The blue pawprint is lifted from the logo – it is designed to be clear and easily recognisable in a browser bar if people move to another page as well as provide site continuity.

blue paw shown in Chrome browser

Logo: The logo adds continuity through the site as its appearance matches the heading fonts and colours used throughout the website. The pawprint in the logo matches the favicon. (The logo can be seen in the menu screenshot below.)

Menu: The full responsive menu guides people easily through the three pages of the site: Home, Pros & Cons and Tips. For mobiles, the menu becomes the widely recognised ‘hamburger menu” matching the colour scheme of the site. It’s fixed to the top of the page so that it is easily accessible wherever people are at on the site.

menu at 696px, 697px, and expanded hamburger menu

Hero Headers: These are designed to engage the viewer when they first come onto each page with animation, a cute photo of a puppy and a clear indication of the information found on the page. The mobile version has an opacity covering the entire image as the content took up a large proportion of the image.

Hero appearance at two different widths (mobile and tablet)

Essential Qualifications: These provide the bare minimum requirements for any responsible dog owner so that is why they are given such prominence on the website. They are broken down into three bite-size chunks to make them easier to read.

Essential info at three different widths

About Me:This section is meant to help people identify with the website author and know that they are not alone as well as give them confidence that if they are willing to commit to doing it properly, Labradors are a great option – even for people who aren’t naturally drawn to animals. As it looks long on the mobile version and isn’t essential, there is a “Read More” option for smaller viewports. As this is not key information, it is given a semantic tag of an aside.

About Me section in mobile form with 'read more' button

Ask a question: This is a friendly looking form with an inviting ‘Ask Away’ submit button to encourage people to get in touch if they are unsure of anything and want some advice.

Example of a form at the bottom of the page at three different widths to show responsiveness

Pros and Cons: This is to help people assess the Pros and Cons of having a Labrador versus having other breeds (or no dog at all). I knew someone who purchased a Labrador to help her feel safe and be a ‘guard dog’ of sorts: this is completely the wrote type of dog for that! She ultimately gave her Labrador to a friend; it is happy and well cared for, but it is this type of misconception that this site hopes to address. This section is placed second because it is assuming that people meet the ‘Essential Qualifications’ for having a dog and are now determining if this breed (or any dog) is really right for them.

Screenshots of the Pros and Cons in two different layouts: two columns and one column

Tips: This section came last as it is assuming that people have ultimately come to the conclusion that Labradors are potentially right for them. However, the site also wants to address that to be a responsible dog owner requires training (so that they won’t decide to give up the dog later due to behaviour issues): early and consistent training is key to having a happy, healthy and successful dog! The tips are broken down into small sections in coloured boxes with columns broken up by images to make them appealing and easy to read. Links to reputable sites provide additional research opportunities, and audio and video options provide the viewer to experience content with media, rather than just by reading.

Screenshots of the Tips content in three different layouts: three columns, two columns and one column

Quotes Slideshow: This shows a mixture of quotes about the joys of having a dog and the need for responsibility. It is designed to show a glimpse of the next quote so the viewer knows to slide to see more.

Screenshot of the first quote and glimpse of the second in the slideshow on the Pros/Cons page


Features left to implement
Blog/Message Board: In the future, I would add a page with a blog where I could write updates and post photos about my training journey with my Labrador puppy Daisy and allow others to submit their stories/photos for inclusion.

New image for Pros/Cons form background image: Whilst this image is sized properly, I realised belatedly that it wasn't quite as clear as I would have liked due to the quality of the original photo so I ideally would find or take another image that fit the size requirements.

Testing
Layout:
I originally designed the homepage using the theories taught in the course (using floats, display: none, column widths/heights). With a rather complicated design of double column intro and an aside, it was very difficult to look good without an unmanageable number of breakpoints; to have my content and photos line up, I had to give each div an arbitrary size, which meant that, depending on media widths, I would have had massive gaps between my columns. Also, I was having to have extra filler images appear or be hidden depending on how my content was split so there wasn’t a massive gap in a column. I also would have to check the height for various breakpoints to make sure the columns were the same size. Finally, as my aside appeared in the wrong place in the mobile view (under the qualifications intro), I then had to hide/show the original/duplicate depending on the media width. It was all very messy and complicated, and I knew there had to be a better way...

Upon recommendation from my Mentor, I tried flex-box for my pros/cons page. Researching that also let me to grid css, which I implemented on my tips page. Both were remarkably easier to use, and my gaps between both pages were consistent and the pages looked much more professional. Upon reflection, I decided to redo my homepage with grid to ensure consistency in gaps/margins through the site. Unfortunately, doing it retrospectively caused a lot more effort and took a lot of experimentation to get it right, removing the extra divs, images and formatting that were no longer required.

Hamburger menu:
I discovered that this would not work properly if the user had already scrolled down the page. Working with my mentor, we discovered the heading needed to be fixed as opposed to sticky.

Media queries:
To make the site responsive, I went from three to two columns on both the home and Tips pages for a smaller screen/tablet, and then down again to a one column layout for mobile. For the pros/cons page, it went from a two column to a one column layout for mobile. I also had to add alternate mobile images for some background images to ensure that the dog’s face was shown.

Consistency:
As I reviewed the site, I realised that there was a bit of inconsistency in various elements across the site, which I sought to address by changing the inconsistent elements to be stylised by classes which I then implemented throughout the site, removing only elements that had to change (e.g., the background image on the hero) to be used in specific ids/classes. I used this approach for the headings, buttons, top hero area and form areas (and as I mentioned earlier, redoing the homepage to ensure consistency with row and column gaps/margins).

Google Fonts:
As I reviewed the deployed site on my mobile, I realised that it wasn't recognising the Google Chewy font family and instead used a cursive. I realised that the link to the Google fonts was at the bottom of the CSS file instead of the top so I moved it to the top, which fixed the issue. To be on the safe side, I also changed the alternative font family to serif instead of cursive in case a font rendering issues happened to occur.

Incorrectly sized image and missing description:
As I reviewed the site using Lighthouse, I realised one image was sized to 4000px (I meant to do 400px) which slowed down the website as it was 1.7MB. I resized the image to 300px. I also realised that it wasn't picking up the meta description for the Tips page due to a typo so I fixed that.

Colour contrast:
When initially selecting colours, I utilised WebAIM's colour contrast checker to ensure the background colours I used were suitable for dark colour text at a normal size. I then found the lightest black shade I could that still met AAA standards for normal text to use as my main font colour. I put the blue/yellow combination into a colour wheel to find a complementary third colour: a shade of magenta pink. As it did not meet colour contrast standards for text, I used it solely for decoration.

Validator Testing
HTML: No errors were returned when passing through the official W3C validator
CSS: No errors were found when passing through the official (Jigsaw) validator
Unfixed Bugs
Form: The form submissions are currently set up to go to a form dump area on the Code Institute website. Ideally, these would be sent to my email so that I could respond accordingly, have reCAPTCHA functionality to weed out spam and an auto response/message so that the user knows that the form was successfully submitted. They were not fixed as I do not have a database capable of collecting data at the moment.

What I Would Have Done Differently
Git Add/Commit: I sometimes found myself lost on a mission and would realise that I should have done an add/commit sooner than I did, and then tried to remember what it was I had done! I also sometimes thought I’d committed something and realised a typo of some sort meant it didn’t go through, and I’d often have to kill of a terminal and restart and then have a commit taking both messages into account. Unfortunately, this is not something that can be fixed retrospectively, but it is something I am going to be more mindful of in future.

Deployment
The site was deployed to GitHub pages. The steps to deploy are as follows:
In the GitHub repository, navigate to the Settings tab
From the source section drop-down menu, select the Master Branch
Once the master branch has been selected, the page will be automatically refreshed with a detailed ribbon display to indicate the successful deployment.
The live link can be found here - https://mandyhole.github.io/love-a-lab/
Credits:
Content
The content for this website drew on my personal experience of owning a Labrador Retriever and my training from trainers through the charity Dogs for Good.

I also included several external links to reputable sources for more information that I think every potential owner should know, including:

PDSA
The Kennel Club
The Dogs Trust
iframe code for Marley and Me Trailer: YouTube

Quotes about dogs / labradors:

Labrador Loving Soul
Good Reads
The Labrador Site
Red Bubble website
Code
Hamburger style menu: Log Rocket

Read More/ Read Less Button (used in Homepage About Me aside in mobile view): W3Schools

Flexbox:

YouTube
W3Schools
CSS Tricks
CSS Grids:

General concept for using Grids: W3Schools

Code for creating equal-width columns in CSS grid: CSS Tricks

Hero Animation (Page Headers): Code Institute Love Running source code

Slideshow for quotes: CSS Tricks

Media
Images on Tips page: Pexels

Platform to create an ogg and mp3 versions of my mp4 file: Convertio

Chewy and Merriweather fonts used throughout the site: Google Fonts

Icons used for my favicon, logo, homepage boxes and Pros/Cons boxes: Font Awesome

Platform for inserting and creating a Favicon image: Favicon Generator

Platform for resizing images: Adobe PhotoShop

Platform for creating logo: Adobe Illustrator

Application to create audio version only of my movie of a dog making snuffling sounds: Quicktime

About
If you're asking yourself "Should I buy a Labrador?" then you should get the perspective of a non-animal-loving Labrador owner.

Resources
 Readme
Stars
 0 stars
Watchers
 0 watching
Forks
 1 fork
Releases
No releases published
Packages
No packages published
Languages
HTML
64.7%
 
CSS
27.2%
 
Dockerfile
8.1%
Footer
© 2022 GitHub, Inc.
Footer navigation
Terms
Privacy
Security
Status
