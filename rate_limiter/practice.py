from flask import Flask,request,abort
import redis
from flask_cors import CORS
app=Flask(__name__)
CORS(app)
def DecodeHashvalue(HashValue):
	encoding = 'utf-8'
	HashValue=str(HashValue, encoding)
	HashValue=int(HashValue)
	HashValue=HashValue-1
	return HashValue
# def rate_limiter(Thersold,count,RouteName):

# 	global RateClient
# 	AllKeys=RateClient.keys()
# 	for key in AllKeys:
# 	   RateClient.delete(key)
# 	if RouteName=="developers":
# 		print("developers")   
# 		RateClient=DevClient
# 	elif RouteName=="organisations":
# 		print("organisations")
# 		RateClient=OrgClient    
# 	global time
# 	ip=request.remote_addr
# 	print("rate client ip",DevClient.get(ip))	
# 	if RateClient.exists(ip)==False:
# 	   RateClient.set(str(ip),1,ex=time)
# 	   DevRouteSucc=True
# 	   print("milli ",RateClient.get(ip))
# 	else:
# 		print(RateClient.get(ip))
# 		RateClient.incr(ip)
# 		HashValue=RateClient.get(ip)
# 		encoding = 'utf-8'
# 		HashValue=str(HashValue, encoding)
# 		HashValue=int(HashValue)
# 		HashValue=HashValue-1
# 		print(HashValue)
# 		if HashValue>int(Thersold):
# 			DevRouteSucc=False
# 		else:
# 			DevRouteSucc=True
# 	Dict={"RedisClient":RateClient,"Success":DevRouteSucc,"Count":RateClient.get(ip)} 
# 	return Dict     
global time,DevCount,OrgCount,DevClient,OrgClient
time=10
DevCount=OrgCount=0
global count
count=0
DevClient=redis.Redis(host='localhost',port=6379)
DefaultRouteRate=10
OrgClient=redis.Redis(host='localhost',port=6379)
@app.route("/developers",methods=["POST"])
def developers():
	message=request.get_json(force=True)
	global DevCount,DevClient,DefaultRouteRate,count
	ip=request.remote_addr
	IpHash=ip+str("developers")
	print("developers")
	ThRoute1=message['ThRoute1']
	if not ThRoute1.strip():
		ThRoute1=DefaultRouteRate
	print(ThRoute1)

	if DevClient.exists(IpHash)==False:
	   DevClient.set(str(IpHash),1,ex=time)
	   count=1
	else:
		print(DevClient.get(IpHash))
		DevClient.incr(IpHash)
		HashValue=DevClient.get(IpHash)
		HashValue=DecodeHashvalue(HashValue)
		print(HashValue)
		if HashValue>=int(ThRoute1):
			 print("entered here")
			 abort(401)
		count=HashValue+1	   
	return str(count)+"Successful Ping"

@app.route("/organisations",methods=["POST"])
def organisations():
	message=request.get_json(force=True)
	global OrgCount,OrgClient,DefaultRouteRate,count
	print("organisations")
	ThRoute2=message['ThRoute2']
	ip=request.remote_addr
	IpHash=ip+str("organisations")
	if not ThRoute2.strip():
		ThRoute2=DefaultRouteRate
	if OrgClient.exists(IpHash)==False:
	   OrgClient.set(str(IpHash),1,ex=time)
	   count=1
	else:
		print(OrgClient.get(IpHash))
		OrgClient.incr(IpHash)
		HashValue=DevClient.get(IpHash)
		HashValue=DecodeHashvalue(HashValue)
		print(HashValue)
		if HashValue>=int(ThRoute2):
			 print("entered here")
			 abort(401)
		count=HashValue+1	   
	return str(count)+"Successful Ping"
	
if __name__=="__main__":
	app.run(debug=True)