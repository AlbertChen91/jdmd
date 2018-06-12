#!/usr/bin/python
# -*- coding: UTF-8 -*-

import jieba
import random

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

train_data_dir = '../../data/preliminaryData/'

def basic_tokenizer(sentence):
	"""Very basic tokenizer: split the sentence into a list of tokens."""
	sentence = list(jieba.cut(sentence))
	return sentence

def list2string(l):
	return ' '.join(l)

def isVilid(one, two):
	one = set(one)
	two = set(two)
	if (len(one)==0 or list(one)[0]==' ') or (len(two)==0 or list(two)[0]==' '):
		return 0
	else:
		return 1

def generate(data, file):
	with open(train_data_dir+file, 'ab') as f:
		for frag in data:
			first = frag[0]
			for i in range(1, len(frag)):
				second = frag[i]
				if isVilid(first, second):
					f.write('	'.join([list2string(first), list2string(second)])+'\n')
				first = frag[i]

def gen_train_dev():
	# generate training and develop datasets
	fragments = []
	sentences = []
	frag_id = ''

	with open('chat.txt') as f:
		for line_ in f:
			# ﻿输入数据：11c683acd7a  USERID_10069726 1   0   1       这边为您查询，#E-s[数字x]，~有怠慢之处还请您谅解哟!
			line = line_.strip().split('	')
			line_frag_id = line[0]
			line_sentence = line[6]
			if frag_id!='' and line_frag_id!=frag_id:
				fragments.append(sentences)
				sentences = []
			sentences.append(basic_tokenizer(line_sentence))
			frag_id = line_frag_id		
		fragments.append(sentences)

	random.shuffle(fragments)

	cutin = int(len(fragments)*0.7)
	train = fragments[:cutin]
	dev = fragments[cutin:]

	generate(train, 'train.txt')
	generate(dev, 'dev.txt')
	print 'OK'
