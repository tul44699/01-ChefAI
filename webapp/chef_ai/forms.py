from django import forms

class ingredientList(forms.Form):
    PANTRY=[
    ('butter', 'Butter'),
    ('egg', 'Egg'),
    ('garlic', 'Garlic'),
    ('onion', 'Onion'),
    ('milk', 'Milk'),
    ('sugar', 'Sugar'),
    ]
    VEGETABLES =[
    ('bell pepper', 'Bell Pepper'),
    ('scallion', 'Scallion'),
    ('carrot','Carrot'),
    ('tomato', 'Tomato'),
    ('potato', 'Potato'),
    ]
    APPLIANCES =[
    ('gas stove', 'Gas Stove'),
    ('grill', 'Grill'),
    ('air fryer', 'Air Fryer'),
    ('oven', 'Oven'),
    ]
    
    pantry = forms.MultipleChoiceField(
        choices=PANTRY,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    veggies = forms.MultipleChoiceField(
        choices = VEGETABLES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    appliances = forms.MultipleChoiceField(
        choices = APPLIANCES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )