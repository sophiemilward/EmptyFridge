import requests  # For making HTTP requests
from pprint import pprint  # For pretty-printing output
import csv  # For handling CSV file operations

# Function to get recipes based on an ingredient
def get_recipes(ingredient):
    app_id = "f7081987"
    app_key = "4a7f92ae646375a91777e96cfa7ce188"
    url = 'https://api.edamam.com/search?q={}&app_id={}&app_key={}'.format(ingredient, app_id, app_key)
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# Function to filter recipes based on health labels and excluded ingredients
def filter_recipes(recipes, health_label=None, excluded=None):  # New function
    excluded_ingredients = [item.strip().lower() for item in excluded.split(',')] if excluded else []
    filtered_hits = []

    for hit in recipes.get('hits', []):
        ingredients = [ingredient['text'].lower() for ingredient in hit['recipe']['ingredients']]
        health_labels = [label.lower() for label in hit['recipe'].get('healthLabels', [])]

        if (not health_label or health_label.lower() in health_labels) and not any(
                excluded in ingredient for excluded in excluded_ingredients for ingredient in ingredients):
            filtered_hits.append(hit)

    recipes['hits'] = filtered_hits
    return recipes

# Function to display recipes and prepare a list for CSV export
def display_recipes(recipes, ingredient):
    recipe_list = []
    if recipes and 'hits' in recipes:
        for hit in recipes['hits']:
            recipe = hit['recipe']
            recipe_details = {
                "Search_Ingredient": ingredient,
                "Recipe": recipe['label'],
                "Ingredients": [ingredient['text'] for ingredient in recipe['ingredients']],
                "Link": recipe['shareAs']
            }
            recipe_list.append(recipe_details)
            pprint("Recipe: {}".format(recipe['label']))
            pprint("Ingredients: {}".format([ingredient['text'] for ingredient in recipe['ingredients']]))
            pprint("Share As: {}".format(recipe['shareAs']))
    else:
        print("No recipes found. Please try a different ingredient.")
    return recipe_list

# Function to handle user input for ingredient search and dietary restrictions
def ingredient_input():
    ingredient = input("What ingredient do you want to search for? ")
    health_label = input("Please enter diet requirements (e.g. vegetarian, vegan, dairy-free, press enter if none): ")
    excluded = input("Please enter any ingredients to exclude(press enter if none): ")

    if ingredient:
        recipes = get_recipes(ingredient)  # Only pass ingredient
        recipes = filter_recipes(recipes, health_label=health_label, excluded=excluded)  # Filter results after fetching
        recipe_list = display_recipes(recipes, ingredient)
        movie_recommendation = get_movie_recommendation(ingredient)
        print("Recommended movie:", movie_recommendation)

        # Save recipes to CSV
        field_names = ['Search_Ingredient', 'Recipe', 'Ingredients', 'Link']
        for recipe in recipe_list:
            recipe['Ingredients'] = ', '.join(recipe['Ingredients'])

        with open('recipes.csv', 'w+', encoding='utf-8') as csv_file:
            spreadsheet = csv.DictWriter(csv_file, fieldnames=field_names)
            spreadsheet.writeheader()
            spreadsheet.writerows(recipe_list)
    else:
        print("Please enter a valid ingredient.")

# Function to get a movie recommendation based on an ingredient
def get_movie_recommendation(ingredient):
    movie_url = 'https://api.themoviedb.org/3/search/movie?api_key=d02948b9f6b2338ba4aedaea85fe9613&query={}'.format(ingredient)
    response = requests.get(movie_url)
    response.raise_for_status()
    movies = response.json().get('results', [])

    if movies:
        movie_title = movies[0]['title']
        movie_id = movies[0]['id']
        movie_link = 'https://www.themoviedb.org/movie/{}'.format(movie_id)
        return movie_title, movie_link
    else:
        return "No movie recommendations found."

# Start the ingredient input process
ingredient_input()


# Function to get ingredients from chosen recipe
def get_chosen_recipe():
    import requests  # For making HTTP requests
    from pprint import pprint  # For pretty-printing output

    chosen_recipe = input("What recipe do you want to cook? ")
    app_id = "f7081987"
    app_key = "4a7f92ae646375a91777e96cfa7ce188"
    url = 'https://api.edamam.com/search?q={}&app_id={}&app_key={}'.format(chosen_recipe, app_id, app_key)
    response = requests.get(url)
    response.raise_for_status()  # Raises error code if unsuccessful http request
    choice = response.json()
    hits = choice['hits']
    if hits:
        recipe_choice = hits[0] # It seems to find multiple recipes with the same name, so I've told it to choose the first one.
        shopping_list = recipe_choice['recipe']['ingredientLines']

        with open('shopping_list.txt', 'w') as f: # Save as .txt
            for line in shopping_list:
                f.write(f"{line}\n") # Writes each ingredient to a new line

        return print(recipe_choice['recipe']['ingredientLines']) # prints ingredient list
    else:
        return print("No recipe found, try another recipe")

# Call function to choose specific recipe and save to shopping list
get_chosen_recipe()