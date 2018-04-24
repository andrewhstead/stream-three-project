// Function to allow the user to toggle the navigation menu on and off in the default stylesheet.
$('#menu-button').click(function(){
    $('#main-menu').slideToggle(1000);
});

// Function to allow the user to toggle the comments on and off.
$('#show-hide').click(function(){
    $('#comments').fadeToggle(500);
});

// Functions to allow scrolling of hidden overflow on sponsor logos.
var leftOffset = parseInt($('#logo-wrapper').css('left'));
var rightOffset = parseInt($('#logo-wrapper').css('right'));

// Scroll to view logos on the right by moving the logos to the left.
$('#right-scroll').click(function(){
    if (leftOffset >= -500) {
        $("#logo-wrapper").animate({
            left: '-=50px',
            right: '+=50px'
        });
        leftOffset -= 50;
        rightOffset += 50;
    }
});

// Scroll to view logos on the left by moving the logos to the right.
$('#left-scroll').click(function(){
    if (leftOffset < 0) {
        $("#logo-wrapper").animate({
            left: '+=50px',
            right: '-=50px'
        });
        leftOffset += 50;
        rightOffset -= 50;
    }
});

// Function to remove message alerts after five seconds.
function messageRemove() {
    setTimeout(
        function() {
            document.getElementById('messages').classList.add('hidden');
        }, 5000);
}
messageRemove();

// Pop-up function to ask for confirmation or give information.
function confirmationAlert(item) {
    if (item !== undefined) {
        document.getElementById('wrapper-' + item).classList.toggle('activate');
        document.getElementById('alert-' + item).classList.toggle('activate');
    } else {
        document.getElementById('wrapper').classList.toggle('activate');
        document.getElementById('alert').classList.toggle('activate');
    }
}
