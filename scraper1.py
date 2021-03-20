from bs4 import BeautifulSoup
import requests
import pandas as pd
import xlsxwriter

web  = ['https://www.cable.co.uk/broadband/providers/bt-broadband/',
        'https://www.cable.co.uk/broadband/providers/talktalk-broadband/',
        'https://www.cable.co.uk/broadband/providers/virgin-media-broadband/',
        'https://www.cable.co.uk/broadband/providers/plusnet-broadband/',
        'https://www.cable.co.uk/broadband/providers/ee-broadband/',
        'https://www.cable.co.uk/broadband/providers/vodafone-broadband/',
        'https://www.cable.co.uk/broadband/providers/john-lewis-broadband/',
        'https://www.cable.co.uk/broadband/providers/sse-broadband/',
        'https://www.cable.co.uk/broadband/providers/now-broadband/',
        'https://www.cable.co.uk/broadband/providers/bt-broadband/fibre-broadband/',
        'https://www.cable.co.uk/broadband/providers/talktalk-fibre-broadband/',
        'https://www.cable.co.uk/broadband/providers/sky-broadband/fibre-broadband/'
         ]

BroadbandData = {"Plan":[],"Average Speed":[],"Monthly Download":[],
                 "Setup Cost":[],"Monthly Cost":[],"Contract Length":[]}
planname = []
average_speed = []
download = []
Setupcost = []
Contractlength = []
monthly = []

for pg in web:
  webpage_response = requests.get(pg)
  webpage = webpage_response.content
  soup = BeautifulSoup(webpage,'html.parser')

  page_name = soup.find_all(attrs = {'class':'cl-pn'})


  for i in page_name:
      name = i.get_text()
      planname.append(name)


  page_speed = soup.find_all(attrs = {'class':"cl-bb cl-simple-mt"})
  speeds = []
  for i in page_speed:
        speed = i.get_text()
        speeds.append(speed)


  for i in speeds:
      if i.endswith("Mb "):
          i = i.strip("Mb ")
          average_speed.append(int(i))
      else:
          download.append(i)


  page_setup = soup.find_all(attrs = {'class':'cl-pr cl-simple-mt'})
  numbers = []
  new_numbers = []


  for i in page_setup:
        number = i.get_text()
        numbers.append(number)



  for number in numbers:
       new_number = number.replace('Zero','£0')
       new_numbers.append(new_number)



  for i in new_numbers:
      if i.startswith('£'):
          i = i.strip("£")
          Setupcost.append(float(i))
      else:
          Contractlength.append(float(i))


  page_monthly = soup.find_all(attrs = {'class':'cl-pr cl-pr-strong'})



  for i in page_monthly:
      month = i.get_text().strip("£")
      monthly.append(float(month))

  BroadbandData['Plan'] = planname
  BroadbandData['Average Speed'] = average_speed
  BroadbandData['Monthly Download'] = download
  BroadbandData['Setup Cost'] = Setupcost
  BroadbandData['Monthly Cost'] = monthly
  BroadbandData['Contract Length'] = Contractlength




BroadBanddf = pd.DataFrame.from_dict(BroadbandData)
New = {"Plan":'30 Mb Fibre Broadband Only',"Average Speed":30,"Monthly Download":'Unlimited',
                 "Setup Cost":9.99,"Monthly Cost":17.99,"Contract Length":12}
BroadBanddf =BroadBanddf.append(New,ignore_index=True)
BroadBanddf['Whole Contract Price'] = BroadBanddf['Monthly Cost']*BroadBanddf['Contract Length']+BroadBanddf['Setup Cost']
print(BroadBanddf)


writer_obj = pd.ExcelWriter('TRIAL.xlsx',
                            engine='xlsxwriter')


BroadBanddf.to_excel(writer_obj, sheet_name='Sheet')

writer_obj.save()