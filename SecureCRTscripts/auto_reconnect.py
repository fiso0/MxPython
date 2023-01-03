# $language = "Python"

# $interface = "1.0"

 

def main():
	tab = crt.GetScriptTab()
	title = tab.Caption
	# crt.Dialog.MessageBox("title:"+title)
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
	tab.Session.Connect("/S "+title)
	# crt.Dialog.MessageBox("Reconnected")

main()
