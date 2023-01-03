# $language = "Python"

# $interface = "1.0"

 

def main():
	tab = crt.GetScriptTab()
	# objTab = crt.GetScriptTab()
	# objConfig = objTab.Session.Config
	# szUsername = objConfig.GetOption("Username")
	# crt.Dialog.MessageBox("Username:"+szUsername)
	# if tab.Session.Connected == True:
		# tab.Session.Disconnect()
	while(tab.Session.Connected == True):
		tab.Session.Disconnect()
		# pass
	# crt.Dialog.MessageBox("Disconnected")
	tab.Session.Connect("/S Serial-COM23-CH340")
	# crt.Dialog.MessageBox("Reconnected")

main()
