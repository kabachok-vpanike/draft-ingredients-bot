from markups import generate_main_menu_markup, generate_markup_back_to_recipes, generate_markup_remove_ingredient, generate_markup_with_unique_option, generate_options_markup
from retrievers import get_recipe_info_formatted, get_recipes_by_ingredients


def show_menu(chat_id, user_id, bot, user_data):

    collected_ingredients_formatted = ""
    if user_id in user_data:
        for i in user_data[user_id]["collected_ingredients"]:
            collected_ingredients_formatted += f"  • {i}\n"

    responseString = "What would you like to do?"
    if len(collected_ingredients_formatted) > 0:
        responseString = f"Your current ingredients:\n\n{collected_ingredients_formatted}\n{responseString}"
    bot.send_message(chat_id, responseString,
                     reply_markup=generate_main_menu_markup())


def ingredient_suggestion_handler(call, user_data, bot):
    selected_option = user_data[call.from_user.id]["options"][int(
        call.data.split("_")[1])]
    updated_markup = generate_markup_with_unique_option(
        f"✅ {selected_option}")
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=f"You selected: {selected_option}",
                          reply_markup=updated_markup)
    if "collected_ingredients" not in user_data[call.from_user.id]:
        user_data[call.from_user.id]["collected_ingredients"] = [
            selected_option]
    else:
        user_data[call.from_user.id]["collected_ingredients"].append(
            selected_option)
    show_menu(call.message.chat.id, call.from_user.id, bot, user_data)


def recipe_option_handler(call, user_data, bot):
    ind = int(call.data.split("_")[1])
    selected_option = user_data[call.from_user.id]["recipes"][ind]
    recipe = user_data[call.from_user.id]["recipesData"][ind]["recipe"]
    formatted = get_recipe_info_formatted(recipe)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=formatted, parse_mode="Markdown", reply_markup=generate_markup_back_to_recipes())


def ingredient_remove_handler(call, user_data, bot):
    selected_option = user_data[call.from_user.id]["collected_ingredients"][int(
        call.data.split("_")[1])]
    user_data[call.from_user.id]["collected_ingredients"].remove(
        selected_option)
    updated_markup = generate_markup_with_unique_option(
        f"❌ {selected_option}")
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=f"Ingredient removed: {selected_option}",
                          reply_markup=updated_markup)
    show_menu(call.message.chat.id, call.from_user.id, bot, user_data)


def show_recipe_handler(call, user_data, bot, RECIPE_APP_ID, RECIPE_APP_KEY):
    if call.from_user.id not in user_data or len(user_data[call.from_user.id]["collected_ingredients"]) == 0:
        bot.answer_callback_query(
            call.id, "Nothing to show, please add some ingredients first")
        return

    collected_ingredients = user_data[call.from_user.id]["collected_ingredients"]
    allRecipesData = get_recipes_by_ingredients(
        collected_ingredients, RECIPE_APP_ID, RECIPE_APP_KEY)
    recipes = [item["recipe"]["label"] for item in allRecipesData]

    collected_ingredients_formatted = ""
    for ingredient_name in collected_ingredients:
        collected_ingredients_formatted += f"  • {ingredient_name}\n"

    if len(recipes) == 0:
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=f"No recipes were found for your current ingredients:\n\n{collected_ingredients_formatted}\nTry remove some of them", reply_markup=generate_markup_remove_ingredient())
    else:
        bot.edit_message_text(chat_id=call.message.chat.id,  message_id=call.message.message_id,
                              text=f"Your ingredients:\n\n{collected_ingredients_formatted}\nChoose recipe:",
                              reply_markup=generate_options_markup(1, recipes, 'recipe_', 'recipepage_'))
        user_data[call.from_user.id]["recipes"] = recipes
        user_data[call.from_user.id]["recipesData"] = allRecipesData
