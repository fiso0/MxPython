import time

initialTab = crt.GetScriptTab()

def Main():
	while True:
		# initialTab.Screen.Send("$reset,1,2\r\n") # cold reset
		initialTab.Screen.Send("$reset,1,0\r\n") # warn reset
		# time.sleep(1)
		# initialTab.Screen.Send("AT+ROMA_INFO=?\r\n")
		# time.sleep(1)
		# initialTab.Screen.Send("AT+ROMA_INFO=,,,,,123\r\n")
		
		
		# time.sleep(121)
		time.sleep(40)
		
		
		# initialTab.Session.Disconnect()
		# time.sleep(1)
		# initialTab.Session.Connect()
		# time.sleep(1)
		# initialTab.Screen.Send("AT+BOOT=F\r\n")
		# time.sleep(30)
	
Main()