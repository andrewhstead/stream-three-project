/* Variable set to 0 to ensure the slideshow starts with the first item in the array.
Initial value set outside the function so as not to interfere with
incremented value when the function is running. */
var leadStory = 0;
var interval = setInterval(newsFader,10000);

function restartTimer(){
		clearInterval(interval);
		setInterval(newsFader,10000);
}

/* Function to run the image slider. */
function newsFader(item) {

	if (item !== undefined) {
		leadStory = item - 1;
		restartTimer();
	}

	/* Create an array containing all the slider image elements. */
	var newsFader = document.getElementsByClassName("banner-story");
	var newsBlobs = document.getElementsByClassName("news-blob");

	/* Hide each element by giving it the class 'hiddenContent'and ensuring no elements have the class 'blockContent'. */
	for (var i = 0; i < newsFader.length; i++) {
		newsFader[i].classList.add("hidden");
		newsFader[i].classList.remove("active");
		newsBlobs[i].classList.add("default-blob");
		newsBlobs[i].classList.remove("active-blob");
	}

	/* If the currentImage variable has passed the end of the array, return it to the beginning. */
	if (leadStory >= newsFader.length) {
		leadStory = 0;
	}

	/* Display the current image by removing the class 'hiddenContent'. Add the class 'blockContent' to ensure that the image displays as a block element. */
	newsFader[leadStory].classList.remove("hidden");
	newsFader[leadStory].classList.add("active");
	newsBlobs[leadStory].classList.remove("default-blob");
	newsBlobs[leadStory].classList.add("active-blob");

	/* Increment the currentImage variable in preparation for the next transition. */
	leadStory++;
}

/* Run the function on page load and then again at 10 second intervals. */
newsFader();