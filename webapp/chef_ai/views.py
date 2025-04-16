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
from textwrap import wrap
import json


logger = logging.getLogger(__name__)  # optional logging


# Create your views here.

load_dotenv()


def landing(request):
    return render(request, 'landing.html')

def index(request):
    # if request.method == "POST":
        
    #     ingredients_input = request.POST.get("final_ingredients", "")
    #     selected_options = [i.strip() for i in ingredients_input.split(",") if i.strip()]
    #     num_recipes = int(request.POST.get("recipe_amount", "1"))
        
    #     print(f"Number of recipes returned: {num_recipes}")
    #     ai_response = asyncio.run(run_multiple_llm_calls(selected_options, num_recipes))
    #     print(ai_response)
            
    #     #Save successful recipes to database
    #     if request.user.is_authenticated and ai_response:
    #         save_recipe_to_history(request.user, selected_options, ai_response[0])
            
    #     request.session['selected_options'] = selected_options
    #     request.session['ai_response'] = ai_response
            
    #     return redirect('list_of_recipes')
    selected_options = request.session.get('selected_options', [])
    num_recipes = request.session.get('num_recipes', 1)
    return render(request, 'index.html', {'selected_options':selected_options, 'num_recipes':num_recipes})






# Using this for the results page
def list_of_recipes(request):
        selected_options = request.session.get('selected_options', [])
        ai_responses = request.session.get('ai_response', [])
        request.session['selected_options'] = selected_options
        print(f"list_of_recipes view was hit {selected_options}")
        return render(request, 'listResults.html', {'selected_options': selected_options, 'ai_responses': ai_responses})


async def run_multiple_llm_calls(selected_options, num_recipes):
    tasks = [feedLLM(selected_options) for _ in range(num_recipes)]
    results = await asyncio.gather(*tasks)
    return JsonResponse(results, safe=False)



def feedLLM(selected_options, prevRecipes):
    
    try:
        llm = ChatGroq(
            temperature=0,
            api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.3-70b-versatile"
        )

        prompt = f"""I want a recipe that I can make for the list of ingredients and quantity. It is fine even if it simple. The recipe should be accurate with the list of ingredients and their quantity. For now you can assume that the user has the required quantity. The recipe should have a title, cuisine, 
    and amount of time required to cook the recipe, the list of ingredients with their quantity, utensils required and then a step by step process of cooking the recipe. Be careful to not suggest a recipe with ingredients that the user has not mentioned, 
    and one that does not exist. Do not assume that the user has more ingredients. YOU DO NOT NEED TO USE ALL THE INGREDIENTS LISTED. It must be a different recipe than the following:
    {prevRecipes}

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
    index = int(request.GET.get('index', 0))
    ai_responses = request.session.get('ai_response', [])

    if not ai_responses or index >= len(ai_responses):
        return redirect('response_recipe')

    ai_response = ai_responses[index]

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setFont("Helvetica-Bold", 16)

    y = 750
    left_margin = 50
    line_height = 15
    wrap_width = 90  # Approx chars per line

    # Title
    title = ai_response.get("title", "Recipe")
    pdf.drawString(left_margin, y, title)
    y -= 30

    pdf.setFont("Helvetica", 12)

    # Time
    time_required = ai_response.get("time", "")
    pdf.drawString(left_margin, y, f"Time Required: {time_required}")
    y -= 25

    # Ingredients
    pdf.drawString(left_margin, y, "Ingredients:")
    y -= 20
    for item in ai_response.get("ingredients", []):
        for line in wrap(f"- {item}", wrap_width):
            pdf.drawString(left_margin + 20, y, line)
            y -= line_height
            if y < 50:
                pdf.showPage()
                pdf.setFont("Helvetica", 12)
                y = 750

    y -= 10

    # Utensils
    pdf.drawString(left_margin, y, "Utensils:")
    y -= 20
    for item in ai_response.get("utensils", []):
        for line in wrap(f"- {item}", wrap_width):
            pdf.drawString(left_margin + 20, y, line)
            y -= line_height
            if y < 50:
                pdf.showPage()
                pdf.setFont("Helvetica", 12)
                y = 750

    y -= 10

    # Instructions
    pdf.drawString(left_margin, y, "Instructions:")
    y -= 20
    for idx, step in enumerate(ai_response.get("steps", []), 1):
        step_lines = wrap(f"{idx}. {step}", wrap_width)
        for line in step_lines:
            pdf.drawString(left_margin + 20, y, line)
            y -= line_height
            if y < 50:
                pdf.showPage()
                pdf.setFont("Helvetica", 12)
                y = 750

    pdf.save()
    buffer.seek(0)

    safe_title = re.sub(r'[^a-zA-Z0-9_]+', '_', title)
    return FileResponse(buffer, as_attachment=True, filename=f"{safe_title}.pdf")



# Function to generate and download JPG
def download_jpg(request):
    index = int(request.GET.get('index', 0))
    ai_responses = request.session.get('ai_response', [])

    if not ai_responses or index >= len(ai_responses):
        return redirect('response_recipe')

    ai_response = ai_responses[index]

    # Create blank image
    img_width, img_height = 800, 800
    img = Image.new("RGB", (img_width, img_height), "white")
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()

    y = 50
    line_spacing = 20
    wrap_width = 80  # characters per line

    def draw_wrapped(text, indent=0):
        nonlocal y
        lines = wrap(text, width=wrap_width)
        for line in lines:
            draw.text((50 + indent, y), line, fill="black", font=font)
            y += line_spacing
            if y > img_height - 50:
                break  # stop if image height exceeded

    # Title
    title = ai_response.get("title", "Recipe")
    draw.text((50, y), title, fill="black", font=font)
    y += line_spacing * 2

    # Time
    draw_wrapped(f"Time Required: {ai_response.get('time', '')}")

    y += line_spacing
    draw_wrapped("Ingredients:")
    for item in ai_response.get("ingredients", []):
        draw_wrapped(f"- {item}", indent=20)

    y += line_spacing
    draw_wrapped("Utensils:")
    for item in ai_response.get("utensils", []):
        draw_wrapped(f"- {item}", indent=20)

    y += line_spacing
    draw_wrapped("Instructions:")
    for idx, step in enumerate(ai_response.get("steps", []), 1):
        draw_wrapped(f"{idx}. {step}", indent=20)

    # Save image to buffer
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=95, dpi=(150,150))
    buffer.seek(0)

    safe_title = re.sub(r'[^a-zA-Z0-9_]+', '_', title)
    return FileResponse(buffer, as_attachment=True, filename=f"{safe_title}.jpg")

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
# @csrf_exempt
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
            
            # saves ingredients and number to generate to session
            request.session['selected_options'] = ingredients
            request.session['num_recipes'] = numRecipes

            ai_response_list = []
            
            # feeds the ingredients and previous recipes into the llm for unique recipes
            for i in range(numRecipes):
                ai_response = feedLLM(ingredients, ai_response_list)
                ai_response_list.append(ai_response)
                    #     #Save successful recipes to database
                if request.user.is_authenticated and ai_response:
                    save_recipe_to_history(request.user, ingredients, ai_response)
            
            request.session['ai_response']= ai_response_list
            
            return JsonResponse({'status': 'success', 'recieved': ai_response_list})
        
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
