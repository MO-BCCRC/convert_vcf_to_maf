'''
convert_vcf_to_maf.py

@author: keddy
@last_modified: 24 Jun 2015 by jrosner
'''

import os
import argparse
import subprocess

__version__ = '1.1.0'

def get_args():
    ''' return cmd line args '''

    parser = argparse.ArgumentParser(prog='convert_vcf_to_maf', description='converts vcf to maf')
    parser.add_argument('-i', '--infile', required=True,
                        help='path to a single VCF')
    parser.add_argument('-o', '--outfile', required=True,
                        help='path to the output annotated MAF file.')
    parser.add_argument('-t', '--tumor_id', required=True,
                        help='tumor id')
    parser.add_argument('-n', '--normal_id', required=True,
                        help='normal id')
    parser.add_argument('--java_exe', required=True,
                        help='path to java executable')
    args, _ = parser.parse_known_args()
    return args


def convert_vcf_to_maf(vcf, output_maf, cwd, java_exe, tid, nid):
    ''' Creates a MAF file '''

    snpeff_cmd = ['{} -Xmx10g'.format(java_exe),
                  '-jar {}/vcf2maf/snpEff/snpEff.jar eff '.format(cwd),
                  '-cancer -lof -hgvs',
                  '-config {}/vcf2maf/snpEff/snpEff.config'.format(cwd),
                  '-noStats GRCh37.74']

    # Run the script to create the MAF.
    print 'Running vcf2maf on file: ' + vcf
    cmd = ('perl {}/vcf2maf/vcf2maf-master/vcf2maf_museq.pl'
          ' --input-vcf {} '
          ' --output-maf {} '
          ' --tumor-id {}'
          ' --normal-id {}'
          ' --snpeff-cmd \'{}\'').format(cwd, vcf, output_maf, tid, nid, ' '.join(snpeff_cmd))

    print 'Running command: ' + cmd
    subprocess.call(cmd, shell=True)

    # add_sample_id(output_maf, tid, nid)

    print 'vcf2maf complete! Created file: ' + output_maf

    try:
        os.remove(vcf.replace('.vcf','.anno.vcf'))
    except OSError:
        pass


def add_amino_acid_column(infile, outfile):
    '''
    convert 3-letter amino acid change code to 1-letter code
    representation and put in a new column
    '''
    code_converter  = {'Ala':'A','Asx':'B','Cys':'C','Asp':'D','Glu':'E','Phe':'F','Gly':'G',
                       'His':'H','Ile':'I','Lys':'K','Leu':'L','Met':'M','Asn':'N','Pro':'P',
                       'Gln':'Q','Arg':'R','Ser':'S','Thr':'T','Val':'V','Trp':'W','Tyr':'Y',
                       'Glx':'Z'}

    with open(infile,'r') as f, open(outfile, 'w') as o:
        for line in f:
            line = line.rstrip().split('\t')

            # header -- get protein change col# and add new column
            if isinstance(line[0], str) and line[0].startswith('Hugo_'):
                try:
                    pc_index = line.index('Protein_Change')
                except:
                    raise Exception('Are you sure this is a .maf file? '
                                    ' Missing \'Protein_Change\' column')

                prot_chng = 'Amino_Acid_Change'

            else:
                prot_chng = line[pc_index]
                prot_chng = prot_chng[2:prot_chng.find('/')]

                for k,v in code_converter.iteritems():
                    prot_chng = prot_chng.replace(k,v)

            line.append(prot_chng)
            o.write('\t'.join(line) + '\n')


def main():
    ''' main function '''
    args = get_args()
    cwd  = os.path.dirname(os.path.realpath(__file__))
    tmp  = args.infile + '.maf.tmp'

    convert_vcf_to_maf(args.infile, tmp, cwd, args.java_exe, args.tumor_id, args.normal_id)
    add_amino_acid_column(tmp, args.outfile)

if __name__ == '__main__':
    main()
