import os.path
import json
import os

if os.path.isfile('./conf/conf.json') is False:
    with open('./conf/conf.json', 'w') as newconf:
        conf = json.load(newconf)
        conf['dbpassword']  = os.environ['DB_PASSWORD']
        conf['log']  = os.environ['LOG_LVL']
        conf['virustotal'] = '58135bf629cb53d9b7facdf730147025d04a0d12520d83900021ed3f944bb402'
        json.dump(conf, newconf, indent=4)

with open('./conf/conf.json', 'r') as mainconf:
    conf = json.load(mainconf)