import time

initialTab = crt.GetScriptTab()

def Main():
	num = 0
	while True:
		initialTab.Screen.Send(str(num) + "\r\n")
		num = num + 1
		time.sleep(0.5)
	
Main()