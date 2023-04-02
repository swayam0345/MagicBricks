from os import set_inheritable
from bs4 import BeautifulSoup
import requests, openpyxl


excel = openpyxl.Workbook()
sheet = excel.active
sheet.title = 'Magic_Bricks-BBSR-1'

sheet.append(['Description', 'Price', 'Carpet Area', 'Super/ Plot Area', 'Property Status', 'Transaction', 'Property Type', 'Furnishing', 'Tenant Preferred',
            'Availability', 'Society', 'Parking', 'Bathroom', 'Floor', 'Ownership', 'Owner', 'Balcony', 'Overlooking', 'Facing'])


#Web Srcapper API
def MagicBrickWebScrapper(source, transc, buildType):
    try:
        soup = BeautifulSoup(source.text, 'html.parser')

        properties  = soup.find_all('div', class_ = 'mb-srp__list')
            
        for pro in properties:
            description = price = carpet_area = super_area = status = furnish = tenant = avail = society = parking = bathroom = floor = ownership = owner = balcony = overlooking = facing =  'N/A'
            type = transc

            price       = pro.find('div', class_ = 'mb-srp__card__price--amount').text
            description = pro.find('h2', class_ = 'mb-srp__card--title').text
            owner       = pro.find('div', class_ = 'mb-srp__card__ads--name').get_text()
            section     = pro.find_all('div', class_= 'mb-srp__card__summary__list--item')

            for sec in section:
                sec_item = sec.find('div', class_ = 'mb-srp__card__summary--label').text
                #Carpet Area
                if sec_item == 'Carpet Area':
                    carpet_area = sec.find('div', class_ = 'mb-srp__card__summary--value').text
                #Super Area
                if sec_item == 'Super Area' or sec_item == "Plot Area":
                    super_area = sec.find('div', class_ = 'mb-srp__card__summary--value').text
                #Property Status
                if sec_item == 'Under Construction' or sec_item == 'status':
                    status = sec.find('div', class_ = 'mb-srp__card__summary--value').text
                #Property Type
                if(sec_item == 'Transaction'):
                    type = sec.find('div', class_ = 'mb-srp__card__summary--value').text
                #Furnishing
                if(sec_item == 'Furnishing' or sec_item == 'Furnishing Status'):
                    furnish = sec.find('div', class_ = 'mb-srp__card__summary--value').text
                #Tenant Preffered
                if(sec_item == 'Tenant Preferred'):
                    tenant = sec.find('div', class_ = 'mb-srp__card__summary--value').text
                #Availablity
                if(sec_item == 'Availability'):
                    avail = sec.find('div', class_ = 'mb-srp__card__summary--value').text
                #Society
                if(sec_item == 'Society'):
                    society = sec.find('div', class_ = 'mb-srp__card__summary--value').text
                #Car Parking
                if(sec_item == 'Car Parking'):
                    parking = sec.find('div', class_ = 'mb-srp__card__summary--value').text
                #Bathroom
                if(sec_item == 'Bathroom' or sec_item == 'Washroom'):
                    bathroom = sec.find('div', class_ = 'mb-srp__card__summary--value').text
                #Floor
                if(sec_item == 'Floor'):
                    floor = sec.find('div', class_ = 'mb-srp__card__summary--value').text
                #Ownership
                if(sec_item == 'Ownership'):
                    ownership = sec.find('div', class_ = 'mb-srp__card__summary--value').text
                #Balcony
                if(sec_item == 'Balcony'):
                    balcony = sec.find('div', class_ = 'mb-srp__card__summary--value').text
                #overlooking
                if(sec_item == 'overlooking'):
                    overlooking = sec.find('div', class_ = 'mb-srp__card__summary--value').text
                #Facing
                if(sec_item == 'facing'):
                    facing = sec.find('div', class_ = 'mb-srp__card__summary--value').text
            
            sheet.append([description, price, carpet_area, super_area, status, type, buildType, furnish, tenant,
                avail, society, parking, bathroom, floor, ownership, owner, balcony, overlooking, facing])
    
    except Exception as e:
        print(e)



#This API will extract URL of the footer of Magic Bricks website.
def GetUrlFooter(footUrl, transc, buildType):
    url = footUrl
    source = requests.get(url)
    source.raise_for_status()

    soup = BeautifulSoup(source.text, 'html.parser')

    footer = soup.find('div', class_ = 'swiper-wrapper').find_all('ul', class_ = 'mb-srp__faq__seo__card__list')
    for ft in footer:
        innerList = ft.find_all('li', class_ = 'mb-srp__faq__seo__card__list--item')
        for inner in innerList:
            listItem = inner.find('a').get('href')
            source_ptr = requests.get(listItem)
            source_ptr.raise_for_status()
            MagicBrickWebScrapper(source_ptr, transc, buildType)



#This API will extract URL of all flats to buy in Magic Bricks.
def GetAllUrlBuyFlat():
    page = 50

    for i in range(1, page):
        if(i == 1):
            url = 'https://www.magicbricks.com/flats-in-bhubaneswar-for-sale-pppfs/page-1'
        else:
            url = 'https://www.magicbricks.com/flats-in-bhubaneswar-for-sale-pppfs/page-'
            url += str(i)

        source_ptr = requests.get(url)
        source_ptr.raise_for_status()   #Captures the error in case the URL throws any.

        MagicBrickWebScrapper(source_ptr, "Buying", "Flat")
    
    GetUrlFooter(url, "Buying", "Flat")


#This API will extract URL of all houses to buy in Magic Bricks.
def GetAllUrlBuyHouse():
    page = 12

    for i in range(1, page):
        if(i == 1):
            url = 'https://www.magicbricks.com/independent-house-for-sale-in-bhubaneswar-pppfs/page-1'
        else:
            url = 'https://www.magicbricks.com/independent-house-for-sale-in-bhubaneswar-pppfs/page-'
            url += str(i)

        source_ptr = requests.get(url)
        source_ptr.raise_for_status()   #Captures the error in case the URL throws any.

        MagicBrickWebScrapper(source_ptr, "Buying", "House")
    
    GetUrlFooter(url, "Buying", "House")


#This API will extract URL of all villas to buy in Magic Bricks.
def GetAllUrlBuyVilla():
    page = 13

    for i in range(1, page):
        if(i == 1):
            url = 'https://www.magicbricks.com/villa-for-sale-in-bhubaneswar-pppfs/page-1'
        else:
            url = 'https://www.magicbricks.com/villa-for-sale-in-bhubaneswar-pppfs/page-'
            url += str(i)

        source_ptr = requests.get(url)
        source_ptr.raise_for_status()   #Captures the error in case the URL throws any.

        MagicBrickWebScrapper(source_ptr, "Buying", "Villa")
    
    GetUrlFooter(url, "Buying", "Villa")



#This API will extract URL of all plots to buy in Magic Bricks.
def GetAllUrlBuyPlot():
    page = 50

    for i in range(1, page):
        if(i == 1):
            url = 'https://www.magicbricks.com/residential-plots-land-for-sale-in-bhubaneswar-pppfs/page-1'
        else:
            url = 'https://www.magicbricks.com/residential-plots-land-for-sale-in-bhubaneswar-pppfs/page-'
            url += str(i)

        source_ptr = requests.get(url)
        source_ptr.raise_for_status()   #Captures the error in case the URL throws any.

        MagicBrickWebScrapper(source_ptr, "Buying", "Plot")
    
    GetUrlFooter(url, "Buying", "Plot")



#This API will extract URL of all office space to buy in Magic Bricks.
def GetAllUrlBuyOffice():
    page = 2

    for i in range(1, page):
        if(i == 1):
            url = 'https://www.magicbricks.com/office-space-for-sale-in-bhubaneswar-pppfs/page-1'
        else:
            url = 'https://www.magicbricks.com/office-space-for-sale-in-bhubaneswar-pppfs/page-'
            url += str(i)

        source_ptr = requests.get(url)
        source_ptr.raise_for_status()   #Captures the error in case the URL throws any.

        MagicBrickWebScrapper(source_ptr, "Buying", "Office Space")
    
    GetUrlFooter(url, "Buying", "Office Space")



#This API will extract URL of all flats to rent in Magic Bricks.
def GetAllUrlRentFlat():
    page = 21

    for i in range(1, page):
        if(i == 1):
            url = 'https://www.magicbricks.com/flats-for-rent-in-bhubaneswar-pppfr/page-1'
        else:
            url = 'https://www.magicbricks.com/flats-for-rent-in-bhubaneswar-pppfr/page-'
            url += str(i)

        source_ptr = requests.get(url)
        source_ptr.raise_for_status()   #Captures the error in case the URL throws any.

        MagicBrickWebScrapper(source_ptr, "Renting", "Flat")

    GetUrlFooter(url, "Renting", "Flat")



#This API will extract URL of all houses to rent in Magic Bricks.
def GetAllUrlRentHouse():
    page = 24

    for i in range(1, page):
        if(i == 1):
            url = 'https://www.magicbricks.com/independent-house-for-rent-in-bhubaneswar-pppfr/page-1'
        else:
            url = 'https://www.magicbricks.com/independent-house-for-rent-in-bhubaneswar-pppfr/page-'
            url += str(i)

        source_ptr = requests.get(url)
        source_ptr.raise_for_status()   #Captures the error in case the URL throws any.

        MagicBrickWebScrapper(source_ptr, "Renting", "House")

    GetUrlFooter(url, "Renting", "House")



#This API will extract URL of all villas to rent in Magic Bricks.
def GetAllUrlRentHouse():
    page = 3

    for i in range(1, page):
        if(i == 1):
            url = 'https://www.magicbricks.com/villa-for-rent-in-bhubaneswar-pppfr/page-1'
        else:
            url = 'https://www.magicbricks.com/villa-for-rent-in-bhubaneswar-pppfr/page-'
            url += str(i)

        source_ptr = requests.get(url)
        source_ptr.raise_for_status()   #Captures the error in case the URL throws any.

        MagicBrickWebScrapper(source_ptr, "Renting", "Villa")

    GetUrlFooter(url, "Renting", "Villa")



#This API will extract URL of all Office Spaces to rent in Magic Bricks.
def GetAllUrlRentOffice():
    page = 16

    for i in range(1, page):
        if(i == 1):
            url = 'https://www.magicbricks.com/office-space-for-rent-in-bhubaneswar-pppfr/page-1'
        else:
            url = 'https://www.magicbricks.com/office-space-for-rent-in-bhubaneswar-pppfr/page-'
            url += str(i)

        source_ptr = requests.get(url)
        source_ptr.raise_for_status()   #Captures the error in case the URL throws any.

        MagicBrickWebScrapper(source_ptr, "Renting", "Office Space")

    GetUrlFooter(url, "Renting", "Office Space")



#This API will extract URL of all Commercial Properties to rent in Magic Bricks.
def GetAllUrlRentCommerce():
    page = 27

    for i in range(1, page):
        if(i == 1):
            url = 'https://www.magicbricks.com/commercial-property-for-rent-in-bhubaneswar-pppfr/page-1'
        else:
            url = 'https://www.magicbricks.com/commercial-property-for-rent-in-bhubaneswar-pppfr/page-'
            url += str(i)

        source_ptr = requests.get(url)
        source_ptr.raise_for_status()   #Captures the error in case the URL throws any.

        MagicBrickWebScrapper(source_ptr, "Renting", "Commercial Properties")

    GetUrlFooter(url, "Renting", "Commercial Properties")


try:
    #URL for properties to buy
    GetAllUrlBuyFlat()
    GetAllUrlBuyHouse()
    GetAllUrlBuyVilla()
    GetAllUrlBuyPlot()
    GetAllUrlBuyOffice()

    #URL for properties to rent
    GetAllUrlRentFlat()
    GetAllUrlRentHouse()
    GetAllUrlRentOffice()
    GetAllUrlRentCommerce()

except Exception as e:
    print(e)

    
excel.save('Magic_Bricks-BBSR.xlsx')
