# $language = "Python"
# $interface = "1.0"

# 白血氧：087CBE2389F0 BA11F08C5F140B0D1080007CBE2389F0
# 灰血氧：087CBE848407 BA11F08C5F140B0D1080007CBE21EFA9
# 只能连接终端测试使用，无法使用直接连接PC的模块（无法使用script发送16进制数据）

def main():
	while True:
		result = crt.Screen.WaitForStrings(["AT+SCAN=0x087CBEB80166", "0x087CBEB80166 CON_SUCCESS", "CON_FAIL", "DISCON_SUCCESS"])

		if (result == 2):
			crt.Dialog.MessageBox("Coned, send data!")
			crt.Screen.Send("AT+EBLE?h,AA5504B10000B5" + "\r\n")
	
		elif (result == 1):
			crt.Dialog.MessageBox("Find iChoice(white)!")
			crt.Screen.Send("AT+EBLE?1,AT+CON_128=0x087CBEB80166,BA11F08C5F140B0D1080007CBE21EFA9" + "\r\n")
			crt.Screen.Send("AT+EBLE?1,AT+W_DCH=0,0" + "\r\n")

		elif (result == 0):
			crt.Dialog.MessageBox("Timed out!")
			
		else:
			crt.Dialog.MessageBox(str(result))

main()
