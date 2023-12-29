import os
from handlers import ingredient_remove_handler, ingredient_suggestion_handler, recipe_option_handler, show_recipe_handler
from markups import *
from retrievers import *
import telebot

BOT_TOKEN = os.environ.get('BOT_TOKEN')
FOOD_APP_ID = os.environ.get('FOOD_APP_ID')
FOOD_APP_KEY = os.environ.get('FOOD_APP_KEY')
RECIPE_APP_ID = os.environ.get('RECIPE_APP_ID')
RECIPE_APP_KEY = os.environ.get('RECIPE_APP_KEY')

bot = telebot.TeleBot(BOT_TOKEN)

user_data = {}
chat_state = {}


def show_menu(chat_id, user_id):

    collected_ingredients_formatted = ""
    if user_id in user_data:
        collected_ingredients_formatted = format_ingredient_list(
            user_data[user_id]["collected_ingredients"])

    responseString = "What would you like to do?"
    if len(collected_ingredients_formatted) > 0:
        responseString = f"Your current ingredients:\n\n{collected_ingredients_formatted}\n{responseString}"
    bot.send_message(chat_id, responseString,
                     reply_markup=generate_main_menu_markup())


def edit_to_show_menu(chat_id, user_id, message_id):

    collected_ingredients_formatted = ""
    if user_id in user_data:
        collected_ingredients_formatted = format_ingredient_list(
            user_data[user_id]["collected_ingredients"])

    responseString = "What would you like to do?"
    if len(collected_ingredients_formatted) > 0:
        responseString = f"Your current ingredients:\n\n{collected_ingredients_formatted}\n{responseString}"
    bot.edit_message_text(chat_id=chat_id,
                          message_id=message_id,
                          text=responseString,
                          reply_markup=generate_main_menu_markup())


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.send_message(message.chat.id, "What would you like to do?",
                     reply_markup=generate_main_menu_markup())


@bot.message_handler(func=lambda msg: True)
def echo_all(message):

    chat_id = message.chat.id
    if chat_id in chat_state and chat_state[chat_id] == 'waiting_for_ingredient':
        user_input = message.text
        del chat_state[chat_id]
        options = get_ingredients_suggestions(
            user_input, FOOD_APP_ID, FOOD_APP_KEY)
        user_id = message.from_user.id
        initIngredients = []
        if user_id in user_data and "collected_ingredients" in user_data[user_id]:
            initIngredients = user_data[user_id]["collected_ingredients"]
        user_data[user_id] = {
            "options": options, "collected_ingredients":  initIngredients}

        bot.send_message(message.chat.id, "Choose an ingredient:",
                         reply_markup=generate_options_markup(1, options, 'opt_', 'page_'))


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):

    if call.data.startswith("opt_"):
        ingredient_suggestion_handler(call, user_data, bot)

    elif call.data.startswith("recipe_"):
        recipe_option_handler(call, user_data, bot)

    elif call.data.startswith("ingredientremove_"):
        ingredient_remove_handler(call, user_data, bot)

    elif call.data.startswith("page_") and call.from_user.id in user_data:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Choose an ingredient:",
                              reply_markup=generate_options_markup(int(call.data.split("_")[1]), user_data[call.from_user.id]['options'],
                                                                   'opt_', 'page_'))

    elif call.data.startswith("recipepage_") and call.from_user.id in user_data:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Choose recipe:",
                              reply_markup=generate_options_markup(int(call.data.split("_")[1]), user_data[call.from_user.id]['recipes'],
                                                                   'recipe_', 'recipepage_'))

    elif call.data.startswith("ingredientremovepage_") and call.from_user.id in user_data:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Remove an ingredient:",
                              reply_markup=generate_options_markup(int(call.data.split("_")[1]), user_data[call.from_user.id]['collected_ingredients'],
                                                                   'ingredientremove_', 'ingredientremovepage_'))

    elif call.data == "no data":
        bot.answer_callback_query(
            call.id, f"This button is awesome, but why would one tap it")

    elif call.data == "add_ingredient":
        chat_state[call.message.chat.id] = 'waiting_for_ingredient'
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=f"Please type your ingredient",
                              reply_markup=None)

    elif call.data == "remove_ingredient":
        if call.from_user.id not in user_data or len(user_data[call.from_user.id]["collected_ingredients"]) == 0:
            bot.answer_callback_query(
                call.id, "Nothing to remove, please add some ingredients first")
        else:
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text=f"Remove an ingredient:",
                                  reply_markup=generate_options_markup(1, user_data[call.from_user.id]["collected_ingredients"],
                                                                       'ingredientremove_', 'ingredientremovepage_'))

    elif call.data == "show_recipe":
        show_recipe_handler(call, user_data, bot,
                            RECIPE_APP_ID, RECIPE_APP_KEY)

    elif call.data == "back_recipes":
        if call.from_user.id in user_data:
            collected_ingredients_formatted = format_ingredient_list(
                user_data[call.from_user.id]["collected_ingredients"])
        else:
            collected_ingredients_formatted = ""
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=f"Your ingredients:\n\n{collected_ingredients_formatted}\nChoose recipe:",
                              reply_markup=generate_options_markup(1, user_data[call.from_user.id]["recipes"], 'recipe_', 'recipepage_'))

    elif call.data == "back_menu":
        edit_to_show_menu(call.message.chat.id,
                          call.from_user.id, call.message.message_id)


bot.infinity_polling()
