#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np
import logging
from nltk.translate.bleu_score import sentence_bleu
from seq2seq.util.checkpoint import Checkpoint
from seq2seq.evaluator import Predictor
from seq2seq.util.data_util import basic_tokenizer

def deltaBLEU(output_file, reference_file):
	answers = []
	references = []
	with open(output_file) as f:
		for line_ in f:
			line = line_.strip()
			answers.append([x for x in line])
	lines = []	
	with open(reference_file) as f:
		for line_ in f:
			line = line_.strip().split('	')
			if len(line)<2:
				if len(lines)!=0:
					references.append(lines)
					lines = []
			if len(line)==2:
				lines.append(([x for x in line[0]], float(line[1])))
	BLEUs = []
	for i in range(len(answers)):
		weighted_bleus = []
		answer = answers[i]
		reference = references[i]
		for item in reference:
			weighted_bleus.append(sentence_bleu([item[0]], answer) * item[1]) 
		BLEUs.append(np.mean(np.asarray(weighted_bleus, dtype=np.float32)))
	return np.mean(np.asarray(BLEUs, dtype=np.float32))

def test(expt_dir, checkpoint, test_file, output_file):
	if checkpoint is not None:
		checkpoint_path = os.path.join(expt_dir, Checkpoint.CHECKPOINT_DIR_NAME, checkpoint)		
		logging.info("loading checkpoint from {}".format(checkpoint_path))
		checkpoint = Checkpoint.load(checkpoint_path)
		seq2seq = checkpoint.model
		input_vocab = checkpoint.input_vocab
		output_vocab = checkpoint.output_vocab	
	else:
		raise Exception("checkpoint path does not exist")

	predictor = Predictor(seq2seq, input_vocab, output_vocab)

	output = open(output_file, 'ab')

	with open(test_file) as f:
		for line_ in f:
			line = line_.strip().split('<s>')
			if len(line)!=0:
				question = basic_tokenizer(line[-2])
				answer = predictor.predict(question)[:-1]
				output.write(''.join(answer)+'\n')

if __name__ == '__main__':
	expt_dir = 'expir'
	checkpoints = os.listdir(os.path.join(expt_dir, Checkpoint.CHECKPOINT_DIR_NAME))
	test_file = 'data/TestData/questions50.txt'
	reference_file = 'data/TestData/answers50.txt'
	for checkpoint in checkpoints:
		output_file = 'data/TestData/output_%s.txt'%checkpoint
		test(expt_dir, checkpoint, test_file, output_file)
		delta_bleu = deltaBLEU(output_file, reference_file)
		print ('deltaBLEU at %s: %f'%(checkpoint, delta_bleu))
	