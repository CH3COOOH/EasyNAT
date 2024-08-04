import os
import sys

PATH_OLD = '/tmp/easynat_conf.old'

def remove_ch(text, remove_list):
	text_ = text
	for s in remove_list:
		text_ = text_.replace(s, '')
	return text_

def parse_config(config_raw):
	rule_lines = []
	for r in config_raw.split('\n'):
		if ('#' in r) or (r == ''):
			continue
		try:
			rule_line = remove_ch(r, ['\n', '\r'])
			rule_lines.append(rule_line.split(' '))
		except:
			print('** BAD RULE: '+r)
			continue
	return rule_lines

def rule_to_iptbl(proto, src_ip, src_port, des_ip, des_port, isAdd):
	act = '-A'
	if isAdd == False:
		act = '-D'
	if src_ip == '*':
		iptbl_pre = 'iptables -t nat '+act+' PREROUTING -p '+proto+' --dport '+src_port+' -j DNAT --to-destination '+des_ip+':'+des_port
	else:
		iptbl_pre = 'iptables -t nat '+act+' PREROUTING -p '+proto+' -d '+src_ip+' --dport '+src_port+' -j DNAT --to-destination '+des_ip+':'+des_port
	iptbl_pos = 'iptables -t nat '+act+' POSTROUTING -p tcp -d '+des_ip+' --dport '+des_port+' -j MASQUERADE'
	return iptbl_pre, iptbl_pos

def config_to_iptbl(config_path, isExecute, isAdd):
	with open(config_path, 'r') as o:
		config_raw = o.read()
	rule_lines = parse_config(config_raw)
	cmd_list = []
	for r in rule_lines:
		if isAdd:
			iptbl_pre, iptbl_pos = rule_to_iptbl(r[0], r[1], r[2], r[3], r[4], True)
			print('+|'+iptbl_pre)
			print(' |'+iptbl_pos)
		else:
			iptbl_pre, iptbl_pos = rule_to_iptbl(r[0], r[1], r[2], r[3], r[4], False)
			print('-|'+iptbl_pre)
			print(' |'+iptbl_pos)
		cmd_list.append(iptbl_pre)
		cmd_list.append(iptbl_pos)
	return cmd_list

def write_to_tmp(config_path):
	with open(config_path, 'rb') as o:
		buff = o.read()
	with open(PATH_OLD, 'wb') as o:
		o.write(buff)

def main(config_path, isExecute):
	cmd_add = config_to_iptbl(config_path, isExecute, isAdd=True)
	if isExecute == True:
		print('--- Execute ADD ---')
		for c in cmd_add:
			os.system(c)
	if os.path.exists(PATH_OLD):
		cmd_del = config_to_iptbl(PATH_OLD, isExecute, isAdd=False)
		if isExecute == True:
			print('--- Remove Old ---')
			for c in cmd_del:
				os.system(c)
			write_to_tmp(config_path)
	else:
		if isExecute == True:
			write_to_tmp(config_path)

if __name__ == '__main__':
	print('== Easy Redirect ==')
	if len(sys.argv) == 3 and sys.argv[2] == '-e':
		main(sys.argv[1], True)
	else:
		print('** Evaluation mode **')
		main(sys.argv[1], False)