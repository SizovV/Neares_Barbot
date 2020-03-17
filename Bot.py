import telebot
import Config
import pars_ing
import data
import importlib
import asyncio
from telebot import types
from telebot import apihelper

apihelper.proxy = {'http': 'http://catalog.live.ovh:8080'}
qw =  []
bot = telebot.TeleBot(Config.TOKEN)
i = 0
id2=275457031

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "Привет,\nЯ бот который ищет ближайшие бары.\nПросто отправь мне свою геолокацию и я покажу ближайшие.\n\nP.S. В данный момент я нахожусь в режиме разработки, а это значит что функционал не столь полон, как того хочет разработчик")
    bot.send_message(message.chat.id, "Кстати, если найдешь баг или фичу срузу пиши @ghusty_dab")

@bot.message_handler(content_types=['location'])
def handle_location(message):
    print(message.location.longitude, message.location.latitude, message.chat.id, message.chat.first_name)
    i = 0
    try:
        data.mycursor.execute("SELECT * FROM bars_fav")
    except:
        importlib.reload(data)
        data.mycursor.execute("SELECT * FROM bars_fav")
    resa = data.mycursor.fetchall()
    for j in resa:
        dist = pars_ing.distance(message.location.latitude, message.location.longitude, j[5], j[6])
        if dist<1000:
            markup = types.InlineKeyboardMarkup(row_width=1)
            need_url = "https://yandex.ru"+str(j[4])
            item2 = types.InlineKeyboardButton("Поехали!", url = need_url)
            markup.add(item2)
            bot.send_message(message.chat.id, "Из Избранного\n{}-й Ближайший бар: {}\nНа расстоянии: {} метров\nРейтинг: {} \nПо адресу: {}\nЦены: {}".format(i+1, j[0], int(dist), j[1], j[3], j[2]), reply_markup=markup)
            i+=1
    a = pars_ing.get_ip(message.location.longitude, message.location.latitude)
    print(len(a))
    t=i
    while(t+1<6):
        try:
            markup = types.InlineKeyboardMarkup(row_width=1)
            need_url = "https://yandex.ru"+str(a[3][i])
            item2 = types.InlineKeyboardButton("Поехали!", url = need_url)
            markup.add(item2)
            bot.send_message(message.chat.id, "{}-й Ближайший бар: {}\nНа расстоянии: {} метров\nРейтинг: {} \nПо адресу: {}\n{}".format(t+1, a[2][t-i], int(a[4][t-i]), a[1][t-i], a[0][t-i], a[5][i-1]), reply_markup=markup)
            t+=1
        except:
            bot.send_message(message.chat.id, "Тут не так много баров в районе 2 км, как ты надеешься...")
            break
    find_id="SELECT * FROM guys WHERE id={}".format(message.chat.id)
    data.mycursor.execute(find_id)
    resa = data.mycursor.fetchall()
    if len(resa) == 0:
        guy_info = (message.chat.id, message.location.longitude, message.location.latitude)
        sql_formula = ("INSERT INTO guys (id, last_longitude, last_latitude, last_visit_time, last_visit_data)"
        "VALUES (%s, %s, %s, curtime(), curdate())")
        data.mycursor.execute(sql_formula, guy_info)
        data.mydb.commit()
        sql_formula1 = str(message.chat.first_name)
        bot.send_message(Config.my_id, "new"+str(sql_formula1))
    else:
        sql_formula = ("UPDATE guys SET last_longitude=%s, last_latitude=%s, last_visit_time=curtime(), last_visit_data=curdate() WHERE id = %s")
        guy_info = (message.location.longitude, message.location.latitude, message.chat.id)
        data.mycursor.execute(sql_formula, guy_info)
        data.mydb.commit()
        bot.send_message(Config.my_id, str(message.chat.first_name))

@bot.message_handler(content_types=['text'])
def lalala(message):
    try:
        a = str(message.text.split("\n")[0].split(" ")[0])+" "+str(message.text.split("\n")[0].split(" ")[1])
        if a=="Добавь этот:":
            try:
                data.mycursor.execute("SELECT last_longitude, last_latitude FROM guys WHERE id ={}".format(message.chat.id))
            except:
                importlib.reload(data)
                data.mycursor.execute("SELECT last_longitude, last_latitude FROM guys WHERE id ={}".format(message.chat.id))
            resa = data.mycursor.fetchall()
            print(resa)
            a = pars_ing.get_name(message.text.split("\n")[1], resa[0][0], resa[0][1])
            bot.send_message(message.chat.id, "Ты добавил бар {}\nПо адресу:{}\nв Избраное!".format(a[0], a[1]))
            bot.send_message(Config.my_id, "{} добавил бар {}\nПо адресу:{}\nв Избраное!".format(message.chat.first_name, a[0], a[1]))
        else:
            bot.send_message(message.chat.id, message.text)
    except:
        bot.send_message(message.chat.id, message.text)

@bot.message_handler(content_types=['photo'])
def photo(message):
    bot.send_message(message.chat.id, "Ого!!! Какая крутая фотка, это ты сам сделал? \nУ тебя таллант")



# Runing
bot.polling(none_stop=True)
