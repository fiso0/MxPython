import time

initialTab = crt.GetScriptTab()

def Main():
	while True:
		initialTab.Screen.Send("$reset,1,0\r\n")
		time.sleep(5)
	
Main()