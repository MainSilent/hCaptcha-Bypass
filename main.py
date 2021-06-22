import os
import time
from seleniumwire.undetected_chromedriver import Chrome

def interceptor(request):
	if "https://hcaptcha.com/checksiteconfig" in request.url:
		request.url = "https://hcaptcha.com/checksiteconfig?host=discord.com&sitekey=f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34&sc=1&swa=1"
	elif "https://hcaptcha.com/getcaptcha" in request.url:
		modify = request.body.decode('utf-8').split("&")
		modify[2] = "host=discord.com" 
		request.body = bytes("&".join(modify), 'utf-8')
		del request.headers['Content-Length']
		request.headers['Content-Length'] = str(len(request.body))

driver = Chrome(executable_path="./chromedriver")
driver.request_interceptor = interceptor
driver.get(f'file://{os.getcwd()}/hcaptcha.html')
time.sleep(120)