# ChefAI - AI-Powered Recipe Generator
ChefAI is a web application that helps users generate recipes based on the ingredients they have at home. 
Whether you're an inexperienced cook or looking for creative meal ideas, ChefAI provides AI-generated recipes tailored to your available ingredients.
Adding an screenshot or a mockup of your application in action would be nice.  

![This is a screenshot.](https://github.com/cis3296s25/01-ChefAI/blob/main/chef_ai%20launch%20page.png)

Features:
- Implemented ingredient selection from a predefined list to retrieve recipes.
- Allow users to click “Generate Recipe” after selecting ingredients, redirecting them to the
response.html page.
- Display AI-generated recipe on the response.html page, including step-by-step
instructions and a list of necessary ingredients.
- Modularize the ingredient selection form.
- Set up basic environment configuration
- Deploy the website to EC2 for testing and accessibility.
- Implemented a back-to-the-home screen button as the logo.
- Implemented a feature that allows users to search and select from a drop-down menu in the search bar.
- Implemented a feature to let the users download a jpeg or pdf file of the generated recipe.
- Improved search selection accuracy
- Integrated keyboard navigation support for dropdown
- Added image deection model
- Implemented a feature to upload an image for ingredient detection
- Added auto-detection and selection of ingredients from uplaoded image
- Set up registration and profile pages for users
- Create login/logout functionlity
- Implemented feature to save successfully generated recipes by user
- Allow users to view any previous recipe they have searched in their profiles page
- Improved UI readability and design


# How to run
Here is a deployed version of our current app:
[Chef-AI](http://3.21.159.180/)

To run the ChefAI locally:
1. Ensure Python3 is installed on development computer
2. Obtain API Key from GroqCloud: [https://console.groq.com/keys](https://console.groq.com/keys)
4. Obtain your Image Detection Model API Key: [https://clarifai.com/clarifai/main/models/food-item-recognition](https://clarifai.com/clarifai/main/models/food-item-recognition)
5. Fork repository
6. Git clone repository
7. Create .env file in the project root. Then inside the file:
```
a. Create variable: GROQ_API_KEY = "YOUR_API_KEY"
b. Create variable: PAT = "YOUR_IMAGE_MODEL_KEY"
```
8. Create a virtual enironment using command:
```
a. python -m venv myenv  
```
9. Activate the virtual enironment with command
- For mac0S/Linux:
```
a. source myenv/bin/activate
```
- For Windows:
```
a. myenv\Scripts\Activate
```
10. Navigate to the folder that has the file requirements.txt and type the command:
```
a. pip install -r requirements.txt
```
11. Now cd into the directory that has the manage.py file & start local server by typing the following command:
```
a. python manage.py runserver
```
12. Visit http://127.0.0.1:8000

# How to contribute
Follow this project board to know the latest status of the project: [https://github.com/orgs/cis3296s25/projects/58]([https://github.com/orgs/cis3296s25/projects/58])  

### How to build
- Use this github repository: [https://github.com/cis3296s25/01-ChefAI](https://github.com/cis3296s25/01-ChefAI)
- Obtain your LLM API for free at GroqCloud: [https://console.groq.com/keys](https://console.groq.com/keys)
- Obtain your Image Detection Model API Key: [https://clarifai.com/clarifai/main/models/food-item-recognition](https://clarifai.com/clarifai/main/models/food-item-recognition)
- Use the `main` branch for the latest stable release:
```
git checkout main
```
- Create .env file in the project root.
```
Inside the file,
a. create variable: GROQ_API_KEY = "YOUR_API_KEY"
b. create variable: PAT = "YOUR_IMAGE_MODEL_KEY"
```
- All required dependencies are listed in `requirements.txt`. Install them with:
```
a. pip install -r requirements.txt
```
- To start the application, run:
```
a. python manage.py runserver
```
- The Django development server should start, and you should be prompted to go to:
```
http://127.0.0.1:8000/    
```

# How to Run Tests
- Enter folder that contains manage.py and pytest.ini
- Run Command: pytest
- Once tests complete, there is a Test_report.html page that is created.
- There is also a Coverage Report that is available for viewing.
