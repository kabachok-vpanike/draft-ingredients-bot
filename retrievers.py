import json
import requests


def escape_markdown(text):
    escape_chars = '\*_`[](){}#+.!|'
    return ''.join(['\\' + char if char in escape_chars else char for char in text])


def delete_markdown(text):
    escape_chars = '-\*_`[](){}#+.!|'
    return ''.join(['' if char in escape_chars else char for char in text])


def get_recipe_info_formatted(recipe):
    formatted = f"*{escape_markdown(recipe['label'])}*\n\n"
    formatted += f"_Calories:_ {int(recipe['calories'] // 10)}\n"
    if int(recipe['totalTime']):
        formatted += f"_Preparation time:_ {int(recipe['totalTime'])}\n"
    formatted += f"_Cuisine:_ {recipe['cuisineType'][0]}\n"
    formatted += f"_Meal type:_ {recipe['mealType'][0]}\n\n"
    formatted += "_Ingredients:_\n\n"
    for i in recipe["ingredientLines"]:
        formatted += f"   • {escape_markdown(delete_markdown(i))}\n"
    formatted += f"\n[Recipe link]({recipe['url']})"
    return formatted


def get_recipes_by_ingredients(ingredients, RECIPE_APP_ID, RECIPE_APP_KEY):
    recipes = []
    response = requests.get(url='https://api.edamam.com/api/recipes/v2', params={
                            "type": "public", "app_id": RECIPE_APP_ID, "app_key": RECIPE_APP_KEY, "q": ','.join(ingredients)})
    for item in json.loads(response.content)["hits"]:
        recipes.append(item)
    return recipes


def get_ingredients_suggestions(user_input, FOOD_APP_ID, FOOD_APP_KEY):
    response = requests.get(url='https://api.edamam.com/api/food-database/v2/parser', params={
                                "app_id": FOOD_APP_ID, "app_key": FOOD_APP_KEY, "ingr": user_input})
    recipesObj = json.loads(response.content)
    options = []
    for i in recipesObj["hints"]:
        options.append(i["food"]["label"])
    return options
