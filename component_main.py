'''
Created on July 10, 2014

@author: Karen Eddy
@last_modified: 24 Jun 2015 by jrosner

'''

from kronos.utils import ComponentAbstract
import os


class Component(ComponentAbstract):

    def __init__(self, component_name='convert_vcf_to_maf',
                 component_parent_dir=None, seed_dir=None):

        self.version = '1.1.0'

        # Initialize ComponentAbstract
        super(Component, self).__init__(component_name, component_parent_dir, seed_dir)

    def make_cmd(self, chunk = None):
        path = os.path.join(self.seed_dir, 'convert_vcf_to_maf.py')

        cmd = [self.requirements['python'], path]
        cmd_args = []
        for k,v in vars(self.args).iteritems():
            if v is not None:
                cmd_args.append('--' + k)
                cmd_args.append(v)

        if chunk:
            cmd_args.extend(['--infile', chunk])

        cmd = ' '.join(cmd + cmd_args)
        cmd += '\nrm -fv {}.maf.tmp'.format(self.args.infile)
        cmd_args = []

        return cmd, cmd_args

    def test(self):
        # import component_test
        # component_test.run()
        pass

def _main():
    comp = Component()
    comp.args = component_ui.args
    comp.run()
    comp.test()

if __name__ == '__main__':
    import component_ui
    _main()
