import requests
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
import json
import telebot
import os

def privatbank(a):
    r = requests.get('https://privatbank.ua/', timeout=10)
    get_bs_obj = bs(r.text, 'html.parser')
    return float(get_bs_obj.find('td', id=a).text.strip())

def ukrsib(a,b):
    ua = UserAgent()

    header = {'User-Agent': ua.chrome}
    r = requests.get("https://ukrsibbank.com/", headers=header)
    get_bs_obj = bs(r.text, 'html.parser')
    values = get_bs_obj.find('ul', class_='module-exchange__list module-exchange__list--cash').text.split()
    count = 0
    for i in range(values.index(a), len(values)):
        if not values[i].isalpha():
            count += 1
            if count == b:
                return float('.'.join(values[i].split(',')))


def oshadbank():
    l={}
    res = {}
    r = requests.get("https://www.oschadbank.ua")
    get_bs_obj = bs(r.text, 'html.parser')
    for line in get_bs_obj.findAll('div', class_='currency__item', limit=2):
        buy,sell = line.findAll('span', class_='currency__item_value')
        if line.find('span', class_="currency__item_name").text == 'USD':
            res['usd_sell'] = sell.span.text
            res['usd_buy'] = buy.span.text
        if line.find('span', class_="currency__item_name").text == 'EUR':
            res['eur_sell'] = sell.span.text
            res['eur_buy'] = buy.span.text
            l={'USD':{'sell':float(res['usd_sell']), 'buy':float(res['usd_buy'])},'EUR':{'sell':float(res['eur_sell']), 'buy':float(res['eur_buy'])}}
    return l

# def pumb():
#     res = {}
#     ua = UserAgent()
#     header = {'User-Agent': str(ua.chrome)}
#     r = requests.get("https://www.pumb.ua/", headers=header,verify=False, proxies={'https': 'http://94.74.80.88:18081'})
#     get_bs_obj = bs(r.text, 'html.parser')
#     l = []
#     for line in get_bs_obj.findAll('div', class_='rates-block', limit=6):
#         r = line.text
#         l.append((''.join(
#             [r[i] for i in range(len(line.text)) if line.text[i].isdigit() or r[i] == '.' and r[i - 1].isdigit()])))
#     res['usd_sell'] = float(l[1])
#     res['usd_buy'] = float(l[2])
#     res['eur_sell'] = float(l[4])
#     res['eur_buy'] = float(l[5])
#
#     l = {'USD': {'sell':float(res['usd_sell']), 'buy':float(res['usd_buy'])},
#          'EUR': {'sell':float(res['eur_sell']), 'buy':float(res['eur_buy'])}}
#     return l

def kredobank():
    r = requests.get("https://kredobank.com.ua/info/kursy-valyut/commercial")
    get_bs_obj = bs(r.text, 'html.parser')
    res={}
    l=[]
    for line in get_bs_obj.findAll('div', class_='chart__number'):
        l.append(line.text)
    res['usd_sell'] = l[1]
    res['usd_buy'] = l[0]
    for line in get_bs_obj.findAll('td', limit=10):
        l.append(line.text)
    res['eur_sell'] = l[10]
    res['eur_buy'] = l[11]
    l1 = {'USD': {'sell': float(res['usd_sell']), 'buy': float(res['usd_buy'])}, 'EUR':{'sell':float(res['eur_sell']), 'buy':float(res['eur_buy'])}}
    return l1

def getfilekurs():
    with open(curs_file) as kurs:
        templates = json.load(kurs)
    return templates

def putdatetofilekurs(data):
    with open(curs_file, 'w') as f:
        json.dump(data, f)

def get_kurs_from_bank(kurs, bankname):
    return (bankname, str(kurs[bankname]['USD']['sell']), str(kurs[bankname]['USD']['buy']), str(kurs[bankname]['EUR']['sell']), str(kurs[bankname]['EUR']['buy']))




def message(kurs, bankname):
    message = """
<b><u>{}</u></b>
  Доллар:
    Продаж: {}
    Купівля: {}
  Євро:
    Продаж: {}
    Купівля: {}
     """.format(bankname, *kurs)
    return message
def send_telegram(message,token):
    bot=telebot.TeleBot('5343945393:AAHa9fg3dyQBC624pPjQppRUiSPpNXgj1js')
    bot.send_message(token,message,parse_mode='html')
def kirilitsia(bankname):
    d = {'oshad':'ОщадБанк',
         'privat':'Приват',
         'ukrsib':'Укрсиб',
         'kredobank':'Кредобанк',
         'pumb':'Пумб'}
    return d[bankname]

kurs = {}
kurs['ukrsib'] = {
     'USD': {"sell": ukrsib('USD',2), "buy": ukrsib('USD',1)},
     'EUR': {"sell": ukrsib('EUR', 2), "buy": ukrsib('EUR', 1)}}
kurs['privat'] = {
    'USD': {"sell": privatbank("USD_sell"), "buy": privatbank("USD_buy")},
    'EUR': {"sell": privatbank("EUR_sell"), "buy": privatbank("EUR_buy")}}
kurs['oshad'] = oshadbank()
kurs['kredobank'] = kredobank()
if not os.path.exists(os.path.join(os.getcwd(), 'kurs.json')):
    with open(os.path.join(os.getcwd(), 'kurs.json'),'w') as f:
        json.dump(kurs, f)
if not os.path.exists(os.path.join(os.getcwd(), 'users.json')):
    with open(os.path.join(os.getcwd(), 'users.json'),'w') as f:
        json.dump({}, f)

user_file = os.path.join(os.getcwd(), 'users.json')
curs_file = os.path.join(os.getcwd(), 'kurs.json')

send_to_tel = ''
def main():
    kurs_old = getfilekurs()
    flag = False
    vivod = []
    global send_to_tel
    for bank in kurs:
        for val in kurs[bank]:
             for sell_buy in kurs[bank][val]:
                if kurs[bank][val][sell_buy] != kurs_old[bank][val][sell_buy]:
                    vivod.append('<s>{}</s> <b>{}</b>'.format(str(kurs_old[bank][val][sell_buy]), str(kurs[bank][val][sell_buy])))
                    flag = True
                else:
                    vivod.append(str(kurs[bank][val][sell_buy]))
        send_to_tel += message(vivod, kirilitsia(bank))
        vivod = []

    if flag:
        return True
    else:
        return False

if __name__ == '__main__':
    if main()==True:
        with open(user_file) as f:
            user_list = json.load(f)
        for i in user_list:
            if user_list[i]:
                send_telegram(send_to_tel,i)

        putdatetofilekurs(kurs)
    send_to_tel = ''