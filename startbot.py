import time
from time import sleep
from aiogram import Bot,Dispatcher,types,executor
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton,ContentType
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State,StatesGroup
import sqlite3


storage = MemoryStorage()
KEY = "5985821600:AAEkD4Cy4kH-TJ20YptjXXD4hQmOsxfsRxw"

#======================настройка бота===================================
bot = Bot(token=KEY,parse_mode="HTML")
dp = Dispatcher(bot)

#==================== создаем клас в виде базы даных =================
class DatabaseUser:
    def __init__(self,db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        print("Соединение создано!!!")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS user(user_count INT PRIMARY KEY,
                                                                user_id TEXT,
                                                                user_name TEXT,
                                                                answer1  TEXT,
                                                                answer2  TEXT,
                                                                answer3  TEXT);""")
        self.connection.commit()

    def add_user(self,ID,USERNAME):
        with self.connection:
            try:
                self.cursor.execute("INSERT INTO 'user' VALUES (?,?,?,?,?)",(ID,USERNAME,"null","null","null"))
                #self.connection.commit()
            except:
                print("Добавление пользователя неудачно!!!")
                pass

    def update_user_info(self,ID,USERNAME,answer1,answer2,answer3):
        with self.connection:
            self.cursor.execute("""UPDATE user SET user_id = ? ,user_name = ?,answer1 = ?,answer2 = ?,
                                answer3 = ?""",ID,USERNAME,answer1,answer2,answer3)
    def get_user_info(self):
        with self.connection:
            try:
                print("Старт проверки бд")
                for row in self.cursor.execute("""SELECT * FROM user """):
                    print(row)
                    print("Проверка бд")
            except:
                print("Не проверило")
                pass



            #return  self.cursor.execute("""SELECT * FROM user user_id = ?""",(ID,)).fetchmany[0]

    def user_exists(self,ID):
        while self.connection:
            result = self.cursor.execute("""SELECT * FROM user WHERE user_id = ?""",(ID,)).fetchmany[1]
            if not bool(len(result)):
                return False
            else:
                return True


newDB = DatabaseUser("data.db")


#========================создаем клавиатуру и кнопки =================
menu = ReplyKeyboardMarkup(row_width=2)
button_in_menu = KeyboardButton(text="Зареєструватися")
menu.add(button_in_menu)


kontakt = ReplyKeyboardMarkup(row_width=2)
button_kontakt = KeyboardButton(text="Отправить",request_contact=True)
kontakt.add(button_kontakt)

#=========================хендлеры обработка команд ===================
@dp.message_handler(commands=["start"])
async def start_bot (chat_message: types.Message):
    tex_for_new_user = f'{chat_message.chat.first_name}, вітаємо вас у нашому магазині INGAME'
    await chat_message.answer(tex_for_new_user)
    time.sleep(1)
    await bot.send_message(chat_message.from_user.id,f"Ваша айди номер {chat_message.chat.id}")
    time.sleep(1)
    await bot.send_message(chat_message.from_user.id,"Зарегестрируйтесь для получения скидки!!!",reply_markup=menu)

#=======================второй хендлер обработка кнопки =====================
@dp.message_handler(text=["Зареєструватися"])
async def start_registrator (chat_message: types.Message):
    await bot.send_message(chat_message.chat.id, "Отправть контак для регистрации!!!",reply_markup=kontakt)
    #if newDB.user_exists(chat_message.from_user.id):
        #await bot.send_message(chat_message.from_user.id,"Вы уже есть в базе даных!!!")
    #else:
        #await bot.send_message(chat_message.from_user.id,"Старт регистрации!!!")
    user_id = chat_message.chat.id
    user_name = chat_message.chat.first_name
    newDB.add_user(str(user_id),str(user_name))
    newDB.get_user_info()
    await bot.send_message(chat_message.chat.id, f"{chat_message.chat.id} +_' ' + {chat_message.chat.first_name}")

#========================старт работы бота ============================
if __name__ == "__main__":
    executor.start_polling(dp,skip_updates=True)