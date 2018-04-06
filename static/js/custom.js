// Function to allow the user to toggle the navigation menu on and off in the default stylesheet.
$('#menu-button').click(function(){
    $('#main-menu').slideToggle(1000);
});

// Function to allow the user to toggle the comments on and off.
$('#show-hide').click(function(){
    $('#comments').fadeToggle(500);
});

// Pop-up function to ask for confirmation or give information.
$('.alert-link').click(function(){
    $('.popup-wrapper').fadeToggle(100);
    $('.alert-message').fadeToggle(100);
});

function messageRemove() {
    setTimeout(
        function() {
            document.getElementById('messages').classList.add('hidden');
        }, 5000);
}

messageRemove();
