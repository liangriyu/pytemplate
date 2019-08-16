import yaml
import argparse
import sys
import os

_base_dir = os.path.abspath(os.path.dirname(__file__))
_configs = yaml.load(open(_base_dir+"config.yaml",'r'),Loader=yaml.FullLoader)


def get(key):
    keys = str(key).split(".")
    l = len(keys)
    if l == 1:
        return _configs[key]
    else:
        p = 0
        dict = _configs[keys[0]]
        for k in keys:
            if p == l - 1:
                return dict[k]
            if p == 0:
                dict = _configs[k]
            else:
                dict = dict[k]
            p = p + 1
    return dict[key]

def register():
    args = sys.argv[1:]
    if args:
        for arg in args:
            if str(arg).startswith('-') and args != '-':
                i = arg.index('=')
                opt, optarg = arg[1:i], arg[i + 1:]
                if not optarg:
                    raise Exception(('option -%s requires argument') % opt)
                print(opt,optarg)
                conf = _Config()

class _Config(object):

    def __init__(self):
        file_path="config.yaml"
        self._configs=yaml.load(open(file_path,'r'),Loader=yaml.FullLoader)


    def test(self):
        parser = argparse.ArgumentParser()
        args = parser.parse_args()
        print(vars(args))

if __name__ == '__main__':
    conf = Config()
    v = conf.get("datasource.password")
    print(v)


    parser = argparse.ArgumentParser()
    parser.add_argument('--gpus', type=str, default=None)
    parser.add_argument('--batch-size', type=int, default=32)
    args = parser.parse_args()
    print(vars(args))