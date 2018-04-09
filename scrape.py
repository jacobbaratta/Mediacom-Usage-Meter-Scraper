import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
import re
import json

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"), chrome_options=chrome_options)

with open('config.json') as json_config_file:
	config = json.load(json_config_file)

driver.get("http://mediacomtoday.com/usagemeter/index.php")

timeout = 5
try:
	element_present = EC.presence_of_element_located((By.ID, 'username'))
	WebDriverWait(driver, timeout).until(element_present)
except TimeoutException:
	print("Timed out waiting for page to load")

user_field = driver.find_element_by_id("username")
#user_field.clear()
user_field.send_keys(config["username"])

password_field = driver.find_element_by_id("password")
#password_field.clear()
password_field.send_keys(config["password"])

login_button = driver.find_element_by_css_selector("a.ping-button.normal.allow.loginSubmit")
login_button.click()

timeout = 5
try:
	element_present = EC.presence_of_element_located((By.ID, 'body_cols'))
	WebDriverWait(driver, timeout).until(element_present)
except TimeoutException:
	print("Timed out waiting for page to load")

time.sleep(1) # wait for JS to load

driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
# driver.find_element_by_css_selector(#body_cols > iframe)

# Alternatives/other:
# Contains span with Internet 200, then crap text, but contains package specs (DL/UL/bandwidth): #bodyInc > table > tbody > tr:nth-child(4) > td:nth-child(2) > table:nth-child(2) > tbody > tr > td:nth-child(1) > table > tbody > tr:nth-child(2) > td
# Current internet usage: #bodyInc > table > tbody > tr:nth-child(4) > td:nth-child(2) > table:nth-child(2) > tbody > tr > td:nth-child(1) > table > tbody > tr:nth-child(3) > td > b
# Data usage text (includes the measurement date): #bodyInc > table > tbody > tr:nth-child(4) > td:nth-child(2) > table:nth-child(2) > tbody > tr > td:nth-child(3) > table > tbody > tr:nth-child(10) > td:nth-child(2) > span

data_period_raw = driver.find_element_by_css_selector("#highcharts-0 > svg > text.highcharts-title > tspan").text
#print("data_period_raw: "+data_period_raw)

data_percent_used_raw = driver.find_element_by_css_selector("#bodyInc > table > tbody > tr:nth-child(4) > td:nth-child(2) > table:nth-child(2) > tbody > tr > td:nth-child(3) > table > tbody > tr:nth-child(5) > td:nth-child(2) > span.subTitleRed").text
#print("data_percent_used_raw: "+data_percent_used_raw)

data_percent_left_raw = driver.find_element_by_css_selector("#bodyInc > table > tbody > tr:nth-child(4) > td:nth-child(2) > table:nth-child(2) > tbody > tr > td:nth-child(3) > table > tbody > tr:nth-child(5) > td:nth-child(2) > span:nth-child(2)").text
#print("data_percent_left_raw: "+data_percent_left_raw)

days_remaining_raw = driver.find_element_by_css_selector("#bodyInc > table > tbody > tr:nth-child(4) > td:nth-child(2) > table:nth-child(2) > tbody > tr > td:nth-child(3) > table > tbody > tr:nth-child(5) > td:nth-child(2) > span:nth-child(3)").text
#print("days_remaining_raw: "+days_remaining_raw)

data_used_of_total_raw = driver.find_element_by_css_selector("#bodyInc > table > tbody > tr:nth-child(4) > td:nth-child(2) > table:nth-child(2) > tbody > tr > td:nth-child(3) > table > tbody > tr:nth-child(6) > td.subTitleGrey").text
#print("data_used_of_total_raw: "+data_used_of_total_raw)

data_usage_text_raw = driver.find_element_by_css_selector("#bodyInc > table > tbody > tr:nth-child(4) > td:nth-child(2) > table:nth-child(2) > tbody > tr > td:nth-child(3) > table > tbody > tr:nth-child(10) > td:nth-child(2) > span").text
#print("data_usage_text_raw: "+data_usage_text_raw)


# thename = re.search("([a-zA-Z0-9_]*)\s*\=", str(x)).group(1)

#Note Due to the limitation of the current implementation the character following an empty match is not included in a next match, so findall(r'^|\w+', 'two words') returns ['', 'wo', 'words'] (note missed “t”). This is changed in Python 3.7.
#https://docs.python.org/3.6/library/re.html
#https://docs.python.org/2.2/lib/match-objects.html

days_remaining = re.search("([0-9]+ days)", str(days_remaining_raw)).group(1)
data_used_gb = re.search("([0-9]+\.?[0-9]* GB)", str(data_used_of_total_raw)).group(1)
data_used = re.search("([0-9]+\.?[0-9]*)", str(data_used_gb)).group(1)
data_left_gb = re.findall("([0-9]+\.?[0-9]* GB)", str(data_used_of_total_raw))[1]
data_left = re.search("([0-9]+\.?[0-9]*)", str(data_left_gb)).group(1)
data_current_as_of = re.search("as of ([0-9]+\/[0-9]+\/[0-9]+ [0-9]+:[0-9]+)\.", str(data_usage_text_raw)).group(1)

print("---------------------------------------------------------------------------")
print("Usage period: "+data_period_raw+" ("+days_remaining+" remaining)")
#print("Days remaining in usage period: "+days_remaining)
#print("Usage (%): "+data_percent_used_raw+" / "+data_percent_left_raw)
#print("Usage (GB): "+data_used_gb+" / "+data_left_gb)
n1 = float(data_used)
n2 = float(data_left)
percent = (n1 / n2)
print("[%-25s] %0.1f/%0.0f GB (%s / %s)" % ('='*int(25*percent), n1, n2, data_percent_used_raw, data_percent_left_raw))
#print("[%-25s] %0.1f/%0.0f GB (%d%%)" % ('='*int(25*percent), n1, n2, 100*percent))
print("Current as of "+data_current_as_of)
print("---------------------------------------------------------------------------")

driver.close()
