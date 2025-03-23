from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms
from .forms import ingredientList
from django.conf import settings
import groq
# from mysite.settings import LOADENV
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
import re
# Create your views here.

load_dotenv()

def index(request):
    if request.method == "POST":
        form = ingredientList(request.POST)
        if form.is_valid():
            
            pantry = form.cleaned_data.get('pantry',[])
            veggies= form.cleaned_data.get('veggies',[])
            appliances= form.cleaned_data.get('appliances',[])
            spices= form.cleaned_data.get('spices' ,[])

            print(f"Here are the pantry items: {pantry}")
            print(f"Here are the veggies: {veggies}")
            print(f"Here are the appliances: {appliances}")
            print(f"Here are the spices {spices}")

            
            selected_options = pantry + veggies + appliances + spices
            print(selected_options)
            ai_response = feedLLM(selected_options)
            
            request.session['selected_options'] = selected_options
            request.session['ai_response'] = ai_response

            return redirect('response_recipe')
    else:
        form = ingredientList()
    return render(request, 'index.html', {'form': form})

#displays a new page with the recipe listed
def response_recipe(request):
    selected_options = request.session.get('selected_options', [])
    ai_response = request.session.get('ai_response', "")

    return render(request, 'recipetemp.html', {'selected_options': selected_options, 'ai_response': ai_response})


def feedLLM(selected_options):
    
    llm = ChatGroq(temperature=0, api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.3-70b-versatile")


       # Create the prompt
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

    # Invoke the model with the prompt
    response = llm.invoke(prompt)
    # Directly access the content attribute
    # If there's a proxy, you may need to resolve it or use another method to extract data
    raw = response.content if hasattr(response, 'content') else response.resolve()
    print(raw)

    # Using regex to extract specific parts of the response
    sections = {
        "title": re.search(r"(?:Title:|Recipe:)\s*(.+)", raw, re.IGNORECASE),
        "cuisine": re.search(r"Cuisine:\s*(.+)", raw, re.IGNORECASE),
        "time": re.search(r"Time(?: Required)?:\s*(.+)", raw, re.IGNORECASE),
        "ingredients": re.search(r"Ingredients:\s*((?:.|\n)+?)\n(?:Utensils:|Steps:)", raw, re.IGNORECASE),
        "utensils": re.search(r"Utensils:\s*((?:.|\n)+?)\n(?:Steps:)", raw, re.IGNORECASE),
        "steps": re.search(r"Steps:\s*((?:.|\n)+)", raw, re.IGNORECASE),
    }

    # Cleans up lists from repetivenes
    def clean_section_list(section):
        return [
            re.sub(r"^\s*[\d]+[.)]\s*", "", item.strip(" \n\r-•").strip())
            for item in section
            if item.strip() and not item.lower().startswith("ingredients:")
        ]

    # Dictionary from the regex matches in `sections`
    parsed = {
        key: (
            # Send list-based sections through clean_section_list() otherwise just return the string directly
            clean_section_list(match.group(1).strip().split("\n"))
            if key in ["ingredients", "utensils", "steps"]
            else match.group(1).strip()
        )
        for key, match in sections.items() if match # Loop to go through all the sections
    }

    # # Return the full content of the response
    # return response.content
    return parsed