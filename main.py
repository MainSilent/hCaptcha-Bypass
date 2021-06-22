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

def request_interceptor(request):
	if "https://hcaptcha.com/checksiteconfig" in request.url:
		request.url = f"https://hcaptcha.com/checksiteconfig?host={host}&sitekey=f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34&sc=1&swa=1"
	elif "https://hcaptcha.com/getcaptcha" in request.url:
		modify = request.body.decode('utf-8').split("&")
		modify[2] = f"host={host}" 
		request.body = bytes("&".join(modify), 'utf-8')
		del request.headers['Content-Length']
		request.headers['Content-Length'] = str(len(request.body))
		request.headers['Cookie'] = "hc_accessibility=6DbBcYzJctOhoJkeXwAfR2y1qDU6NGV/I00UnfexnHQ2M53KVqq91ftjh1pD2U2HkXHcLcjdR1Mv6qYSgLnAXq3cD4ciLqYGeb2/vzf0pYB8duUXdIBKwbqbMPCP+E4haX0Nk8BGiByBjOke3YDgS3inacc+s1kqrPb7BOpNf5X3DyUEwF7r2c0MTcAjvbFAJwQ+9rGPDFsmZ0ah3Hi4qeCjAaeFjfyZ79xXe83RHQ1AI79MpPfHMNhA/DXXobvNz6fFOekIoXaCUIvz3VpDeKuR/BfqVvb4j9XNYT0tMhTnWyCB5pdAz9LtPptw3Et9bGWLGWdpgq8+IizovIBum98XA1e5wqbsM2z3A+yq1XhEwp6qglJvimn4U2W2HZHy07OcbSGSmFi5cKsJKRqVyFS+KeVzrhmvZj86YRSotfN1jLD/7Zh9namqLSH8FfWJUFdIxg7LJMZ18IHyhta2Ynsxctg31HQ+psJmZZn+6U8B8kVEPnLEVdjyXWydunSE16Fps4+14vKFes1H"

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