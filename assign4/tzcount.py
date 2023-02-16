#!/usr/bin/python3

import sys
import subprocess

grep_process = subprocess.Popen(['grep', '^Date:'], stdin=sys.stdin, stdout=subprocess.PIPE)
tr_process = subprocess.Popen(['tr', '-s', ' '], stdin=grep_process.stdout, stdout=subprocess.PIPE)
cut_process = subprocess.Popen(['cut', '-d', ' ', '-f', '7'], stdin=tr_process.stdout, stdout=subprocess.PIPE)
output = cut_process.stdout.read().decode("utf-8").splitlines()

map = {}

for i in output:
	if i in map:
		map[i] += 1
	else:
		map.update({i : 1})

sorted = sorted(map)
for i in reversed(sorted):
	if i[0] == '-':
		print(i + ' ' + str(map[i]))
for i in sorted:
	if i[0] == '+':
		print(i + ' ' + str(map[i]))