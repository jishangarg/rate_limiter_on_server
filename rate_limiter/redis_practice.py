#from flask import request
from time import sleep
import redis
#print(request.remote_addr)
def func(client3):
   print(client3.get('language'))

client=redis.Redis(host='localhost',port=6379)

client.set('language','python')
print(client.get('language'))

client.set('language','python',px=10000)
print(client.get('language'))
print(client.ttl('language'))


client2=redis.Redis(host='localhost',port=6379)
client3=redis.Redis(host='localhost',port=6379)
client2=client
#sleep(4)
print(client2.get('language'))
print(client.get('language'))




AllKeys=client2.keys()
for key in AllKeys:
	client2.delete(key)
client3.set('me','hello')
client2=client3
print(client2.get('me'))
print(client2.get('language'))

