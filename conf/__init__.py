import os
import configparser
import logging
import logging.config
from collections import namedtuple


BATH_PATH = os.path.dirname(os.path.realpath(__file__))

# 项目基本配置路径
conf_file = os.path.join(BATH_PATH, "config.conf")

log_dir = os.path.join(os.getcwd(), "logs")
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
# 日志配置路径
logging_conf_file = os.path.join(BATH_PATH, "logging.cfg")
logging.config.fileConfig(logging_conf_file)

class GlobalConf():
    def __init__(self, file):
        cp = configparser.RawConfigParser()
        cp.read(file, encoding="utf-8")
        self.cp = cp
        self.dict = {}
        for key, value in self.cp.items():
            if isinstance(value, configparser.SectionProxy):
                self.dict[key] = {}
                for k, v in value.items():
                    self.dict[key][k] = int(v) if isinstance(v, str) and v.isdigit() else v
                setattr(self, key, namedtuple('ConfSection', self.dict[key].keys())(**self.dict[key]))
            else:
                self.dict[key] = value
                setattr(self, key, value)


cnf = GlobalConf(conf_file)
cnf_map = cnf.dict
