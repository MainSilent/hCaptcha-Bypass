import undetected_chromedriver as uc
uc.install()

import os
import time
import json
from selenium import webdriver
from dotenv import load_dotenv; load_dotenv()

def get_cookie():
	print("Waiting for hcaptcha cookie...")
	driver = webdriver.Chrome()
	driver.get("https://accounts.hcaptcha.com/verify_email/"+os.getenv("hcaptcha"))
	while True:
		if "Set Cookie" in driver.find_element_by_xpath("/html/body").text:
			break
		time.sleep(0.4)
	time.sleep(2)
	driver.find_element_by_xpath('//*[@id="root"]/div/div[3]/div/div[3]/button').click()

	while True:
		try:
			# for now i need to open the link in another tab and set the coockie manual
			driver.switch_to.window(driver.window_handles[1])
			res = driver.find_element_by_xpath('//*[@id="root"]/div/div[3]/div/div[3]/span').text
			if "Cookie set" in res:
				with open("h_captcha.json", "w") as f:
				    f.write(json.dumps(driver.get_cookies()))
				print("\033[32m"+"Success"+"\033[0m")
				break 
			else:
				print("\033[31m"+"Failed"+"\033[0m"+", "+res)
				break
		except:
			time.sleep(0.4)

get_cookie()