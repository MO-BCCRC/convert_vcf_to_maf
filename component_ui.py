'''
Created on July 8, 2014

@author: Karen Eddy
@last_modified: 25 Jun 2015 by jrosner

'''

import argparse

parser = argparse.ArgumentParser(prog='CreateAnnotatedMaf', description='converts vcf to maf')
parser.add_argument('-i', '--infile', required=True,
                    help='path to a single VCF')
parser.add_argument('-o', '--outfile', required=True,
                    help='path to the output annotated MAF file.')
parser.add_argument('-t', '--tumor_id', required=False,
                    help='tumor id')
parser.add_argument('-n', '--normal_id', required=False,
                    help='normal id')

args, unknown = parser.parse_known_args()
