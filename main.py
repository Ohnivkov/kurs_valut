import json
import os

import requests
import telebot
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent

user_file = os.path.join(os.getcwd(), 'users.json')
curs_file = os.path.join(os.getcwd(), 'kurs.json')


class PrivatBank:
    def get_kurs_dollarsell(self):
        r = requests.get('https://privatbank.ua/', timeout=10)
        get_bs_obj = bs(r.text, 'html.parser')
        return float(get_bs_obj.find('td', id='USD_sell').text.strip())

    def get_kurs_dollarbuy(self):
        r = requests.get('https://privatbank.ua/', timeout=10)
        get_bs_obj = bs(r.text, 'html.parser')
        return float(get_bs_obj.find('td', id='USD_buy').text.strip())


    def get_kurs_eurosell(self):
        r = requests.get('https://privatbank.ua/', timeout=10)
        get_bs_obj = bs(r.text, 'html.parser')
        return float(get_bs_obj.find('td', id='EUR_sell').text.strip())

    def get_kurs_eurobuy(self):
        r = requests.get('https://privatbank.ua/', timeout=10)
        get_bs_obj = bs(r.text, 'html.parser')
        return float(get_bs_obj.find('td', id='EUR_buy').text.strip())


class UkrSib:
    def get_kurs_dollarsell(self):
        ua = UserAgent()
        header = {'User-Agent': ua.chrome}
        r = requests.get("https://ukrsibbank.com/currency-cash/", headers=header)
        get_bs_obj = bs(r.text, 'html.parser')
        values = get_bs_obj.find_all('div', class_='module-exchange__item-text')
        return float(values[1].text)

    def get_kurs_dollarbuy(self):
        ua = UserAgent()
        header = {'User-Agent': ua.chrome}
        r = requests.get("https://ukrsibbank.com/currency-cash/", headers=header)
        get_bs_obj = bs(r.text, 'html.parser')
        values = get_bs_obj.findAll('div', class_='module-exchange__item-text')
        return float(values[3].text)

    def get_kurs_eurosell(self):
        ua = UserAgent()
        header = {'User-Agent': ua.chrome}
        r = requests.get("https://ukrsibbank.com/currency-cash/", headers=header)
        get_bs_obj = bs(r.text, 'html.parser')
        values = get_bs_obj.findAll('div', class_='module-exchange__item-text')
        return float(values[7].text.strip().replace(',', '.'))

    def get_kurs_eurobuy(self):
        ua = UserAgent()
        header = {'User-Agent': ua.chrome}
        r = requests.get("https://ukrsibbank.com/currency-cash/", headers=header)
        get_bs_obj = bs(r.text, 'html.parser')
        values = get_bs_obj.findAll('div', class_='module-exchange__item-text')
        return float(values[9].text.strip().replace(',', '.'))


class OshadBank:
    def get_kurs_dollarsell(self):
        res = {}
        r = requests.get("https://www.oschadbank.ua")
        get_bs_obj = bs(r.text, 'html.parser')
        for line in get_bs_obj.findAll('div', class_='currency__item', limit=2):
            buy, sell = line.findAll('span', class_='currency__item_value')
            if line.find('span', class_="currency__item_name").text == 'USD':
                res['usd_sell'] = sell.span.text
        return float(res['usd_sell'])
    def get_kurs_dollarbuy(self):
        res = {}
        r = requests.get("https://www.oschadbank.ua")
        get_bs_obj = bs(r.text, 'html.parser')
        for line in get_bs_obj.findAll('div', class_='currency__item', limit=2):
            buy, sell = line.findAll('span', class_='currency__item_value')
            if line.find('span', class_="currency__item_name").text == 'USD':
                res['usd_buy'] = sell.span.text

        return float(res['usd_buy'])
    def get_kurs_eurosell(self):
        res = {}
        r = requests.get("https://www.oschadbank.ua")
        get_bs_obj = bs(r.text, 'html.parser')
        for line in get_bs_obj.findAll('div', class_='currency__item', limit=2):
            buy, sell = line.findAll('span', class_='currency__item_value')
            if line.find('span', class_="currency__item_name").text == 'EUR':
                res['eur_sell'] = sell.span.text

        return float(res['eur_sell'])
    def get_kurs_eurobuy(self):
        res = {}
        r = requests.get("https://www.oschadbank.ua")
        get_bs_obj = bs(r.text, 'html.parser')
        for line in get_bs_obj.findAll('div', class_='currency__item', limit=2):
            buy, sell = line.findAll('span', class_='currency__item_value')
            if line.find('span', class_="currency__item_name").text == 'EUR':
                res['eur_buy'] = sell.span.text

        return float(res['eur_buy'])
class KredoBank:
    def get_kurs_dollarsell(self):
        r = requests.get("https://kredobank.com.ua/info/kursy-valyut/commercial")
        get_bs_obj = bs(r.text, 'html.parser')
        values=get_bs_obj.findAll('td')

        return values[2].text
    def get_kurs_dollarbuy(self):
        r = requests.get("https://kredobank.com.ua/info/kursy-valyut/commercial")
        get_bs_obj = bs(r.text, 'html.parser')
        values = get_bs_obj.findAll('td')
        return values[3].text
    def get_kurs_eurosell(self):
        r = requests.get("https://kredobank.com.ua/info/kursy-valyut/commercial")
        get_bs_obj = bs(r.text, 'html.parser')
        values = get_bs_obj.findAll('td')

        return values[8].text
    def get_kurs_eurobuy(self):
        r = requests.get("https://kredobank.com.ua/info/kursy-valyut/commercial")
        get_bs_obj = bs(r.text, 'html.parser')
        values = get_bs_obj.findAll('td')
        return values[9].text


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
    privat = PrivatBank()
    ukrsib = UkrSib()
    oshad = OshadBank()
    kredobank = KredoBank()
    kurs['privat'] = {
        'USD': {"sell": privat.get_kurs_dollarsell(), "buy": privat.get_kurs_dollarbuy()},
        'EUR': {"sell": privat.get_kurs_eurosell(), "buy": privat.get_kurs_eurobuy()}}
    kurs['ukrsib'] = {
        'USD': {"sell": ukrsib.get_kurs_dollarsell(), "buy": ukrsib.get_kurs_dollarbuy()},
        'EUR': {"sell": ukrsib.get_kurs_eurosell(), "buy": ukrsib.get_kurs_eurobuy()}}
    kurs['oshad'] = {
        'USD': {"sell": oshad.get_kurs_dollarsell(), "buy": oshad.get_kurs_dollarbuy()},
        'EUR': {"sell": oshad.get_kurs_eurosell(), "buy": oshad.get_kurs_eurobuy()}}
    kurs['kredobank'] = {
        'USD': {"sell": kredobank.get_kurs_dollarsell(), "buy": kredobank.get_kurs_dollarbuy()},
        'EUR': {"sell": kredobank.get_kurs_eurosell(), "buy": kredobank.get_kurs_eurobuy()}}
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
    if main(get_new_kurs()):
        with open(user_file) as f:
            user_list = json.load(f)
        for i in user_list:
            if user_list[i]:
                send_telegram(send_to_tel, i)
