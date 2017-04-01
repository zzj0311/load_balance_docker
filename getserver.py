import requests
import os
import argparse
import logging
import re
import time

parser = argparse.ArgumentParser()
parser.add_argument("--api-key",dest = "key", help="provide api key", default="")
parser.add_argument("--api-pass",dest = "password", help="provide api pass", default="")
parser.add_argument("--container-id",dest = "container", help="provide container id", default="")
parser.add_argument("--interval",dest = "interval", help="provide request interval", type = int, default=300)
args = parser.parse_args()
file_name = "/root/.netrc"
f = open(file_name, "w+")
f.write('''
	machine app.arukas.io
	login {0}
	password {1}
'''.format(args.key, args.password))
f.close()
ip = ""
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d]%(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename="/opt/nginx/logs/getserver.log",
                    filemode='w+')

while True:
	old_ip = ip
	url = "https://app.arukas.io/api/containers/"
	url = url + args.container
	response = requests.get(url).json()
	host = str(response['data']['attributes']['port_mappings'][0][0]['host'])
	ip_list = re.split(r'[-.]',host)
	ip_list = ip_list[1:5]
	str_ip = ''
	for i_p in ip_list:
		str_ip = str_ip + i_p + '.'
	str_ip = str_ip[0:-1]
	port = str(response['data']['attributes']['port_mappings'][0][0]['service_port'])
	ip = str_ip + ":" + port
	logging.debug('current ip is: %s', ip)
	if old_ip != ip:
		logging.debug('updating configure & reloading nginx')
		file_name = "/opt/nginx/conf/sakura.conf"
		f = open(file_name,"w+")
		f.write('''
			server{{
				listen 11223;
				proxy_pass {0};
			}}
			server{{
				listen 11223 udp;
				proxy_pass {1};
			}}
		'''.format(ip,ip))
		f.close()
		os.system("kill -s HUP `cat /opt/nginx/logs/nginx.pid`")
	time.sleep(args.interval)
