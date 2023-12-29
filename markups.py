from telebot import types


def format_ingredient_list(ingredients):
    collected_ingredients_formatted = ""
    for ingredient in ingredients:
        collected_ingredients_formatted += f"  • {ingredient}\n"
    return collected_ingredients_formatted


def generate_options_markup(page, options, button_data_prefix, page_data_prefix):

    ITEMS_PER_PAGE = 5
    markup = types.InlineKeyboardMarkup()
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    for i in range(start, min(end, len(options))):
        button = types.InlineKeyboardButton(
            options[i], callback_data=f"{button_data_prefix}{i}")
        markup.add(button)

    if page > 1:
        markup.add(types.InlineKeyboardButton("⬅️ Previous",
                   callback_data=f"{page_data_prefix}{page-1}"))
    if end < len(options):
        markup.add(types.InlineKeyboardButton(
            "Next ➡️", callback_data=f"{page_data_prefix}{page+1}"))

    backButton = types.InlineKeyboardButton(
        ">> Back to menu <<", callback_data=f"back_menu")
    markup.add(backButton)

    return markup


def generate_markup_with_unique_option(option):
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(option, callback_data=f"no data")
    markup.add(button)
    return markup


def generate_main_menu_markup():
    markup = types.InlineKeyboardMarkup()
    addIngredientButton = types.InlineKeyboardButton(
        "➕ Add ingredient", callback_data="add_ingredient")
    removeIngredientButton = types.InlineKeyboardButton(
        "➖ Remove ingredient", callback_data="remove_ingredient")
    showRecipesButton = types.InlineKeyboardButton(
        "👩‍🍳 Show recipes", callback_data="show_recipe")
    markup.add(addIngredientButton)
    markup.add(removeIngredientButton)
    markup.add(showRecipesButton)
    return markup


def generate_markup_remove_ingredient():
    markup = types.InlineKeyboardMarkup()
    removeIngredientButton = types.InlineKeyboardButton(
        "➖ Remove ingredient", callback_data="remove_ingredient")
    markup.add(removeIngredientButton)
    return markup


def generate_markup_back_to_recipes():
    markup = types.InlineKeyboardMarkup()
    backButton = types.InlineKeyboardButton(
        "🔙 Back", callback_data="back_recipes")
    markup.add(backButton)
    return markup
