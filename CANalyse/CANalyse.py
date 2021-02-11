import os
import threading
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
from lib import Canalyse

settings = {
	'comm_channel' : 'vcan0',
	'source':'source.log',
	'attack':'attack.log',
	'sec_attack':'attack2.log',
	'payload':'payload.log',
	'color': "green"
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
		tc.cprint("1) CANalyse",settings['color'])
		tc.cprint("2) settings",settings['color'])
		tc.cprint("3) Manual",settings['color'])
		tc.cprint("4) Exit",settings['color'])
		try:
			z = int(input("=====> "))
			return z
		except:
			continue

def canalyse_menu():
	while True:
		os.system('clear')
		logo()
		print("**************** CANalyse *******************")
		print("")
		print("")
		tc.cprint("1) Capture source",settings['color'])
		tc.cprint("2) Capture primary attack",settings['color'])
		tc.cprint("3) Capture secondary attack (optional)",settings['color'])
		tc.cprint("4) Brew payload",settings['color'])
		tc.cprint("5) Exploit",settings['color'])
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
		print("**************** Settings *******************")
		print("")
		print("")
		tc.cprint("1) Comm_channel : "+settings['comm_channel'],settings['color'])
		tc.cprint("2) Color : "+settings['color'],settings['color'])
		tc.cprint("3) source filename : "+settings['source'],settings['color'])
		tc.cprint("4) primary attack filename : "+settings['attack'],settings['color'])
		tc.cprint("5) secondary attack filename : "+settings['sec_attack'],settings['color'])
		tc.cprint("6) Payload filename : "+settings['payload'],settings['color'])
		tc.cprint("7) Exit",settings['color'])
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
		#print(df7)
		print("************Suspected ID's*****************")
		tc.cprint("0) Play all the ID's",settings['color'])
		tc.cprint("1) exit",settings['color'])
		for i in range(2,len(l)+2):
			tc.cprint(str(i)+") "+l[i-2],settings['color'])
		try:
			z = int(input("===> "))
			return z
		except:
			continue



def analysis(cn):
	print(" Analysing source ...")
	try:
		df1 = cn.read(settings['source'])
	except:
		print(settings['source']+" file not available")
		start_action('Main menu')
		return
	print(" Analysing attack ...")
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


def main():
	while True:
		o = main_menu()
		if o == 1:
			cn = Canalyse(settings['comm_channel'])
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
					show_exit()
					break

		elif o == 3:
			while True:
				p = manual()
				if p == 1:
					show_exit()
					break

		elif o == 4:
			show_exit()
			break

if __name__ == '__main__':
	main()
