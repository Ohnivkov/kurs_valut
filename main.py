import requests
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
import json
import telebot
import os

user_file = os.path.join(os.getcwd(), 'users.json')
curs_file = os.path.join(os.getcwd(), 'kurs.json')


def privatbank(a):
    r = requests.get('https://privatbank.ua/', timeout=10)
    get_bs_obj = bs(r.text, 'html.parser')
    return float(get_bs_obj.find('td', id=a).text.strip())


def ukrsib():
    ua = UserAgent()
    kurs_dict={}
    header = {'User-Agent': ua.chrome}
    r = requests.get("https://ukrsibbank.com/", headers=header)
    get_bs_obj = bs(r.text, 'html.parser')
    values = get_bs_obj.findAll('div', class_='module-exchange__item-text')
    kurs_dict['USD']={"sell":float(values[1].text.strip().replace(',','.')),'buy':float(values[2].text.strip().replace(',','.'))}
    kurs_dict['EUR']={"sell":float(values[5].text.strip().replace(',','.')),'buy':float(values[6].text.strip().replace(',','.'))}
    return kurs_dict


def oshadbank():
    l = {}
    res = {}
    r = requests.get("https://www.oschadbank.ua")
    get_bs_obj = bs(r.text, 'html.parser')
    for line in get_bs_obj.findAll('div', class_='currency__item', limit=2):
        buy, sell = line.findAll('span', class_='currency__item_value')
        if line.find('span', class_="currency__item_name").text == 'USD':
            res['usd_sell'] = sell.span.text
            res['usd_buy'] = buy.span.text
        if line.find('span', class_="currency__item_name").text == 'EUR':
            res['eur_sell'] = sell.span.text
            res['eur_buy'] = buy.span.text
            l = {'USD': {'sell': float(res['usd_sell']), 'buy': float(res['usd_buy'])},
                 'EUR': {'sell': float(res['eur_sell']), 'buy': float(res['eur_buy'])}}
    return l


def kredobank():
    r = requests.get("https://kredobank.com.ua/info/kursy-valyut/commercial")
    get_bs_obj = bs(r.text, 'html.parser')
    res = {}
    l = []
    for line in get_bs_obj.findAll('div', class_='chart__number'):
        l.append(line.text)
    res['usd_sell'] = l[1]
    res['usd_buy'] = l[0]
    for line in get_bs_obj.findAll('td', limit=10):
        l.append(line.text)
    res['eur_sell'] = l[10]
    res['eur_buy'] = l[11]
    l1 = {'USD': {'sell': float(res['usd_sell']), 'buy': float(res['usd_buy'])},
          'EUR': {'sell': float(res['eur_sell']), 'buy': float(res['eur_buy'])}}
    return l1


def getfilekurs():
    with open(curs_file) as kurs:
        templates = json.load(kurs)
    return templates


def putdatetofilekurs(data):
    with open(curs_file, 'w') as f:
        json.dump(data, f)


def get_kurs_from_bank(kurs, bankname):
    return (
        bankname, str(kurs[bankname]['USD']['sell']), str(kurs[bankname]['USD']['buy']),
        str(kurs[bankname]['EUR']['sell']),
        str(kurs[bankname]['EUR']['buy']))


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


def send_telegram(message, token):
    bot = telebot.TeleBot('5343945393:AAHa9fg3dyQBC624pPjQppRUiSPpNXgj1js')
    bot.send_message(token, message, parse_mode='html')


def kirilitsia(bankname):
    d = {'oshad': 'ОщадБанк',
         'privat': 'Приват',
         'ukrsib': 'Укрсиб',
         'kredobank': 'Кредобанк',
         'pumb': 'Пумб'}
    return d[bankname]


def get_new_kurs():
    kurs = {}


    kurs['privat'] = {
        'USD': {"sell": privatbank("USD_sell"), "buy": privatbank("USD_buy")},
        'EUR': {"sell": privatbank("EUR_sell"), "buy": privatbank("EUR_buy")}}
    kurs['ukrsib'] = ukrsib()
    kurs['oshad'] = oshadbank()
    kurs['kredobank'] = kredobank()
    return kurs


if not os.path.exists(os.path.join(os.getcwd(), 'kurs.json')):
    with open(os.path.join(os.getcwd(), 'kurs.json'), 'w') as f:
        json.dump(get_new_kurs(), f)
if not os.path.exists(os.path.join(os.getcwd(), 'users.json')):
    with open(os.path.join(os.getcwd(), 'users.json'), 'w') as f:
        json.dump({}, f)

send_to_tel = ''


def main(kurs):
    kurs_old = getfilekurs()
    flag = False
    vivod = []
    global send_to_tel
    for bank in kurs:
        for val in kurs[bank]:
            for sell_buy in kurs[bank][val]:
                if kurs[bank][val][sell_buy] != kurs_old[bank][val][sell_buy]:
                    vivod.append('<s>{}</s> <b>{}</b>'.format(str(kurs_old[bank][val][sell_buy]),
                                                              str(kurs[bank][val][sell_buy])))
                    flag = True
                else:
                    vivod.append(str(kurs[bank][val][sell_buy]))
        send_to_tel += message(vivod, kirilitsia(bank))
        vivod = []

    if flag:
        putdatetofilekurs(kurs)
        return True
    else:
        return False


if __name__ == '__main__':
    if main(get_new_kurs()) == True:
        with open(user_file) as f:
            user_list = json.load(f)
        for i in user_list:
            if user_list[i]:
                send_telegram(send_to_tel, i)
