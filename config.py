# encoding:utf-8
import json
import logging
import os
import pickle
from log import logger

# 将所有可用的配置项写在字典里, 请使用小写字母
# 此处的配置值无实际意义，程序不会读取此处的配置，仅用于提示格式，请将配置加入到config.json中

available_setting = {
    # 输入的txt数据文件夹
    "input_dir":"", 
    # 输出的.list文件的名称
    "output_file":"",
    "valid_file":"",
    "train_file":"",
    # “我”的名字
    "my_name":"我",
    # 角色的名字，比如”陆沉“
    "char_name":"",
    # 系统prompt
    "system_prompt":"",
    # 中间的输出文件夹名称
    "output_dir_1":"",
    "output_dir_2":"",
    "debug":False,
}

class Config(dict):
    def __init__(self, d=None):
        super().__init__()
        if d is None:
            d = {}
        for k, v in d.items():
            self[k] = v

    def __getitem__(self, key):
        print(f"KEY:{key}")
        if key not in available_setting:
            raise Exception("key {} not in available_setting".format(key))
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        if key not in available_setting:
            raise Exception("key {} not in available_setting".format(key))
        return super().__setitem__(key, value)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError as e:
            return default
        except Exception as e:
            raise e

config = Config()


def load_config():
    global config
    config_path = "./config.json"
    if not os.path.exists(config_path):
        logger.info("配置文件不存在，将使用config-template.json模板")
        config_path = "./config-template.json"

    config_str = read_file(config_path)
    logger.debug("[INIT] config str: {}".format(config_str))

    # 将json字符串反序列化为dict类型
    config = Config(json.loads(config_str))

    # override config with environment variables.
    # Some online deployment platforms (e.g. Railway) deploy project from github directly. So you shouldn't put your secrets like api key in a config file, instead use environment variables to override the default config.
    for name, value in os.environ.items():
        name = name.lower()
        if name in available_setting:
            logger.info("[INIT] override config by environ args: {}={}".format(name, value))
            try:
                config[name] = eval(value)
            except:
                if value == "false":
                    config[name] = False
                elif value == "true":
                    config[name] = True
                else:
                    config[name] = value

    if config.get("debug", False):
        logger.setLevel(logging.DEBUG)
        logger.debug("[INIT] set log level to DEBUG")

    logger.info("[INIT] load config: {}".format(config))

def get_root():
    return os.path.dirname(os.path.abspath(__file__))

def read_file(path):
    with open(path, mode="r", encoding="utf-8") as f:
        return f.read()

def conf():
    return config