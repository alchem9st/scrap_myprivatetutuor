from bs4 import BeautifulSoup
import urllib2
from selenium import webdriver
import requests
import csv
import time
from pyexcel.cookbook import merge_all_to_a_book
import pyexcel.ext.xlsx # needed to support xlsx format, pip install pyexcel-xlsx
import glob

csv.register_dialect(
    'mydialect',
    delimiter = ',',
    quotechar = '"',
    doublequote = True,
    skipinitialspace = True,
    lineterminator = '\r\n',
    quoting = csv.QUOTE_MINIMAL)

with open('private_scrap_data1.csv','a') as mycsv:
	c = csv.writer(mycsv, dialect='mydialect')
	c.writerow(['Name','Phone','Website','Area','Address','City','Pincode','India','Image','Category','About'])


	url = 'https://www.myprivatetutor.com/institute-all-cities.php'
	    
	headers = {'User-agent': 'Mozilla/5.0'}
	webpage = requests.get( url, headers=headers )
	#soup = BeautifulSoup(webpage.content, "html.parser")
	page = urllib2.urlopen('https://www.myprivatetutor.com/institute-all-cities.php')
	soup = BeautifulSoup(page,"html.parser")####CHANGE

	temps = soup.find_all('div',class_='display_block_alpha')
	for temp in temps :

		temp1= temp.find('div',class_='dis_data_area')

		temp2 = temp1.find_all('li')

		for x in temp2 :
			name = 	x.find('a').text
			print(name)		
			url = 'https://www.myprivatetutor.com/institutes/'+x.find('a').text
    
			headers = {'User-agent': 'Mozilla/5.0'}
			webpage = requests.get( url, headers=headers )
			#soup = BeautifulSoup(webpage.content, "html.parser")
			page = urllib2.urlopen('https://www.myprivatetutor.com/institutes/'+x.find('a').text)
			soup = BeautifulSoup(page,"html.parser")####CHANGE
			stores_url=[]
			li = soup.find_all('div',class_='listing_block_holder tutorlisting_latest_holder')

			li2=[]
			for x in li:
				for y in x.find_all('li'):
					#print(y)
					#print('########################')
					if 'Pincode' in y.get_text():
						#print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
						li2.append(y.get_text().replace('<span>Pincode:</span>',''))
			#print(li2)
			#print("\n")
			z=0 

			for x in li :
				stores_url.append(x.find('a')['href'])
			#print(stores_url)

			for store_url in stores_url:

				url = store_url
				headers = {'User-agent': 'Mozilla/5.0'}
				webpage = requests.get( url, headers=headers )
				soup = BeautifulSoup(webpage.content, "html.parser")
		
		
				store_det = {}

				store_det['name']='N/A'
				store_det['phone']='N/A'
				store_det['addr']='N/A'
				store_det['mail']='N/A'
				store_det['website']='N/A'
				store_det['area']='N/A'
				store_det['category']='N/A'
				store_det['services_offered']=''
				store_det['about'] = 'N/A'
				store_det['images'] = ''
				store_det['city']= name
				store_det['pincode']=''
				store_det['country'] = 'India'

				print('\n--------------------start-------------------\n')

				store_det['name'] = soup.find('div', class_='memtitle_holder').find('h2').get_text()
				print(store_det['name'])
				print("\n")
		
				temp = soup.find('div', class_="instute-contact-details")
				print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
				temp2 = []
				if temp is not None:
					temp2 = temp.find_all('a', class_='view_contact')
		
				if len(temp2) >= 1:
					store_det['phone'] = temp2[0]['href'].replace('tel:','')
				if len(temp2) >= 2:
					store_det['website'] = temp2[1]['href']
				if store_det['phone'] =='javascript:void(0);':store_det['phone']='N/A'
				if store_det['website'] =='javascript:void(0);':store_det['website']='N/A'
				print(store_det['phone'])
				print("\n")
				print(store_det['website'])
				print("\n")

				temp = soup.find_all('div', class_="member_basic_info_holder")
		
				if soup.find('div', class_="centerimg_holder") is not None and soup.find('div', class_="centerimg_holder").find('img') is not None:
					store_det['images'] = 'https://www.myprivatetutor.com'+soup.find('div', class_="centerimg_holder").find('img')['src']
					print('^^^^^^^^^^^^^^^^^^')
				print(store_det['images'])
		
				print("\n")
				for x in temp:
					temp3 = x.find_all('li')
				#print(temp3)
				if len(temp3) >= 1 and temp3[0].find('a') is not None:
					store_det['area'] = temp3[0].find('a').get_text()
				if len(temp3) >= 2:
					store_det['addr'] = temp3[1].get_text().replace('Address:','').lstrip()
				if len(temp3) >= 3:
					store_det['category'] = temp3[2].get_text().replace("Courses:",'').lstrip()
				print(store_det['area'])
				print("\n")
				print(store_det['addr'])
				print("\n")
				print(store_det['category'])

				temp = soup.find('div', class_='prof_cont_block')
				if temp is not None and len(temp.find_all('p')) >= 2:
					store_det['about'] = temp.find_all('p')[1].get_text()
				print(store_det['about'])
				if(z>=len(li2)) :
					li2.append(" ")

				c.writerow([
							store_det['name'].encode('utf8'),
							store_det['phone'].encode('utf8'),
							store_det['website'].encode('utf8'),
							store_det['area'].encode('utf8'),
							store_det['addr'].encode('utf8'),
							store_det['city'].encode('utf8'),
							li2[z].replace('Pincode:','').encode('utf8'),
							'India'.encode('utf8'),
							store_det['images'].encode('utf8'),
							store_det['category'].encode('utf8'),
							store_det['about'].encode('utf8')
					
							])
				z+=1

				print('\n--------------------------------------------\n')

merge_all_to_a_book(glob.glob("private_scrap_data.csv"), "output.xlsx")

				







