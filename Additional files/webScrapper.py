import selenium as se
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

links = open('links_attributes.txt','a')


browser = webdriver.Chrome(executable_path='chromedriver.exe')

website_URL = 'https://public.msrtcors.com/users/guest_user_wel.php'

email = 'mayank30@somaiya.edu'
cemail = 'mayank30@somaiya.edu'
phno = '9029772254'
browser.get(website_URL)

time.sleep(2)

#email 

stops = ['MUMBAI','PUNE','RATNAGIRI','AKOLA','NASIK','NAGPUR','AHMEDNAGAR','AMRAVATI','KOLHAPUR','JALGAON']

tp = browser.find_element_by_xpath("//h1[contains(text(), 'Maharashtra State Road Transport Corporation')]")
print(tp.text)

browser.switch_to.frame('frmMain1')

a = browser.find_element_by_id("email")
a.send_keys(email)

b = browser.find_element_by_xpath("//input[@id = 'conemail']")
b.send_keys(cemail)

c = browser.find_element_by_xpath("//input[@id = 'mobno']")
c.send_keys(phno)

browser.find_element_by_xpath("//input[@id = 'btnSubmit']").click()

time.sleep(2)


browser.switch_to.frame('frmMain1')

d = browser.find_element_by_xpath("//input[@id = 'fromstop']")

e = browser.find_element_by_xpath("//input[@id = 'tostop']")

f = browser.find_element_by_xpath("//input[@id = 'onjrdt']")

g = browser.find_element_by_xpath("//input[@value = 'Search']")

h = browser.find_element_by_xpath("//input[@value = 'Reset']")



for city_from in stops :
	for city_to in stops :
		if city_from == city_to : continue

		links.write(city_from + "TO" + city_to + '\n')
		
		browser.switch_to.default_content()
		browser.switch_to.frame('frmMain1')

		h.click()

		d.send_keys(Keys.ENTER)
		d.send_keys(city_from)
		time.sleep(1)
		d.send_keys(Keys.ENTER)

		e.send_keys(Keys.ENTER)
		e.send_keys(city_to)
		time.sleep(1)
		e.send_keys(Keys.ENTER)

		f.send_keys(Keys.ENTER)
		f.send_keys('04-09-2019')
		time.sleep(1)
		f.send_keys(Keys.ENTER)

		g.click()

		time.sleep(5)

		browser.switch_to.frame('frmbookdtls')

		for busdata in browser.find_elements_by_id('busopt') :
			links.write(busdata.get_attribute('value') +'\n')
			time.sleep(0.2)
			print(city_from + " to " + city_to )

links.close()



# ./getStops.php?dptDt="+field[1]+"&dptTm="+field[2]+"&bt="+field[3]+"&field="+field[4]+"&field2="+field[5]+"&frm="+field[6]+"&till="+field[7], 'sdfsdf1',  'dependent=yes,toolbar=0,scrollbars=1,location=0,statusbar=1,menubar=0,resizable=1,width=550,height=500,left = 462,top = 154
# https://public.msrtcors.com/ticket_booking/getStops.php?dptDt=2019-09-04&dptTm=00:15&bt=SL&field=569930&field2=PAREL%20to%20BHOR%20via%20KASURDI&frm=DDRE&till=SWR