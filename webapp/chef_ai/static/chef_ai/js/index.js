let i = 0;
let placeholder = "";
const txt = "Search ingredients...";
const speed = 300;

function type() {
    placeholder += txt.charAt(i);
    document.getElementById('searchInput').setAttribute("placeholder", placeholder);
    i++;
    setTimeout(type, speed);
}

type();

let plusButton = document.getElementById("increment_recipes");
let minusButton = document.getElementById("decrement_recipes");
let numRecipesDisplay = document.getElementById("recipe_amount");

numRecipesDisplay.value=1;

plusButton.addEventListener("click", () =>{
    numRecipesDisplay.value =Number(numRecipesDisplay.value)+1; 

});
minusButton.addEventListener("click", () =>{
    numRecipesDisplay.value = Math.max(1, Number(numRecipesDisplay.value)-1);
});


const ingredientCategories = {
    pantryEssentials: [
        'Rice', 'Pasta', 'Flour', 'Sugar',
        'Salt', 'Olive Oil', 'Vinegar',
        'Bread', 'Cereal'
    ],
    spices: [
        'Black Pepper', 'Paprika', 'Cumin',
        'Oregano', 'Garlic Powder', 'Cinnamon',
        'Turmeric', 'Chili Powder', 'Basil'
    ],
    vegetablesGreens: [
        'Onions', 'Tomatoes', 'Spinach',
        'Carrots', 'Broccoli', 'Lettuce',
        'Potato', 'Bell Pepper', 'Cucumber'
    ]
};

function createCategoryItems() {
    Object.keys(ingredientCategories).forEach(categoryKey => {
        const categoryContainer = document.querySelector(`#${categoryKey} .category-items`);

        if (!categoryContainer) return; // Prevent errors if container is missing

        ingredientCategories[categoryKey].forEach(item => {
            const itemWrapper = document.createElement('div');
            itemWrapper.classList.add('category-item');

            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.id = `${categoryKey}-${item.toLowerCase().replace(/\s+/g, '-')}`;
            checkbox.name = item;

            const label = document.createElement('label');
            label.htmlFor = checkbox.id;
            label.textContent = item;

            itemWrapper.appendChild(checkbox);
            itemWrapper.appendChild(label);

            categoryContainer.appendChild(itemWrapper);
        });
    });
}

document.addEventListener('DOMContentLoaded', () => {
    // For tracking highlighted sugguestions
    let selectedIndex = -1; 
    let suggestions = [];
    
    const chefItUpBtn = document.getElementById('chefItUpBtn');
    const mainContent = document.querySelector('.content');
    const searchSection = document.getElementById('searchSection');
    const searchInput = document.getElementById('searchInput');
    const selectedItemsContainer = document.getElementById('selectedItemsContainer');
    const selectedItemsDiv = document.getElementById('selectedItems');
    const video = document.querySelector('.back-video');
    const form = document.querySelector("form");



    form.addEventListener("submit", (e) => {
        if (document.activeElement === searchInput) {
            e.preventDefault(); // Block submission if user is typing and hits enter in the search bar
        }
    });

    createCategoryItems(); // Generate ingredient checkboxes

    // Show search section when "Let's Chef it up!" is clicked
    chefItUpBtn.addEventListener('click', (e) => {
        e.preventDefault();
        const img = document.getElementById('bg-img');

        mainContent.style.display = 'none';
        searchSection.style.display = 'block';

        searchInput.focus();

        video.pause();
        video.currentTime = video.duration;
        video.style.display = 'none';
        img.style.backgroundImage = `url('${STATIC_IMAGE}')`;

    });

    // Search and select ingredients
    const suggestionBox = document.getElementById("searchSuggestions");
    searchInput.addEventListener('keyup', async (event) => {
        if (["ArrowUp", "ArrowDown", "Enter"].includes(event.key)) return;

        const query = searchInput.value.trim(); // Grabs the user's input and remove any extra spaces
        // Ignores unneccessary inputs
        if (query.length < 2) {
            suggestionBox.style.display = "none";
            return;
        }

        // Sends a request to the backend
        try {
            const response = await fetch(`/search/?q=${encodeURIComponent(query)}`);
            const data = await response.json();

            suggestionBox.innerHTML = '';
            selectedIndex = -1;
            suggestions = [];


            if (data.results.length > 0) {
                data.results.forEach(result => {
                    const suggestion = document.createElement("div"); // To make each match as a clickable div
                    suggestion.textContent = result;
                    suggestion.classList.add("suggestion-ingredient");

                    //adds button to selected ingredients
                    suggestion.addEventListener("click", () => {
                        let matched = false;
                        Object.keys(ingredientCategories).forEach(categoryKey => { // Trys to match with predefined ingredientCategories
                            ingredientCategories[categoryKey].forEach(item => {
                                //First checks if item exists in the predefines list of ingredients
                                // Selects the checkbox and adds to UI
                                if (item.toLowerCase() === result.toLowerCase()) {
                                    const checkboxId = `${categoryKey}-${item.toLowerCase().replace(/\s+/g, '-')}`;
                                    const checkbox = document.getElementById(checkboxId);
                                    if (checkbox && !checkbox.checked) {
                                        checkbox.checked = true;
                                        addSelectedItem(item, categoryKey);
                                        matched = true;
                                    }
                                }
                                // else {
                                //     //add item since it exists in db
                                //     addSelectedItem(data.results[0], data.results[0]);
                                // }
                            });
                        });
                        // Treats non-matches in the ingredientCategories as a valid DB result
                        if (!matched) {
                            addSelectedItem(result, "db");
                        }

                        // Clears input and hides dropdown after user clicks a suggestion
                        searchInput.value = '';
                        suggestionBox.innerHTML = '';
                        suggestionBox.style.display = "none";
                    });
                    suggestionBox.appendChild(suggestion);
                    suggestions.push(suggestion); // Stores suggestion for keyboard use
                });
                suggestionBox.style.display = "block";
            } else {
                suggestionBox.style.display = "none";
            }
        } catch (err) {
            console.error("Search error:", err);
            suggestionBox.style.display = "none";
        }
    });

    //Script that scans images for ingredients
    document.getElementById('scan-btn').addEventListener('click', () => {
        const formData = new FormData();
        const images = document.getElementById('image-upload-input').files;
    
        for (let i = 0; i < images.length; i++) {
            formData.append('images', images[i]);
        }
    
        fetch('/scan-images/', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            const ingredients = data.ingredients;
            const categoryKey = 'detected'; // Or however you want to categorize
    
            ingredients.forEach(item => {
                addSelectedItem(item, categoryKey);
                console.log("added item: ",item);
            });
        })
        .catch(error => console.error('Error:', error));
    });

    // Highlights the currently selected suggestion based on selectedIndex
    function updateHighlight() {
        suggestions.forEach((s, index) => {
            if (index === selectedIndex) {
                s.classList.add("highlighted");
                s.scrollIntoView({ block: "nearest", behavior: "smooth" });
            } else {
                s.classList.remove("highlighted");
            }
        })
    }

    searchInput.addEventListener("keydown", (event) => {
        if (suggestionBox.style.display === "none") return;

        if (event.key === "ArrowDown") {
            event.preventDefault();
            selectedIndex = (selectedIndex + 1) % suggestions.length; // Loops to first after last
            updateHighlight();
        } else if (event.key === "ArrowUp") {
            event.preventDefault();
            selectedIndex = (selectedIndex - 1 + suggestions.length) % suggestions.length; // Loops to last from first
            updateHighlight();
        } else if (event.key === "Enter") {
            event.preventDefault();
            const inputValue = searchInput.value.trim();
            if (selectedIndex >= 0 && suggestions[selectedIndex]) {
                suggestions[selectedIndex].click(); // Triggers click on highlighted suggestion
            }else if(inputValue.length>=2){
                let matched = false;
                Object.keys(ingredientCategories).forEach(categoryKey => {
                    ingredientCategories[categoryKey].forEach(item => {
                        if (item.toLowerCase() === inputValue.toLowerCase()) {
                            const checkboxId = `${categoryKey}-${item.toLowerCase().replace(/\s+/g, '-')}`;
                            const checkbox = document.getElementById(checkboxId);
                            if (checkbox && !checkbox.checked) {
                                checkbox.checked = true;
                                addSelectedItem(item, categoryKey);
                                matched = true;
                            }
                        }
                    });
                    // If not matched, assume it's a valid DB result and add it
                    if (!matched) {
                        addSelectedItem(inputValue, 'db');
                    }

                    // Clear input and hide suggestion box
                    searchInput.value = '';
                    suggestionBox.innerHTML = '';
                    suggestionBox.style.display = 'none';
                })
            }
        }  
    })

    // Hides the dropdown if user clicks anywhere on the page
    document.addEventListener("click", (e) => {
        if (!searchInput.contains(e.target) && !suggestionBox.contains(e.target)) {
            suggestionBox.style.display = "none";
        }
    });

    //allows the entire ingredient div to be clickable
    document.querySelectorAll('.category-item').forEach(categoryItem => {
        categoryItem.addEventListener('click', (e) => {
            // Prevent default label behavior
            e.preventDefault();
    
            const checkbox = categoryItem.querySelector('input[type="checkbox"]');
            if (!checkbox) return;
    
            // Toggle checkbox manually
            checkbox.checked = !checkbox.checked;
    
            const item = checkbox.name;
            const categoryKey = checkbox.id.split('-')[0];
            const selectedId = `selected-${item.toLowerCase().replace(/\s+/g, '-')}`;
            const alreadyAdded = document.getElementById(selectedId);
    
            if (checkbox.checked && !alreadyAdded) {
                addSelectedItem(item, categoryKey);
                categoryItem.classList.add("selected");
            } else if (!checkbox.checked && alreadyAdded) {
                console.log("removing the item from box: ",item)
                removeSelectedItem(item);
                categoryItem.classList.remove("selected");
            }
            console.log("at bottom of querythinggy");
        });
    });

    

    // Function to add selected item to the top div
    function addSelectedItem(item, categoryKey) {
        selectedItemsContainer.style.display = 'block'; // Show container when items are added

        // Prevent duplicates
        if (document.getElementById(`selected-${item.toLowerCase().replace(/\s+/g, '-')}`)) return;
        console.log(item, categoryKey);
        // Create a div for the selected ingredient
        const itemDiv = document.createElement('div');
        itemDiv.classList.add('selected-item');
        itemDiv.id = `selected-${item.toLowerCase().replace(/\s+/g, '-')}`;

        // Create the quantity container (wraps the input field)
        const quantityContainer = document.createElement('div');
        quantityContainer.classList.add('quantity-container');

        const quantityInput = document.createElement('input');
        quantityInput.type = 'text';
        quantityInput.placeholder = 'Quantity';
        quantityInput.id = `quantity-${item.toLowerCase().replace(/\s+/g, '-')}`;

        quantityContainer.appendChild(quantityInput);

        const itemName = document.createElement('span');

        itemName.textContent = item;
        itemName.classList.add('ingredient-name');

        // Append the name and quantity container to the item div
        itemDiv.appendChild(itemName);
        itemDiv.appendChild(quantityContainer);


        // Add remove button
        const removeBtn = document.createElement('button');
        removeBtn.textContent = '✖';
        removeBtn.classList.add('remove-btn');
        removeBtn.addEventListener('click', () => {
            removeSelectedItem(item);

            const checkbox = document.getElementById(`${categoryKey}-${item.toLowerCase().replace(/\s+/g, '-')}`);
            if (checkbox) {
                checkbox.checked = false;
        
                
                const categoryItem = checkbox.closest('.category-item');
                if (categoryItem) {
                    categoryItem.classList.remove('selected');
                }
            }
        });

        // Append the remove button to the itemDiv
        itemDiv.appendChild(removeBtn);

        // Append itemDiv to selected items container
        selectedItemsDiv.appendChild(itemDiv);
        console.log('Added selected item:', item); // For debugging
        // Clear the input field after adding the i
    }

    // Function to remove item from selected list
    function removeSelectedItem(item) {
        const itemDiv = document.getElementById(`selected-${item.toLowerCase().replace(/\s+/g, '-')}`);
        if (itemDiv) {
            console.log("removed item: ", itemDiv);
            itemDiv.remove();
            checkIfEmpty();
        }
    }

    // Hide container if no items remain
    function checkIfEmpty() {
        if (selectedItemsDiv.children.length === 0) {
            selectedItemsContainer.style.display = 'none';
        }
    }

//     //items sent back as an Array ["Ing1 (1)", "Ing2 (1)", "...", "IngN(1)", "Number of Recipes: (1)""]
//     document.getElementById("generateRecipeBtn").addEventListener("click", () => {
//         const items = document.querySelectorAll('.selected-item');
        
//         const final = [];

//         items.forEach(item => {
//             const name = item.querySelector('.ingredient-name').textContent;
//             const qty = item.querySelector('input[type="text"]').value || '1';
//             final.push(`${name} (${qty})`);
//         });
        

//         document.getElementById("final_ingredients").value = final.join(", ");
//         console.log("Final Ingredients:", final); // For debugging
//     });
// });

document.getElementById("generateRecipeBtn").addEventListener("click", () => {
    const items = document.querySelectorAll('.selected-item');
    const numRecipes = numRecipesDisplay.value;
    const final = [];

    items.forEach(item => {
        const name = item.querySelector('.ingredient-name').textContent;
        const qty = item.querySelector('input[type="text"]').value || '1';
        final.push(`${name} (${qty})`);
    });
    
    // document.body.innerHTML = "<h1>Loading recipe...</h1>";

    document.getElementById("final_ingredients").value = final.join(", ");
    console.log("Final Ingredients:", final); // For debugging

    document.body.innerHTML = "<h1>Loading recipe...</h1>";

    fetch('/post-recipe/', {
        method: 'POST',
        body: JSON.stringify({'ingredients':final, 'numberOfRecipes': numRecipes
        }),
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken') 
        }
    })
    //loading function
    .then(response => {
        
        return response.json();
    })
    //success function
    .then(data => {
        console.log(data);
        sessionStorage.setItem('ai_response', JSON.stringify(data));

        window.location.href='/chefai/recipe/';
        });
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            // Does this cookie string begin with the name we want?
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
