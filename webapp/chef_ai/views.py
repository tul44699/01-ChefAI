from .models import userHistory, Ingredient
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.http import HttpResponse, JsonResponse, FileResponse
from django import forms
from .forms import ingredientList
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image, ImageDraw, ImageFont
from django.views.decorators.csrf import csrf_exempt
import groq
import asyncio
from asgiref.sync import async_to_sync
# from mysite.settings import LOADENV
from langchain_groq import ChatGroq
from groq import AsyncGroq
import os
from dotenv import load_dotenv
import re
import io
from django.shortcuts import render
from clarifai.client.model import Model
import logging
import traceback
from django_ajax.decorators import ajax
import json


logger = logging.getLogger(__name__)  # optional logging

# Create your views here.

load_dotenv()


def index(request):
    if request.method == "POST":
        
        ingredients_input = request.POST.get("final_ingredients", "")
        selected_options = [i.strip() for i in ingredients_input.split(",") if i.strip()]
        num_recipes = int(request.POST.get("recipe_amount", "1"))
        
        print(f"Number of recipes returned: {num_recipes}")
        ai_response = asyncio.run(run_multiple_llm_calls(selected_options, num_recipes))
        print(ai_response)
            
        #Save successful recipes to database
        if request.user.is_authenticated and ai_response:
            save_recipe_to_history(request.user, selected_options, ai_response[0])
            
        request.session['selected_options'] = selected_options
        request.session['ai_response'] = ai_response

        # if num_recipes ==1:
        #     return redirect('response_recipe')
        # else:
            
        return redirect('list_of_recipes')

    return render(request, 'index.html')


# #displays a new page with the recipe listed
# def response_recipe(request):
#     selected_options = request.session.get('selected_options', [])
#     ai_response = request.session.get('ai_response', [])
#     print("view was hit")
#     return render(request, 'recipeResults.html', {'selected_options': selected_options, 'ai_response': ai_response})


# Using this for the results page
def list_of_recipes(request):
        selected_options = request.session.get('selected_options', [])
        ai_responses = request.session.get('ai_response', [])
        print(f"list_of_recipes view was hit {ai_responses}")
        return render(request, 'listResults.html', {'selected_options': selected_options, 'ai_responses': ai_responses})


async def run_multiple_llm_calls(selected_options, num_recipes):
    tasks = [feedLLM(selected_options) for _ in range(num_recipes)]
    results = await asyncio.gather(*tasks)
    return JsonResponse(results, safe=False)



def feedLLM(selected_options):
    
    try:
        llm = ChatGroq(
            temperature=0,
            api_key=os.getenv("GROQ_API_KEY"),
            model_name="deepseek-r1-distill-llama-70b"
        )

        prompt = f"""I want a recipe that I can make for the list of ingredients and quantity. It is fine even if it simple. The recipe should be accurate with the list of ingredients and their quantity. For now you can assume that the user has the required quantity. The recipe should have a title, cuisine, 
    and amount of time required to cook the recipe, the list of ingredients with their quantity, utensils required and then a step by step process of cooking the recipe. Be careful to not suggest a recipe with ingredients that the user has not mentioned, 
    and one that does not exist. Do not assume that the user has more ingredients. YOU DO NOT NEED TO USE ALL THE INGREDIENTS LISTED.

    Please format your recipe response like this:

    Title: <recipe title>  
    Cuisine: <cuisine type>  
    Time Required: <cook time>  
    Ingredients:
    - ...
    Utensils:
    - ...
    Steps:
    1. ...
    2. ...
    Here is the list of ingredients with the quantity: {selected_options}"""

        response = llm.invoke(prompt)
        raw = response.content if hasattr(response, 'content') else response.resolve()
        
        print(f"the raw output from llm: {raw}")

        # Regex-based parsing
        sections = {
            "title": re.search(r"(?:Title:|Recipe:)\s*(.+)", raw, re.IGNORECASE),
            "cuisine": re.search(r"Cuisine:\s*(.+)", raw, re.IGNORECASE),
            "time": re.search(r"Time(?: Required)?:\s*(.+)", raw, re.IGNORECASE),
            "ingredients": re.search(r"Ingredients:\s*((?:.|\n)+?)\n(?:Utensils:|Steps:)", raw, re.IGNORECASE),
            "utensils": re.search(r"Utensils:\s*((?:.|\n)+?)\n(?:Steps:)", raw, re.IGNORECASE),
            "steps": re.search(r"Steps:\s*((?:.|\n)+)", raw, re.IGNORECASE),
        }

        def clean_section_list(section):
            return [
                re.sub(r"^\s*[\d]+[.)]\s*", "", item.strip(" \n\r-•").strip())
                for item in section
                if item.strip() and not item.lower().startswith("ingredients:")
            ]

        parsed = {
            key: (
                clean_section_list(match.group(1).strip().split("\n"))
                if key in ["ingredients", "utensils", "steps"]
                else match.group(1).strip()
            )
            for key, match in sections.items() if match
        }
        print(f"Inside feedLLM Parsed data: {parsed}")  

        return parsed

    except Exception as e:
        logger.error("Error in feedLLM: %s", traceback.format_exc())
        
        return {"error": "Failed to generate recipe. Please try again later."}


# Function to generate and download PDF
def download_pdf(request):
    ai_response = request.session.get('ai_response', "")
    print(ai_response)

    if not ai_response:
        return redirect('response_recipe')

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setFont("Times-Roman", 12)  # Set font to Times New Roman

    y_position = 750  # Start position for text

    for key, value in ai_response.items():
        print(y_position)
        if y_position < 50:  # Create a new page if necessary
            print("Making new page")
            pdf.showPage()
            pdf.setFont("Times-Roman", 12)
            y_position = 750

        pdf.drawString(50, y_position, f"{key.capitalize()}:")
        y_position -= 20  # Move down after the key

        if isinstance(value, list):
            for item in value:
                if y_position < 50:  # Create a new page if necessary
                    print("Making new page")
                    pdf.showPage()
                    pdf.setFont("Times-Roman", 12)
                    y_position = 750
                pdf.drawString(70, y_position, f"- {item}")  # Indent list items
                y_position -= 15  # Move down for each item
        else:
            if y_position < 50:
                pdf.showPage()
                pdf.setFont("Times-Roman", 12)
                y_position = 750
            pdf.drawString(70, y_position, value)
            y_position -= 20  # Move down for the next section

    pdf.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="recipe.pdf")


# Function to generate and download JPG
def download_jpg(request):
    ai_response = request.session.get('ai_response', "")

    if not ai_response:
        return redirect('response_recipe')  # Redirect if no data

    img = Image.new("RGB", (800, 800), "white")
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 20)  # Use Arial if available
    except:
        font = ImageFont.load_default()

    y_position = 50
    line_spacing = 25  # Adjust line spacing for better readability

    for key, value in ai_response.items():
        if y_position > 550:  # Ensure text fits within image bounds
            break  
        draw.text((50, y_position), f"{key.capitalize()}:", fill="black", font=font)
        y_position += 30  # Move down after the key

        if isinstance(value, list):
            for item in value:
                draw.text((70, y_position), f"- {item}", fill="black", font=font)  # Indent list items
                y_position += line_spacing  # Move down for each list item
        else:
            draw.text((70, y_position), value, fill="black", font=font)
            y_position += line_spacing  # Move down for the next section

    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    buffer.seek(0)
    
    return FileResponse(buffer, as_attachment=True, filename="recipe.jpg")


def search_ingredients(request):
    # Gets the search query
    query = request.GET.get('q', '').strip().lower()
    # Query the database for ingredients whose name starts with the input
    if query:
        results = Ingredient.objects.filter(ingredient_name__istartswith=query).values_list('ingredient_name', flat=True)
        return JsonResponse({'results': list(results)}) # Sends back the matching ingredient names as JSON
    return JsonResponse({'results': []})


# User Registration
def userRegistration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
                user = form.save()
                #logs user in automatically
                login(request, user)
                
                return redirect('index')
    else:
        form = UserCreationForm()
    
    return render(request, "registration/register.html", {"form":form})

def logoutUser(request):
    logout(request)
    return redirect('index')

def getProfile(request):
    
    return render(request, 'registration/profile.html')

def save_recipe_to_history(user, selected_options, ai_response):

    recipe_text = "\n".join([
        f"Title: {ai_response.get('title', 'N/A')}",
        f"Cuisine: {ai_response.get('cuisine', 'N/A')}",
        f"Time Required: {ai_response.get('time', 'N/A')}",
        "\nIngredients:\n" + "\n".join(ai_response.get('ingredients', [])),
        "\nUtensils:\n" + "\n".join(ai_response.get('utensils', [])),
        "\nSteps:\n" + "\n".join(ai_response.get('steps', [])),
    ])

    userHistory.objects.create(
        userID=user,
        selectedIngredients=", ".join(selected_options),
        generatedRecipe=recipe_text,
        title=ai_response.get('title', 'Untitled Recipe')
    )

#Code that runs the Image detection model
@csrf_exempt
def scan_images(request):
    if request.method == 'POST':
        images = request.FILES.getlist('images')
        detected_items = set()

        model = Model(url="https://clarifai.com/clarifai/main/models/food-item-recognition", pat=os.getenv('PAT'))
        for image in images:
            print("success")
            img_bytes = image.read()
            prediction = model.predict_by_bytes(img_bytes, input_type="image", output_config={"min_value": 0.01})
            print(prediction)
            for c in prediction.outputs[0].data.concepts:
                if c.value > 0.75:
                    detected_items.add(c.name.lower())
                    print(c.name)

        # Match items to your DB
        #Ingredients Model 
        db_items = Ingredient.objects.values_list('ingredient_name', flat=True)
        db_items_lowered = [item.lower() for item in db_items]
        matched = [item for item in detected_items if item in db_items_lowered]
        matched_upper = [item.capitalize() for item in matched]
        return JsonResponse({'ingredients': matched_upper})


#History Page content

def view_saved_recipe(request, recipe_id):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        recipe = userHistory.objects.get(id=recipe_id, userID=request.user)
    except userHistory.DoesNotExist:
        return HttpResponse("Recipe not found.", status=404)

    # Parse the generatedRecipe string back into structured data
    raw_content = recipe.generatedRecipe
    
    # Extract sections using regex patterns similar to your feedLLM function
    title_match = re.search(r"Title:\s*(.+)", raw_content)
    cuisine_match = re.search(r"Cuisine:\s*(.+)", raw_content)
    time_match = re.search(r"Time Required:\s*(.+)", raw_content)
    
    # Extract list sections
    ingredients_section = re.search(r"Ingredients:\s*((?:.|\n)+?)(?:\n\nUtensils:|\n\nSteps:)", raw_content)
    utensils_section = re.search(r"Utensils:\s*((?:.|\n)+?)(?:\n\nSteps:)", raw_content)
    steps_section = re.search(r"Steps:\s*((?:.|\n)+)", raw_content)
    
    # Format into ai_response dictionary
    ai_response = {
        "title": title_match.group(1) if title_match else recipe.title,
        "cuisine": cuisine_match.group(1) if cuisine_match else "Not specified",
        "time": time_match.group(1) if time_match else "Not specified",
        "ingredients": [line.strip("- ") for line in ingredients_section.group(1).strip().split("\n")] if ingredients_section else [],
        "utensils": [line.strip("- ") for line in utensils_section.group(1).strip().split("\n")] if utensils_section else [],
        "steps": [line.strip("0123456789. ") for line in steps_section.group(1).strip().split("\n")] if steps_section else []
    }
    
    return render(request, 'recipeResults.html', {
        'selected_options': recipe.selectedIngredients.split(', '),
        'ai_response': ai_response  # Pass with the same name your template expects
    })



def getProfile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    history = userHistory.objects.filter(userID=request.user).order_by('-id')
    return render(request, 'registration/profile.html', {'history': history})


def post_recipe(request):
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        try:
            data = json.loads(request.body)
            ingredients = data.get('ingredients', [])
            numRecipes = int(data.get('numberOfRecipes', 1))
            print("Recieved number of recipes to be processed: ", numRecipes)
            print("Recieved ingredients in backend ", ingredients)
            ai_response_list = []
            
            for i in range(numRecipes):
                ai_response = feedLLM(ingredients)
                ai_response_list.append(ai_response)
            
            request.session['ai_response']= ai_response_list
            
            return JsonResponse({'status': 'success', 'recieved': ai_response_list})
        
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
