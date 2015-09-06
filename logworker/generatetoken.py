# -*- coding: utf-8 -*-
__author__ = 'fanzhanao'

import sys,redis,base64,hashlib,random

def generateToken():
	"""
	生成token
	:return: string
	"""
	return base64.b64encode(hashlib.sha256( str(random.getrandbits(256)) ).digest(), random.choice(['rA','aZ','gQ','hH','hG','aR','DD'])).rstrip('==')

if __name__ == "__main__":
	rds = redis.Redis(host='127.0.0.1',port=6379,db=0)
	token = generateToken()
	v = None
	if len(sys.argv) == 2:
		v = sys.argv[1]
	else:
		v = "some app"

	rds.hset('appKeys',token,v)
	print(token)
