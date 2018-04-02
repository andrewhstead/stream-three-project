// Function to allow the user to toggle the navigation menu on and off in the default stylesheet.
$('#menu-button').click(function(){
    $('#main-menu').slideToggle(1000);
});

// Function to allow the user to toggle the comments on and off.
$('#show-hide').click(function(){
    $('#comments').fadeToggle(500);
});

// Function to allow the user to confirm that they wish to delete a post or a comment.
$('.delete-link').click(function(){
    $('.lights-down').fadeToggle(100);
    $('.delete-confirm').fadeToggle(100);
});