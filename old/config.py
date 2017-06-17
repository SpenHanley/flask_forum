import os
import configparser


class Config:
    def __init__(self, conf_dir="config", file_name="config.ini"):
        self.config_directory = conf_dir
        self.config = configparser.ConfigParser()
        self.config_file = os.path.join(conf_dir, file_name)
        self.create_config()
        self.failed = False
        self.config.read(self.config_file)

    def create_config(self):
        try:
            if not os.path.isdir(self.config_directory):
                os.mkdir(self.config_directory)
            if not os.path.isfile(self.config_file):
                cfg = open(self.config_file, 'w')
                # MongoDB Configuration
                self.config.add_section('mongo_db')
                self.config.set('mongo_db', 'host', 'localhost')
                self.config.set('mongo_db', 'port', 27017)
                # self.config.set('mongo_db', 'pass', '')
                self.config.set('mongo_db', 'db_name', 'forum')
                # User Domain Configuration
                self.config.add_section('ui_ctl')
                self.config.set('ui_ctl', 'AllowAnonymous', 'yes')
                self.config.write(cfg)
                cfg.close()
            else:
                return
        except:
            print('Somethings broken here')

