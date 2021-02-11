import os
import threading
try:
    from telegram import Bot
except:
    os.system('pip3 install python-telegram-bot')
    os.system('clear')
    from telegram import Bot
try:
    import pandas as pd
except:
    os.system('pip3 install pandas')
    os.system('clear')
    import pandas as pd
try:
    import termcolor as tc
except:
    os.system('pip3 install termcolor')
    os.system('clear')
    import termcolor as tc
from canalyse import Canalyse

settings = {
	'comm_channel' : 'vcan0',
	'interface':'socketcan',
	'source':'source.log',
	'attack':'attack.log',
	'sec_attack':'attack2.log',
	'payload':'payload.log',
	'color': "cyan"
}

try:
    import pyfiglet as pf
except:
    os.system('pip3 install pyfiglet==0.7')
    os.system('clear')
    import pyfiglet as pf 

def logo():
	print("")
	result = pf.figlet_format("CANalyse", font = "slant" ) 
	print(result)
	print("")


def main_menu():
	while True:
		os.system('clear')
		logo()
		print("")
		print("**************** Main menu *******************")
		print("")
		tc.cprint("1) CANalyse",settings['color'])
		tc.cprint("2) Connect to Telegram",settings['color'])
		tc.cprint("3) settings",settings['color'])
		tc.cprint("4) Manual",settings['color'])
		tc.cprint("5) Exit",settings['color'])
		try:
			z = int(input("=====> "))
			return z
		except:
			continue

def canalyse_menu():
	while True:
		os.system('clear')
		logo()
		print("")
		print("**************** CANalyse menu *******************")
		print("")
		tc.cprint("1) Capture source",settings['color'])
		tc.cprint("2) Capture primary attack",settings['color'])
		tc.cprint("3) Capture secondary attack (optional)",settings['color'])
		tc.cprint("4) Analyse logs",settings['color'])
		tc.cprint("5) Play payload",settings['color'])
		tc.cprint("6) Exit",settings['color'])
		print("")
		try:
			z = int(input("=====> "))
			return z
		except:
			continue
	

def settings_menu():
	while True:
		os.system('clear')
		logo()
		print("")
		print("*****************settings*****************")
		print("")
		tc.cprint("1) Comm_channel : "+settings['comm_channel'],settings['color'])
		tc.cprint("2) Color : "+settings['color'],settings['color'])
		tc.cprint("3) source filename : "+settings['source'],settings['color'])
		tc.cprint("4) primary attack filename : "+settings['attack'],settings['color'])
		tc.cprint("5) secondary attack filename : "+settings['sec_attack'],settings['color'])
		tc.cprint("6) Payload filename : "+settings['payload'],settings['color'])
		tc.cprint("7) Interface : "+settings['interface'],settings['color'])
		tc.cprint("8) Exit",settings['color'])
		print("")
		try:
			z = int(input("=====> "))
			return z
		except:
			continue

def manual():
	f = open('man.txt')
	c = f.read()
	f.close()
	while True:
		os.system('clear')
		logo()
		print(c)
		print("1) Exit")
		try:
			z = int(input("=====> "))
			return z
		except:
			continue

def show_exit():
	print(" exiting ....")
	os.system('clear')
def start_action(a):
	while True:
		print("press enter to "+a)
		try:
			h = input("===> ")
			break
		except:
			continue

def stop_action(a):
	print(" press ctrl+c when you need to stop "+a)


def show_id(l):
	while True:
		os.system('clear')
		logo()
		print("************Suspected ids*****************")
		tc.cprint("0) play all",settings['color'])
		tc.cprint("1) exit",settings['color'])
		for i in range(2,len(l)+2):
			tc.cprint(str(i)+") "+l[i-2],settings['color'])
		try:
			z = int(input("===> "))
			return z
		except:
			continue



def analysis(cn):
	print(" analysing source ...")
	try:
		df1 = cn.read(settings['source'])
	except:
		print(settings['source']+" file not available")
		start_action('Main menu')
		return
	print(" analysing attack ...")
	try:
		df2 = cn.read(settings['attack'])
	except:
		print(settings['attack']+" file not available")
		start_action('Main menu')
		return
	df3 = cn.refine(df1,df2)
	l = cn.unique_ids(df3)
	try:
		df5 = cn.read(settings['sec_attack'])
		df6 = cn.refine(df1,df5)
		df7 = cn.match(df3,df6)
		l = cn.unique_ids(df7)
	except:
		df7 = df3
	
	while True:
		z = show_id(l)
		if z == 1:
			show_exit()
			break
		elif z == 0:
			print("writing payload")
			cn.write(df7,settings['payload'])
			play_payload(cn)
		elif z < len(l)+2:
			print("writing payload")
			df4 = df3.loc[df3.id==l[z-2]]
			df4 = df4.reset_index()
			cn.write(df4,settings['payload'])
				



def play_payload(cn):
	playthread = threading.Thread(target = cn.canplay,args=(settings['payload'],))
	showthread = threading.Thread(target = cn.show_log,args=(settings['payload'],"all"))
	showthread.start()
	playthread.start()
	showthread.join()
	playthread.join()

def connect_to_Telegram():
	while True:
		try:
			z = input("Enter the telegram API token : ")
			bot = Bot(token=z)
			print("connected with telegram")
			print("send commands to get started")
			return bot
		except:
			print("Invalid token key , try again...")
def get_new_message(bot,update_id=None):
	while  True:
		try:
			msg = bot.get_updates()[-1]
			if msg.update_id != update_id:
				return msg
		except:
			pass

'''
candump source
candump attack
candump sec_attack

analyse source attack sec_attack
	refine source attack
	match attack sec_attack
play file
show file
'''

def upload(bot,msg,filename):
	chat_id = msg.message.chat_id
	bot.send_document(chat_id=chat_id,document=open(filename,'rb'))

def exec_message(bot,msg,cn):
	text = msg.message.text
	chat_id = msg.message.chat_id
	text = text.lower().strip().split(" ")
	if text[0] == 'record':
		telegram_record(bot,msg,settings[text[1]],cn,text[2])
	elif text[0] == 'play':
		if len(text) == 4:
			for i in range(int(text[1])):
				telegram_play(bot,msg,settings[text[2]],cn,text[3])
		else:
			for i in range(int(text[1])):
				telegram_play(bot,msg,settings[text[2]],cn)
	elif text[0] == 'analyse':
		telegram_analyse(bot,msg,text[1],text[2],cn)

	elif text[0] == 'get' or text[0] == 'download':
		upload(bot,msg,text[1])
	elif text[0] == 'menu' or text[0] == 'whatcanido':
		bot.send_message(chat_id=chat_id,text="'record (source / attack) (seconds)' to record the files ")
		bot.send_message(chat_id=chat_id,text="'play filename can_id (optional)' to canplay")
		bot.send_message(chat_id=chat_id,text="'analyse source attack' to analyse files")
		bot.send_message(chat_id=chat_id,text="'get filename' to download any file")

	else:
		bot.send_message(chat_id=chat_id,text="Invalid command type 'Menu' for manual")

def telegram_record(bot,msg,filename,cn,time=0):
	chat_id = msg.message.chat_id
	bot.send_message(chat_id=chat_id,text="recording started")
	cn.candump(filename,time)
	bot.send_message(chat_id=chat_id,text="recording completed")



def telegram_play(bot,msg,filename,cn,can_id=None):
	chat_id = msg.message.chat_id
	bot.send_message(chat_id=chat_id,text="executing payload")
	print(can_id)
	if can_id != None:
		df = cn.read(filename)
		print(df)
		print(df.loc[df.id==can_id])
		df = df.loc[df.id==can_id]
		df = df.reset_index()
		print(df)
		cn.write(df,settings['payload'])
	cn.canplay(filename)
	bot.send_message(chat_id=chat_id,text="payload execution completed !")




def telegram_analyse(bot,msg,source,attack,cn):
	chat_id = msg.message.chat_id
	bot.send_message(chat_id=chat_id,text="analysis started")
	source = cn.read(source)
	attack = cn.read(attack)
	payload = cn.refine(source,attack)
	cn.write(payload,settings['payload'])
	bot.send_message(chat_id=chat_id,text="analysis completed")
	bot.send_message(chat_id=chat_id,text="written payload at "+settings['payload'])
	bot.send_message(chat_id=chat_id,text="Suspected IDs are")
	ids = cn.unique_ids(payload)
	bot.send_message(chat_id=chat_id,text='\n'.join(ids))



def main():
	while True:
		o = main_menu()
		if o == 1:
			cn = Canalyse(settings['comm_channel'],settings['interface'])
			while True:
				p = canalyse_menu()
				if p == 1:
					start_action('capture source')
					stop_action('capturing source')
					cn.candump(settings['source'])
				elif p == 2:
					start_action('capture primary attack')
					stop_action('capturing primary attack')
					cn.candump(settings['attack'])
					#cn.copy(settings['attack'],settings['sec_attack'])
				elif p == 3:
					start_action('capture secondary attack')
					stop_action('capturing secondary attack')
					cn.candump(settings['sec_attack'])
				elif p == 4:
					start_action('start analysis')
					analysis(cn)
				elif p == 5:
					start_action('start playing')
					play_payload(cn)
				elif p == 6:
					show_exit()
					break
		elif o == 2:
			cn = Canalyse(settings['comm_channel'],settings['interface'])
			bot = connect_to_Telegram()
			msg = get_new_message(bot)
			while True:
				msg = get_new_message(bot,msg.update_id)
				exec_message(bot,msg,cn)
			pass#telegram

		elif o == 3:
			while True:
				p = settings_menu()
				if p == 1:
					ch = input("comm_channel name : ")
					settings['comm_channel'] = ch
				elif p == 2:
					c_list = ['red','cyan','green','yellow','grey','blue','magenta','white']
					os.system('clear')
					for c in c_list:
						tc.cprint(" "+c,c)
					cl = input("color : ")
					if cl in c_list:
						settings['color'] = cl
				elif p == 3:
					sr = input("source name : ")
					settings['source'] = sr
				elif p == 4:
					at = input("primary attack name : ")
					settings['attack'] = at
				elif p == 5:
					at2 = input("secondary attack name : ")
					settings['sec_attack'] = at2
				elif p == 6:
					pl = input("payload name : ")
					settings['payload'] = pl
				elif p == 7:
					pl = input("Interface type : ")
					settings['interface'] = pl
				elif p == 8:
					show_exit()
					break

		elif o == 4:
			while True:
				p = manual()
				if p == 1:
					show_exit()
					break

		elif o == 5:
			show_exit()
			break


if __name__ == '__main__':
	main()
