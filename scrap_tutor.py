from bs4 import BeautifulSoup
from urllib import urlopen
import requests
import csv

csv.register_dialect(
    'mydialect',
    delimiter = ',',
    quotechar = '"',
    doublequote = True,
    skipinitialspace = True,
    lineterminator = '\r\n',
    quoting = csv.QUOTE_MINIMAL)

base_url = 'https://www.myprivatetutor.com/institutes'
headers = {'User-agent': 'Mozilla/5.0'}
webpage = requests.get(base_url, headers=headers )

soup = BeautifulSoup(webpage.content, "html.parser")
locations_url = []
links_mess = soup.find('div',class_='sub_location')

for location in links_mess.find_all('li'):
	print location.find('a').string
	locations_url.append(location.find('a').string)

for location in locations_url:
	with open(location+'.csv','wb') as mycsv:
		c = csv.writer(mycsv, dialect='mydialect')
		c.writerow(['Name','Phone','Website','Area','Address','City','Pincode','India','Image','Category','About'])



		print '\n\nSCRAPPING FOR '+location+'\n\n'

		url = base_url+'/'+location

		headers = {'User-agent': 'Mozilla/5.0'}
		webpage = requests.get( url, headers=headers )
		#soup = BeautifulSoup(webpage.content, "html.parser")

		soup = BeautifulSoup(webpage.content, "html.parser")####CHANGE
		stores_url=[]
		li = soup.find_all('div',class_='listing_block_holder')

		li2=[]
		for x in li:
			if 'Pincode' in x.get_text():
				for y in x.find_all('li'):
					#print(y)
					#print('########################')
					if 'Pincode' in y.get_text():
						#print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
						li2.append(y.get_text().replace('<span>Pincode:</span>',''))
			else:
				li2.append('')
		#print(li2)

		z=0

		for x in li :
			stores_url.append(x.find('a')['href'])
		#print(soup)


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
			store_det['city']='Delhi'
			store_det['pincode']=''
			store_det['country'] = 'India'

			print('\n--------------------start-------------------\n')



			store_det['name'] = soup.find('div', class_='memtitle_holder').find('h2').get_text()
			print(store_det['name'])

			temp = soup.find('div', class_="instute-contact-details")
			#print(temp)
			#print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
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
			print(store_det['website'])

			temp = soup.find_all('div', class_="member_basic_info_holder")

			#print(soup.find('div', class_="centerimg_holder"))
			if soup.find('div', class_="img_holder") is not None and soup.find('div', class_="img_holder").find('img') is not None:
				store_det['images'] = 'https://www.myprivatetutor.com'+soup.find('div', class_="img_holder").find('img')['src']
				print('^^^^^^^^^^^^^^^^^^')
			print(store_det['images'])


			for x in temp:
				temp3 = x.find_all('li')
			#print(temp3)
			if len(temp3) >= 1 and temp3[0].find('a') is not None:
				store_det['area'] = temp3[0].find('a').get_text()
			if len(temp3) >= 2:
				store_det['addr'] = temp3[1].get_text().replace('Address:','').lstrip()
			if len(temp3) >= 3:
				store_det['category'] = temp3[2].get_text().replace("Courses:",'').lstrip()
			print(store_det['area'].encode('utf-8'))
			print(store_det['addr'].encode('utf-8'))
			print(store_det['category'].encode('utf-8'))

			temp = soup.find('div', class_='prof_cont_block')
			if temp is not None and len(temp.find_all('p')) >= 2:
				store_det['about'] = temp.find_all('p')[1].get_text()
			print(store_det['about'].encode('utf-8'))


			c.writerow([
						store_det['name'].encode('utf8'),
						store_det['phone'].encode('utf8'),
						store_det['website'].encode('utf8'),
						store_det['area'].encode('utf8'),
						store_det['addr'].encode('utf8'),
						'Delhi'.encode('utf8'),
						li2[z].replace('Pincode:','').encode('utf8'),
						'India'.encode('utf8'),
						store_det['images'].encode('utf8'),
						store_det['category'].encode('utf8'),
						store_det['about'].encode('utf8')

						])
			z+=1

			print('\n--------------------------------------------\n')
