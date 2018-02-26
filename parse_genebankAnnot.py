#!/usr/bin/env python
'''
@name: parse_genebankAnnot.py
@author: Juan C. Castro <jccastrog at gatech dot edu>
@update: 15-Jan-2018
@version: 1.0.4
@license: GNU General Public License v3.0.
please type "./fitModel.py -h" for usage help
'''

###===== 1.0 Load packages, define functions, initialize variables =====###
# 1.1 Load packages ======================================================#
import sys, os
import argparse
import re
# 1.2. Define functions ==================================================#
def parse_genebank(genebank_file):
	with open(genebank_file) as file:
		lines = file.readlines()
		for line in lines:
			line = line.rstrip('\n')
			if line.startswith('LOCUS'):
				locus = line.split()
				strain_gene = locus[1].split('|')
				strain = strain_gene[0]
				gene = strain_gene[1]
			elif len(re.findall('"\w+.CDS.\w+"',line)) > 0:
				kbase_id = re.findall('"\w+.CDS.\w+"',line)[0]
				kbase_id = kbase_id.replace('"','')
				out = '{}\t{}\t{}\n'.format(strain, gene, kbase_id)
				sys.stdout.write(out)
# 1.3 Initialize variables ===============================================#
parser = argparse.ArgumentParser(description="parse_genebankAnnot.py: Estimation of bacterial genomes in biological samples [jccastrog@gatech.edu]")
group = parser.add_argument_group('Required arguments') #Required
group.add_argument('-g', action='store', dest='genebank_file', required=True, default='', help='GeneBank file to parse.')
args = parser.parse_args()

###========================= 2.0 Parse the file ========================###
parse_genebank(args.genebank_file)
#==========================================================================#
