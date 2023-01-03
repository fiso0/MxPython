import time

initialTab = crt.GetScriptTab()

def Main():
	while True:
		initialTab.Screen.Send("AT+TEST\r\n")
		time.sleep(1)
		# initialTab.Session.Disconnect()
		# time.sleep(1)
		# initialTab.Session.Connect()
		# time.sleep(1)
		initialTab.Screen.Send("AT+BOOT=F\r\n")
		time.sleep(30)
	
Main()