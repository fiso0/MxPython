# $language = "Python"

# $interface = "1.0"

 

def main():
	result = crt.Screen.WaitForStrings(["+CSQ: 1", "bar", "quux", "gee"], 30)

	#crt.Dialog.MessageBox(str(result))

	if (result == 1):

		crt.Dialog.MessageBox("Got +CSQ: 1!")

	if (result == 0):

		crt.Dialog.MessageBox("Timed out!")


main()
