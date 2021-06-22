import os
import time
import json
import gzip
from selenium.webdriver.chrome.options import Options
from seleniumwire.undetected_chromedriver import Chrome

# Note: You should also change the site key in html file
host = "discord.com"
options = Options()
options.add_argument("--headless")
driver = Chrome(executable_path="./chromedriver", options=options)

def get_token():
	with open("h_captcha.json", "r") as f:
		cookies = json.load(f)
	for cookie in cookies:
		if cookie["name"] == "hc_accessibility":
			if int(cookie["expiry"]) < time.time():
				print("Cookie has expired") 
			return cookie["value"]

def request_interceptor(request):
	if "https://hcaptcha.com/checksiteconfig" in request.url:
		request.url = f"https://hcaptcha.com/checksiteconfig?host={host}&sitekey=f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34&sc=1&swa=1"
	elif "https://hcaptcha.com/getcaptcha" in request.url:
		modify = request.body.decode('utf-8').split("&")
		modify[2] = f"host={host}" 
		request.body = bytes("&".join(modify), 'utf-8')
		del request.headers['Content-Length']
		request.headers['Content-Length'] = str(len(request.body))
		request.headers['Cookie'] = f"hc_accessibility={get_token()}"

def response_interceptor(request, response):
	if "https://hcaptcha.com/getcaptcha" in request.url:
		body = gzip.decompress(response.body).decode('utf-8')
		data = json.loads(body)
		try:
			if data["bypass-message"]:
				print("Failed")
		except:
			print(data['generated_pass_UUID'])
		driver.close()

driver.request_interceptor = request_interceptor
driver.response_interceptor = response_interceptor
driver.get(f'file://{os.getcwd()}/hcaptcha.html')

while True:
	try:
		driver.switch_to.frame(0)
		driver.find_element_by_id("checkbox").click()
		break
	except Exception as e:
		#print(e)
		driver.switch_to.default_content()
		time.sleep(0.2)

time.sleep(60)