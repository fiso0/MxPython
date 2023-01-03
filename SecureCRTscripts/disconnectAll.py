# $language = "Python"
# $interface = "1.0"

# Get a reference to the tab that was active when this script was launched.
initialTab = crt.GetScriptTab()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def Main():
	# Activate each tab in order from left to right, and issue the command in
	# each "connected" tab...
	skippedTabs = ""
	for i in range(1, crt.GetTabCount()+1):
		tab = crt.GetTab(i)
		tab.Activate()
		# Skip tabs that aren't connected
		if tab.Session.Connected == True:
			tab.Session.Disconnect()

	# Now, activate the original tab on which the script was started
	initialTab.Activate()

Main()
