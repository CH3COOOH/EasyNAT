from os import system
from sys import argv

def replaceKeys(origin, keys):
	isFirst = True
	newtext = ''
	for k in keys.keys():
		if isFirst:
			newtext = origin.replace(k, keys[k])
			isFirst = False
		else:
			newtext = newtext.replace(k, keys[k])
	return newtext

def readAndExec(fname, n_loop=65535, debug=True):
	if debug == False:
		print('*** EXEC MODE ***')
	var_dict = {}
	isHeader = True
	with open(fname, 'r') as o:
		for i in range(n_loop):
			buff = o.readline().replace('\n', '')
			# print(buff)
			if buff == '' or buff[0] == '#':
				continue
			if buff == 'EOF':
				break
			if isHeader == True:
				cmd = buff
				isHeader = False
				continue

			param = buff.split()
			if param[0][0] == '$':
				var_dict[param[0]] = param[1]
			else:
				pr = param[1]
				if param[2] == '0':
					si = ''
				elif param[2] in var_dict.keys():
					si = var_dict[param[2]]
				else:
					si = param[2]
				sp = param[3]
				if param[4] in var_dict.keys():
					di = var_dict[param[4]]
				else:
					di = param[4]
				dp = param[5]
				cmd_parse = replaceKeys(cmd, 
					{'$pr': pr, '$si': si, '$sp': sp, '$di': di, '$dp': dp})
				print(cmd_parse)
				if debug == False:
					system(cmd_parse)
					
	print('End of the process.')

def main(config_fname, debug):
	readAndExec(config_fname, debug=debug)

if __name__ == '__main__':
	print('Easy Redirect')
	main(argv[1], int(argv[2]))