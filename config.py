from configparser import ConfigParser


class Config:
    token: str

    def __init__(self):
        config = ConfigParser()
        result = config.read("config.ini")
        if len(result) == 0:
            raise Exception("Config File NotFound or Cannot Read Config File!!")
        try:
            self.token = config['bot']['token']
            self.sudo = int(config['settings']['sudo'])
        except KeyError as e:
            raise Exception(f"Keys not found in config file => {' '.join(e.args)}")

