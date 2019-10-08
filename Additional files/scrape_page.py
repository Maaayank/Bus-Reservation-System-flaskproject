import selenium as se
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

stops_table = open('stop_details2.txt','a')

links = open('links_attributes.txt','r')

browser = webdriver.Chrome(executable_path='chromedriver.exe')

website_URL = 'https://public.msrtcors.com/users/guest_user_wel.php'

linksList = []
base_details = []

for lines in links.readlines() :
	field = lines.strip().split('|')
	if len(field) == 1 :
		print(field[0])
	else : 
		linksList.append("https://public.msrtcors.com/ticket_booking/getStops.php?dptDt="+field[1]+"&dptTm="+field[2]+"&bt="+field[3]+"&field="+field[4]+"&field2="+field[5]+"&frm="+field[6]+"&till="+field[7])
		base_details.append([field[4],field[5],field[3]])

email = 'mayank30@somaiya.edu'
cemail = 'mayank30@somaiya.edu'
phno = '9029772254'
browser.get(website_URL)

time.sleep(2)


stops = ['MUMBAI','PUNE','RATNAGIRI','AKOLA','NASIK','NAGPUR','AHMEDNAGAR','AMRAVATI','KOLHAPUR','JALGAON']


browser.switch_to.frame('frmMain1')

a = browser.find_element_by_id("email")
a.send_keys(email)

b = browser.find_element_by_xpath("//input[@id = 'conemail']")
b.send_keys(cemail)

c = browser.find_element_by_xpath("//input[@id = 'mobno']")
c.send_keys(phno)

browser.find_element_by_xpath("//input[@id = 'btnSubmit']").click()
time.sleep(2);


for j in range(len(linksList)) :

	browser.get(linksList[j])
	[bus_no,route,bus_class] = base_details[j]
	browser.switch_to.default_content()
	stops_data = browser.find_elements_by_xpath("//table/tbody/tr[4]/td/table/tbody/tr")
	no_of_stops = len(browser.find_elements_by_xpath("//table/tbody/tr[4]/td/table/tbody/tr"))
	print(no_of_stops)
	stops_table.write("bus :" + "|" + bus_no + "|" + route + "|" + bus_class + "|" + str(no_of_stops) +"\n")
	for stop in stops_data[1:] :
		name = stop.find_element_by_xpath('./td[1]').text
		district = stop.find_element_by_xpath('./td[5]').text
		taluka = stop.find_element_by_xpath('./td[6]').text
		arvl = stop.find_element_by_xpath('./td[4]').text
		stops_table.write("stop :" + "|" + name+'|'+district+'|'+taluka +'|'+ arvl +'\n')
		print(name)
	time.sleep(2)

stops_table.close()

# https://public.msrtcors.com/ticket_booking/getStops.php?dptDt=2019-09-04&dptTm=00:15&bt=SL&field=569930&field2=PAREL%20to%20BHOR%20via%20KASURDI&frm=DDRE&till=SWR
# https://public.msrtcors.com/ticket_booking/getStops.php?dptDt=2019-09-02&dptTm=00:15&bt=SL&field=569930&field2=PAREL%20to%20BHOR%20via%20KASURDI&frm=DDRE&till=SWR,sdfsdf1,dependent=yes,toolbar=0,scrollbars=1,location=0,statusbar=1,menubar=0,resizable=1,width=550,height=500,left%20=%20462,top%20=%20154