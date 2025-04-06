"use strict";


// Get the dropdown element
const dropdown = document.querySelector('.dropdown');

// Add an event listener to toggle the dropdown menu on click
dropdown.addEventListener('click', function(event) {
    // Prevent the event from bubbling up
    event.stopPropagation();

    // Toggle the 'active' class on the dropdown to show/hide the menu
    this.classList.toggle('active');
});

// Close the dropdown if the user clicks outside of it
window.addEventListener('click', function(event) {
    if (!dropdown.contains(event.target)) {
        dropdown.classList.remove('active');
    }
});