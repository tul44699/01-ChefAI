from django import forms

class ingredientList(forms.Form):
    PANTRY=[
    ('butter', 'Butter'),
    ('egg', 'Egg'),
    ('milk', 'Milk'),
    ('sugar', 'Sugar'),
    ('flour', 'Flour'),
    ('salt', 'Salt'),
    ('olive_oil', 'Olive Oil'),
    ('vegetable_oil', 'Vegetable Oil'),
    ('baking_powder', 'Baking Powder'),
    ('baking_soda', 'Baking Soda'),
    ('honey', 'Honey'),
    ('vanilla_extract', 'Vanilla Extract'),
    ('cocoa_powder', 'Cocoa Powder'),
    ('soy_sauce', 'Soy Sauce'),
    ('rice', 'Rice'),
    ('pasta', 'Pasta'),
    ('cheese', 'Cheese'),
    ('chocolate', 'Chocolate'),
    ('beans', 'Beans'),
    ('bread', 'Bread'),
    ('canned_tuna', 'Canned Tuna'),
    ('canned_soup', 'Canned Soup'),
    ('canned_corn', 'Canned Corn'),
    ('canned_peas', 'Canned Peas'),
    ('spaghetti_sauce', 'Spaghetti Sauce'),
    ('mayonnaise', 'Mayonnaise'),
    ('mustard', 'Mustard'),
    ('ketchup', 'Ketchup'),
    ('hot_sauce', 'Hot Sauce'),
    ('peanut_butter', 'Peanut Butter'),
    ('jam', 'Jam'),
    ('cereal', 'Cereal'),
    ('tea', 'Tea'),
    ('coffee', 'Coffee'),
    ('chicken_bouillon', 'Chicken Bouillon'),
    ('chicken breast', 'Chicken Breast')
    ]

    SPICES = [
        ('cinnamon', 'Cinnamon'),
        ('nutmeg', 'Nutmeg'),
        ('oregano', 'Oregano'),
        ('thyme', 'Thyme'),
        ('cumin', 'Cumin'),
        ('paprika', 'Paprika'),
        ('bay_leaves', 'Bay Leaves'),
        ('chili_powder', 'Chili Powder'),
        ('red_pepper_flakes', 'Red Pepper Flakes'),
        ('turmeric', 'Turmeric'),
        ('ginger', 'Ginger'),
        ('garam_masala', 'Garam Masala'),
        ('cardamom_green', 'Cardamom (Green)'),
        ('cardamom_black', 'Cardamom (Black)'),
        ('fenugreek', 'Fenugreek (Methi)'),
        ('asafoetida', 'Asafoetida (Hing)'),
        ('mustard_seeds', 'Mustard Seeds'),
        ('coriander_powder', 'Coriander Powder'),
        ('fennel_seeds', 'Fennel Seeds'),
        ('cloves', 'Cloves'),
        ('amchur', 'Mango Powder (Amchur)'),
        ('curry_leaves', 'Curry Leaves')
    ]

    VEGETABLES = [
    ('garlic', 'Garlic'),
    ('onion', 'Onion'),
    ('tomato', 'Tomato'),
    ('potatoes', 'Potatoes'),
    ('carrot', 'Carrot'),
    ('broccoli', 'Broccoli'),
    ('spinach', 'Spinach'),
    ('lettuce', 'Lettuce'),
    ('cucumber', 'Cucumber'),
    ('zucchini', 'Zucchini'),
    ('bell_pepper', 'Bell Pepper'),
    ('eggplant', 'Eggplant'),
    ('cabbage', 'Cabbage'),
    ('kale', 'Kale'),
    ('cauliflower', 'Cauliflower'),
    ('peas', 'Peas'),
    ('green_beans', 'Green Beans'),
    ('sweet_potatoes', 'Sweet Potatoes'),
    ('asparagus', 'Asparagus'),
    ('radish', 'Radish'),
    ('corn', 'Corn'),
    ('mushroom', 'Mushroom'),
    ('leeks', 'Leeks'),
    ('pumpkin', 'Pumpkin'),
    ('brussels_sprouts', 'Brussels Sprouts'),
    ('artichoke', 'Artichoke'),
    ('chard', 'Chard'),
    ('squash', 'Squash'),
    ('parsnip', 'Parsnip')
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
    spices = forms.MultipleChoiceField(
        choices = SPICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )