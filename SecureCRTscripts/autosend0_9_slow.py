import time

initialTab = crt.GetScriptTab()

def Main():
	while True:
		initialTab.Screen.Send("0123456789")
		time.sleep(0.03)
	
Main()