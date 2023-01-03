import sys

MYOUT = 0

def myprint(*objects, sep=' ', end='\n', flush=False):
	if MYOUT == 0:
		print(*objects,sep=sep,end=end,flush=flush)
	else:
		try:
			f = open('test_myprint.txt', 'x')
		except FileExistsError:
			f = open('test_myprint.txt', 'a')
		print(*objects,sep=sep,end=end,file=f,flush=flush)

		
# TEST:
# to console
myprint('124')

a = 1
myprint(a)

myprint('\tbetween line %d'%(a),end='')
myprint('124')

# to file
MYOUT = 1

myprint('122')

a = 1
myprint(a)

myprint('\tbetween line %d'%(a),end='')
myprint('122')
input()