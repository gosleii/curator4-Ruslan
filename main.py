import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State

state_storage = StateMemoryStorage()
bot = telebot.TeleBot("6778842641:AAFKSD_N0Ti7SJ9_6fEh_usqr8j78XoP4ew",
                      state_storage=state_storage, parse_mode='Markdown')


class PollState(StatesGroup):
 name = State()
 age = State()


class HelpState(StatesGroup):
 wait_text = State()


text_poll = "Ну давай опросник)"
text_button_1 = "Что ты умеешь?"
text_button_2 = "Кто тебя создал?"
text_button_3 = "Что еще расскажешь?"

menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
 telebot.types.KeyboardButton(
  text_poll,
 )
)
menu_keyboard.add(
 telebot.types.KeyboardButton(
  text_button_1,
 )
)

menu_keyboard.add(
 telebot.types.KeyboardButton(
  text_button_2,
 ),
 telebot.types.KeyboardButton(
  text_button_3,
 )
)


@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
 bot.send_message(
  message.chat.id,
  'Приветик! Чем займемся мой друг?',
  reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
 bot.send_message(message.chat.id, 'Будьте добры *Ваше* _имя_?')
 bot.set_state(message.from_user.id, PollState.name, message.chat.id)


@bot.message_handler(state=PollState.name)
def name(message):
 with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
  data['name'] = message.text
 bot.send_message(message.chat.id, 'Супер! [Ваш](https://www.example.com/) `возраст?`')
 bot.set_state(message.from_user.id, PollState.age, message.chat.id)


@bot.message_handler(state=PollState.age)
def age(message):
 with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
  data['age'] = message.text
 bot.send_message(message.chat.id, 'Спасибо за регистрацию! Какую не скажу  :Ъ', reply_markup=menu_keyboard)
 bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):
 bot.send_message(message.chat.id, "В общем и целом, я пока ничего не умею, но я усердно стараюсь ;) "
                                   "Могу зарегестрировать тебя на что то интересное... если ты нажмешь 'Опросник'",
                  reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
 bot.send_message(message.chat.id, "Очень интересный вопрос. Меня создал начинающий программист,"
                                   "который уже знает язык программирования Phyton, и он учится в Благовещенске на программиста,"
                                   "ведь он любит программировать и я надеюсь у него все получится!",
                  reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_button_3 == message.text)
def help_command(message):
 bot.send_message(message.chat.id, "В Питоне все выводится с помощью print()", reply_markup=menu_keyboard)


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()
