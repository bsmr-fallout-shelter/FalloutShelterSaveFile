import os
import base64
import re
import json

from pbkdf2 import PBKDF2
from Crypto.Cipher import AES

class SaveFile(object):
    
    main_key = b'tu89geji340t89u2'

    def __init__(self, filename):
        self.filename = filename
        self.rawdata = None
        self.pwd = (base64.b64encode('PlayerData'.encode('utf-8')))[:8]
        
        if not os.path.exists(self.filename):
            raise ValueError('File does not exist')
        
    def load(self):
        with open(self.filename, 'rb') as f:
            self.rawdata = f.read()
        self.key = PBKDF2(self.pwd, self.main_key).read(32)
        aes = AES.new(self.key, AES.MODE_CBC, self.main_key)
        data = base64.b64decode(self.rawdata)
        self.decrypted = str(aes.decrypt(data), 'utf-8')
    
    def set_resources(self, caps, food, energy, water, stim, rad):
        m = re.search("""],"storage":{"resources":{"Nuka":([0-9.]+),"Food":([0-9.]+),"Energy":([0-9.]+),"Water":([0-9.]+),"StimPack":([0-9.]+),"RadAway":([0-9.]+)""", self.decrypted)
        print('Original resources: Nuka {}, Food {}, Energy {}, Water {}, Stim {}, Rad {}'.format(m.group(1), m.group(2), m.group(3), m.group(4), m.group(5), m.group(6)))
        new_string = """],"storage":{{"resources":{{"Nuka":{},"Food":{},"Energy":{},"Water":{},"StimPack":{},"RadAway":{}""".format(caps, food, energy, water, stim, rad)
        self.decrypted = self.decrypted[0:m.start()] + new_string + self.decrypted[m.end():]
    
    def save(self):
        with open(self.filename + '.new', 'wb') as f:
            aes = AES.new(self.key, AES.MODE_CBC, self.main_key)
            data = self.decrypted.encode('utf-8')
            if len(data) % 16 != 0:
                data += (16 - (len(data) % 16)) * b'\t'
            data = aes.encrypt(data)
            data = base64.b64encode(data)
            f.write(data)
            