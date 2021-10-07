#Installed
import requests


#Start server
if __name__ == '__main__':

    #Setup Refresh etc
    url = 'http://localhost:5011/autorefresh/{interval}'
    myobj = {'interval': '5'}

    try:
        x = requests.post(url, data = myobj)
    except:
        print('Failed')

    try:
        r = requests.get('http://localhost:5011/ping')
        print(r)
    except:
        print('Ping Failed')

    while True:
        continue
