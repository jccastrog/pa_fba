#!/usr/bin/env python
'''
@name: meanContigLength.py
@author: Juan C. Castro <jccastrog at gatech dot edu>
@update: 04-May-2016
@version: 1.0
@license: artistic license 2.0
'''

'''1.0 Import packages and initialize variables'''
#================1.1 Import packages===============
import os, sys, argparse
from Bio import SeqIO
import numpy as np
#import matplotlib.pyplot as plt
#import plotly.plotly as py

#=============1.2 Initialize variables=============
#1.2.1 Parser variables============================
parser = argparse.ArgumentParser(description="meanContigLength: Calculate the mean length of an assembly and print a list of the contig sizes [jccastrog@gatech.edu]")
group = parser.add_argument_group('Required arguments')
group.add_argument('-t', action='store', dest='target', required=True, help='The target assembly in FASTA format.')
group.add_argument('-s', action='store', dest='save_file', required=False, default=False, help='Write a list with the contig sizesi. (default : %(default)s)')
group.add_argument('-l', action='store', dest='min_length', required=False, default=0, help='Minimum contig length to include a contig. (default : %(default)s)')
args = parser.parse_args()
genomeFile = args.target
minContigSize = args.min_length

#==============1.3 Define functions================
def get_genome_size(genomeFile, minContigSize):
        genomeSize = 0
        with open(genomeFile) as fastaFile:
                for fastaParse in SeqIO.parse(fastaFile,"fasta"):
                        ID = fastaParse.id
                        seq = fastaParse.seq
			if len(seq) >= minContigSize:
				genomeSize = genomeSize+len(seq)
        return(genomeSize)

def get_mean_sequence_length(genomeFile, minContigSize):
	contigLen = []
	with open(genomeFile) as fastaFile:
                for fastaParse in SeqIO.parse(fastaFile,"fasta"):
                        ID = fastaParse.id
			seq = fastaParse.seq
			if len(seq) >= minContigSize:
				contigLen.append(len(seq))
	meanLength = np.mean(np.array(contigLen))	
        return(meanLength)

def get_contigs_number(genomeFile, minContigSize):
	numContigs = 0
	with open(genomeFile) as fastaFile:
		for fastaParse in SeqIO.parse(fastaFile,"fasta"):
			ID = fastaParse.id
			seq = fastaParse.seq
			if len(seq) >= minContigSize:
				numContigs += 1
	return(numContigs)

def write_contigs_size(genomeFile,outName, minContigSize):
	outFile = open(outName,'w')
	with open(genomeFile) as fastaFile:
		for fastaParse in SeqIO.parse(fastaFile,"fasta"):
			seq = fastaParse.seq
			contigLen = len(seq)
			if contigLen >= minContigSize:
				outFile.write(str(contigLen)+'\n')
	outFile.close()

'''2.0 Calculate genome size'''
if __name__ == "__main__":
	if args.save_file:
		meanLength = get_mean_sequence_length(genomeFile,int(minContigSize))
		genomeSize = get_genome_size(genomeFile,int(minContigSize))
		numContigs = get_contigs_number(genomeFile,int(minContigSize))
		print 'meanLength\tgenomeSize\tnumContigs'
		print '{}\t{}\t{}'.format(str(meanLength),str(genomeSize),str(numContigs))
		outFile = 'contig_lengths.txt'
		write_contigs_size(genomeFile,outFile,int(minContigSize))
	else :
		meanLength = get_mean_sequence_length(genomeFile,int(minContigSize))
		genomeSize = get_genome_size(genomeFile,int(minContigSize))
		numContigs = get_contigs_number(genomeFile,int(minContigSize))
		print 'meanLength\tgenomeSize\tnumContigs'
		print '{}\t{}\t{}'.format(str(meanLength),str(genomeSize),str(numContigs))




