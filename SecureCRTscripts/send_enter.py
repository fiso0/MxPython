import time

initialTab = crt.GetScriptTab()

def Main():
	initialTab.Screen.Send("123")
	initialTab.Screen.Send("\r\n")
	initialTab.Screen.Send("456")
	time.sleep(0.02)
	
Main()