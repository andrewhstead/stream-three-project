// Function to allow the user to toggle the navigation menu on and off in the default stylesheet.
$('#menu-button').click(function(){
    $('#main-menu').slideToggle(1000);
});

// Function to allow the user to toggle the comments on and off.
$('#show-hide').click(function(){
    $('#comments').fadeToggle(500);
});