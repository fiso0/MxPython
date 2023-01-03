#$language = "VBScript"
#$interface = "1.0"

crt.Screen.Synchronous = True

' This automatically generated script may need to be
' edited in order to work correctly.

Sub Main
	crt.Screen.Send "AT+LOGLVL3" & chr(13)
	crt.Screen.Send chr(10)
End Sub
