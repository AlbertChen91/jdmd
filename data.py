#!/usr/bin/python
# -*- coding: UTF-8 -*-

import jieba
import random

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def basic_tokenizer(sentence):
	"""Very basic tokenizer: split the sentence into a list of tokens."""
	sentence = list(jieba.cut(sentence))
	return sentence

def list2string(l):
	return ' '.join(l)

def isOK(one, two):
	one = set(one)
	two = set(two)
	if (len(one)==0 or list(one)[0]==' ') or (len(two)==0 or list(two)[0]==' '):
		return 0
	else:
		return 1

def generate(data, file):
	with open(file, 'ab') as f:
		for frag in data:
			first = frag[0]
			for i in range(1, len(frag)):
				second = frag[i]
				if isOK(first, second):
					f.write('	'.join([list2string(first), list2string(second)])+'\n')
				first = frag[i]

fragments = []
sentences = []
frag_id = ''
turn = -1
chat_line = ''

with open('chat.txt') as f:
	for line_ in f:
		# ﻿输入数据：11c683acd7a  USERID_10069726 1   0   1       这边为您查询，#E-s[数字x]，~有怠慢之处还请您谅解哟!
		line = line_.strip().split('	')
		line_frag_id = line[0]
		line_speaker = int(line[2])
		line_sentence = line[6]
		if frag_id!='' and line_frag_id!=frag_id:
			if len(sentences)!=0:			
				fragments.append(sentences)
				sentences = []
		if turn!=-1 and line_speaker!=turn:
			sentences.append(basic_tokenizer(chat_line))
			chat_line = ''
		chat_line += line_sentence
		turn = line_speaker
		frag_id = line_frag_id	
	if len(sentences)!=0:	
		fragments.append(sentences)

random.shuffle(fragments)

cutin = int(len(fragments)*0.9)
train = fragments[:cutin]
dev = fragments[cutin:]

generate(train, 'train.txt')
generate(dev, 'dev.txt')
print 'OK'
