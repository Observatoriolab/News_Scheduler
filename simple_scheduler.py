import schedule
import time
import requests 
import json
import xmltodict
#REGEX LIBRARY
import re
from ast import literal_eval


API_ENDPOINT_TO_POST = "https://satelite-noticias-api.herokuapp.com/create_news"


API_ENDPOINT_REGISTER = "https://satelite-noticias-api.herokuapp.com/registration"
API_ENDPOINT_LOGIN = "https://satelite-noticias-api.herokuapp.com/login"

global idBot


def substractStrings(str1,str2):
    result =  "".join(str1.rsplit(str2))
    return result

def regexTitle(title):
    axis = re.search(r"^[^:]*:", title)
    withoutAxis = substractStrings(title,axis.group())
    
    print("----------------------------------------------------------------------------------------------------------------------\n")
    print(withoutAxis)
    print("escribo aqui")
    print("----------------------------------------------------------------------------------------------------------------------\n")

    actualAxis = re.search(r".* -",withoutAxis)
    
    print("----------------------------------------------------------------------------------------------------------------------\n")
    print(actualAxis)
    print("----------------------------------------------------------------------------------------------------------------------\n")
    return actualAxis.group()

def job():
    print('Im working on it...')
    # Aqui estan las noticias que se descargan en formato xml
    
    # ENDPOINT DE NOTICIAS DEL OBSERVATORIO ESPECIALIZADAS
    API_ENDPOINT_DATA = "https://dl.dropboxusercontent.com/s/2ai5twyzkmmkfdn/feed_rss_general_Filtro2.xml?dl=0"
    
    # sending post request and saving response as response object 
    r = requests.get(url = API_ENDPOINT_DATA) 


    #Transformar formato byte a string con codificacion utf-8
    rssContent = r.content.decode("utf-8") 
    parse_data = xmltodict.parse(rssContent)
    print("----------------------------------------")
    print(type(parse_data))
    print("----------------------------------------")

    listOfNews = json.dumps(parse_data, indent=4, sort_keys=True)
    d = json.loads(listOfNews)
    #print(d['rss']['channel']['item'])

    #Se tienen todas las noticias enlistadas en "data"
    realData =  d['rss']['channel']['item']


    listOfNews = json.loads(json.dumps(realData, indent=4, sort_keys=True))

    for news_single in listOfNews:
        print(news_single)
        source = news_single["category"][0]["#text"] 
        country = news_single["category"][1]["#text"]
        axis = news_single["category"][2]["#text"]
        try:            
            date = news_single["pubDate"].replace(",","")
        
        except KeyError:
            date = ''
        
        
        print("----------------------------------------------------------------------------------------------------------------------\n")
        print(news_single["link"])
        print("----------------------------------------------------------------------------------------------------------------------\n")
        actualTitle = regexTitle(news_single["title"])
        print("----------------------------------------------------------------------------------------------------------------------\n")
        print(source)
        print(country)
        print(axis)
        print(date)
        print("----------------------------------------------------------------------------------------------------------------------\n")
        data = {"title": actualTitle,
                "content_summary": news_single["description"],
                "link":news_single["link"],
                "tags": "",
                "source": source,
                "country": country,
                "axis_primary": axis,
                "axis_secondary": "",
                "date": date,
                "idBot": id,
                "type": "Fintech"}


        print("viendo que se va a enviar -->>>>>>>   ", data)
        reply = requests.post(url = API_ENDPOINT_TO_POST, data = data) 
        print(reply)



def createNewsBot():
    print('Im working on it...')
    
    data = {
            "username": "NewsBot",
            "email": "randomnames@gmail.com",
            "password1":"changeme123",
            "password2": "changeme123"
	
    }
    id = requests.post(url = API_ENDPOINT_LOGIN, data = data)  
    print('esto fue lo que me respondieron')
    print(id)
    if not id:
        id = requests.post(url = API_ENDPOINT_REGISTER, data = data)  

    idBot = id    


    

#Llamado a la funcion afuera del job
createNewsBot()
# 6 hrs
schedule.every(360).minutes.do(job)
#schedule.every().monday.at("14:09").do(job)



while True:
    schedule.run_pending()
    time.sleep(1)
