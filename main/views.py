import bs4
from django.db.models import Sum, Prefetch, Q, Count
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
import requests
from django.shortcuts import render
from selenium.webdriver.common import service
from django.shortcuts import render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import logging
import os



def headd(request):
    return render(request, "main/headd.html")

def shop(request):
    images = [
        {'id': 1, 'name': 'сүйекші', 'image': 'images/1.png'},
        {'id': 2, 'name': 'қалам', 'image': 'images/2.png'},
        {'id': 3, 'name': 'жүректен жүреке', 'image': 'images/3.png'},
        {'id': 4, 'name': 'пластилин', 'image': 'images/4.png'},
        {'id': 5, 'name': 'клеевые точки', 'image': 'images/5.png'},
    ]

    selected_id = request.GET.get('product', '1')
    selected_image = next((img for img in images if str(img['id']) == selected_id), images[0])

    return render(request, 'main/shop.html', {
        'images': images,
        'selected_image': selected_image,
    })



def index(request):
    scale = ''
    distance_cm = ''
    result = ''

    if request.method == "POST":
        if 'calculate' in request.POST:
            scale = request.POST.get("scale", "")
            distance_cm = request.POST.get("distance_cm", "")
            try:
                result_value = float(scale) * float(distance_cm)
                result = f"{result_value}"
            except (ValueError, TypeError):
                result = "Қате енгізу!"
        elif 'clear' in request.POST:
            scale = ''
            distance_cm = ''
            result = ''

    return render(request, "main/index.html", {
        "scale": scale,
        "distance_cm": distance_cm,
        "result": result
    })



def make_models_map():
    models_map = {
        "хобби": [
            {
                "name": "Acron CSH-240B",
                "image": "images/1.png",
                "desc": "Acron кондиционер – қуатты үлгі.",
                "article": "ACR-CSH-240B",
                "power": "2200W",
                "size": "72 м²",
                "extra": "Инвертор, энергия классы A+"
            },
            {
                "name": "Acron CSH-120B",
                "image": "images/2.png",
                "desc": "Acron кондиционер – үйге арналған.",
                "article": "ACR-102",
                "power": "1800W",
                "size": "36 м²",
                "extra": "Түнгі режим, таймер"
            },
            {
                "name": "Acron CSHI-120B",
                "image": "images/3.png",
                "desc": "Acron кондиционер – кеңсе үшін.",
                "article": "ACR-103",
                "power": "2600W",
                "size": "30 м²",
                "extra": "Wi-Fi басқару"
            },
            {
                "name": "Acron CSH-180B",
                "image": "images/acron4.jpg",
                "desc": "Acron кондиционер – үнемді үлгі.",
                "article": "ACR-104",
                "power": "1500W",
                "size": "52 м²",
                "extra": "Эко-режим"
            },
            {
                "name": "Acron CSH-18DO",
                "image": "images/acron5.jpg",
                "desc": "Acron кондиционер – премиум үлгі.",
                "article": "ACR-105",
                "power": "3000W",
                "size": "54 м²",
                "extra": "Жылытқыш функциясы"
            },
        ],

        "almacom": [
            {
                "name": "Almacom ACH-24QF",
                "image": "images/Almacom.jpg",
                "desc": "Almacom – сенімді тұрмыстық үлгі.",
                "article": "ACH-24QF",
                "power": "2000W",
                "size": "72 кв",
                "extra": "Таймер, авто-тазалау"
            },
            {
                "name": "Almacom ACH-12QI",
                "image": "images/almacom2.jpg",
                "desc": "Almacom – кеңсе үшін қолайлы.",
                "article": "ALM-ACH-12QI",
                "power": "2400W",
                "size": "74 кв",
                "extra": "Wi-Fi басқару"
            },
            {
                "name": "Almacom ACH-24AS",
                "image": "images/almacom3.jpg",
                "desc": "Almacom – үнемді үлгі.",
                "article": "ALM-ACH-24AS",
                "power": "3000W",
                "size": "75 kv",
                "extra": "Эко-режим,Wi-Fi басқару"
            },
            {
                "name": "Almacom ACH-12LCi",
                "image": "images/almacom4.jpg",
                "desc": "Almacom – премиум үлгі.",
                "article": "ACH-12LCi",
                "power": "2800W",
                "size": "86 kv",
                "extra": "Жылытқыш функциясы"
            },
            {
                "name": "Almacom ACH-12IV",
                "image": "images/almacom5.jpg",
                "desc": "Almacom – қуатты үлгі.",
                "article": "ALM-ACH-12IV",
                "power": "3000W",
                "size": "35 м²",
                "extra": "Инвертор, энергия классы A++"
            },
        ],

        "aux": [
            {
                "name": "AUX ASW-H24A4/FXR1",
                "image": "images/AUX.jpg",
                "desc": "AUX – тұрмыстық үлгі.",
                "article": "AUX-H24A4/FXR1",
                "power": "1800W",
                "size": "70 kv",
                "extra": "Таймер"
            },
            {
                "name": "AUX H18A4/QGR1DI",
                "image": "images/aux2.jpg",
                "desc": "AUX – кеңсе үшін.",
                "article": "AUX-302",
                "power": "2200W",
                "size": "50 м²",
                "extra": "Wi-Fi басқару"
            },
            {
                "name": "AUX ASW-H07A4/FXR1",
                "image": "images/aux3.jpg",
                "desc": "AUX – үнемді үлгі.",
                "article": "AUX-H07A4/FXR1",
                "power": "1500W",
                "size": "23 м²",
                "extra": "Эко-режим"
            },
            {
                "name": "AUX ASW-H12C4",
                "image": "images/aux4.jpg",
                "desc": "AUX – премиум үлгі.",
                "article": "AUX-304",
                "power": "2800W",
                "size": "32 м²",
                "extra": "Жылытқыш функциясы"
            },
            {
                "name": "AUX ASW-H18A4/HCR3DI",
                "image": "images/aux5.jpg",
                "desc": "AUX – қуатты үлгі.",
                "article": "AUX-305",
                "power": "3000W",
                "size": "35 м²",
                "extra": "Инвертор, энергия классы A+"
            },
        ],

        "haier": [
            {
                "name": "Haier 24HRM503",
                "image": "images/haier.jpg",
                "desc": "Haier – тұрмыстық үлгі.",
                "article": "HAI-24503",
                "power": "2000W",
                "size": "70 кв",
                "extra": "Таймер, авто-тазалау"
            },
            {
                "name": "Haier HSU-24HFM4S03/R3(SDB) ",
                "image": "images/haier2.jpg",
                "desc": "Haier – кеңсе үшін.",
                "article": "HAI-402",
                "power": "2400W",
                "size": "70.0 кв",
                "extra": "Wi-Fi басқару Класс энергоэффективности A+++"
            },
            {
                "name": "Haier HSU- 12HTM303/R3 ",
                "image": "images/haier3.jpg",
                "desc": "Haier – үнемді үлгі.",
                "article": "HAI-303/R3",
                "power": "1600W",
                "size": "18 м²",
                "extra": "Эко-режим"
            },
            {
                "name": "Haier 24HRM503/R3(SDB)",
                "image": "images/haier.jpg",
                "desc": "Haier – премиум үлгі.",
                "article": "HAI-404",
                "power": "2800W",
                "size": "32 м²",
                "extra": "Жылытқыш функциясы"
            },
            {
                "name": "Haier AS25S2F2A-B",
                "image": "images/haier5.jpg",
                "desc": "Haier – қуатты үлгі.",
                "article": "HAI-AS25S2F2A-B",
                "power": "3200W",
                "size": "26 kv ",
                "extra": "Инвертор, энергия классы A++"
            },
        ],

        "samsung": [
            {
                "name": "Samsung AR12TXHQASINUA",
                "image": "images/samsung.jpg",
                "desc": "Samsung – тұрмыстық үлгі.",
                "article": "SAM-AR12",
                "power": "2100W",
                "size": "43 м²",
                "extra": "Таймер, авто-тазалау"
            },
            {
                "name": "Samsung AR09TXHAQSINUA",
                "image": "images/samsung2.png",
                "desc": "Samsung – кеңсе үшін.",
                "article": "SAM-AR09",
                "power": "2500W",
                "size": "28 м²",
                "extra": "Wi-Fi басқару"
            },
            {
                "name": "Samsung ARO9BSFAMWKNER",
                "image": "images/samsung3.jpg",
                "desc": "Samsung – үнемді үлгі.",
                "article": "SAM-ARO9BS",
                "power": "1700W",
                "size": "18 м²",
                "extra": "Эко-режим"
            },
            {
                "name": "Samsung AR24BXHQASINUA",
                "image": "images/samsung4.jpg",
                "desc": "Samsung – үнемді үлгі.",
                "article": "SAM-AR24BX",
                "power": "1700W",
                "size": " 84 м²",
                "extra": "Эко-режим"
            },
            {
                "name": "Samsung AR12TXHQSINUA",
                "image": "images/samsung.jpg",
                "desc": "Samsung – қуатты үлгі.",
                "article": "AR12TX",
                "power": "3200W",
                "size": "38 м²",
                "extra": "Инвертор, энергия классы A++"
            }
        ]
    }

    return models_map


def combo_ac(request):  # combo_ac_view орнына
    models_map = make_models_map()
    manufacturers = list(models_map.keys())

    selected_manufacturer = None
    selected_model = None
    selected_models = []

    if request.method == "GET" and not any(key in request.GET for key in ['manufacturer', 'model', 'action']):
        default_manufacturer = "haier"
        default_model_index = 1

        if default_manufacturer in models_map:
            selected_manufacturer = default_manufacturer
            selected_models = models_map[default_manufacturer]
            if len(selected_models) > default_model_index:
                selected_model = selected_models[default_model_index]

    if request.method == "POST":
        if request.POST.get("action") == "clear":
            return redirect(reverse("combo_ac"))

        selected_manufacturer = request.POST.get("manufacturer")
        selected_model_name = request.POST.get("model")

        if selected_manufacturer and selected_manufacturer in models_map:
            selected_models = models_map[selected_manufacturer]

            if selected_model_name:
                for m in selected_models:
                    if m["name"] == selected_model_name:
                        selected_model = m
                        break

    context = {
        "manufacturers": manufacturers,
        "selected_manufacturer": selected_manufacturer,
        "selected_model": selected_model,
        "selected_models": selected_models,
    }

    return render(request, "main/coj.html", context)


def combo_ac_clear(request):  # combo_ac_clear_view орнына
    return redirect(reverse("combo_ac"))

def pract3(request):
    return render(request, "main/coj.html")


from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone


def headd(request):
    return render(request, "main/headd.html")


def shop(request):
    images = [
        {'id': 1, 'name': 'сүйекші', 'image': 'images/1.png'},
        {'id': 2, 'name': 'қалам', 'image': 'images/2.png'},
        {'id': 3, 'name': 'жүректен жүреке', 'image': 'images/3.png'},
        {'id': 4, 'name': 'пластилин', 'image': 'images/4.png'},
        {'id': 5, 'name': 'клеевые точки', 'image': 'images/5.png'},
    ]

    selected_id = request.GET.get('product', '1')
    selected_image = next((img for img in images if str(img['id']) == selected_id), images[0])

    return render(request, 'main/shop.html', {
        'images': images,
        'selected_image': selected_image,
    })


def index(request):
    scale = ''
    distance_cm = ''
    result = ''

    if request.method == "POST":
        if 'calculate' in request.POST:
            scale = request.POST.get("scale", "")
            distance_cm = request.POST.get("distance_cm", "")
            try:
                result_value = float(scale) * float(distance_cm)
                result = f"{result_value}"
            except (ValueError, TypeError):
                result = "Қате енгізу!"
        elif 'clear' in request.POST:
            scale = ''
            distance_cm = ''
            result = ''

    return render(request, "main/index.html", {
        "scale": scale,
        "distance_cm": distance_cm,
        "result": result
    })


def make_models_map():
    models_map = {
        "хобби": [
            {
                "name": "Acron CSH-240B",
                "image": "images/1.png",
                "desc": "Acron кондиционер – қуатты үлгі.",
                "article": "ACR-CSH-240B",
                "power": "2200W",
                "size": "72 м²",
                "extra": "Инвертор, энергия классы A+"
            },

        ],

    }
    return models_map


def combo_ac(request):
    models_map = make_models_map()
    manufacturers = list(models_map.keys())

    selected_manufacturer = None
    selected_model = None
    selected_models = []

    if request.method == "GET" and not any(key in request.GET for key in ['manufacturer', 'model', 'action']):
        default_manufacturer = "haier"
        default_model_index = 1

        if default_manufacturer in models_map:
            selected_manufacturer = default_manufacturer
            selected_models = models_map[default_manufacturer]
            if len(selected_models) > default_model_index:
                selected_model = selected_models[default_model_index]

    if request.method == "POST":
        if request.POST.get("action") == "clear":
            return redirect(reverse("combo_ac"))

        selected_manufacturer = request.POST.get("manufacturer")
        selected_model_name = request.POST.get("model")

        if selected_manufacturer and selected_manufacturer in models_map:
            selected_models = models_map[selected_manufacturer]

            if selected_model_name:
                for m in selected_models:
                    if m["name"] == selected_model_name:
                        selected_model = m
                        break

    context = {
        "manufacturers": manufacturers,
        "selected_manufacturer": selected_manufacturer,
        "selected_model": selected_model,
        "selected_models": selected_models,
    }

    return render(request, "main/coj.html", context)


def combo_ac_clear(request):
    return redirect(reverse("combo_ac"))


def pract3(request):
    return render(request, "main/coj.html")


def exchange(request):
    # Валюта бағамы
    exchange_rates = {
        'USD': {'buy': 484.5, 'sell': 486.5},
        'EUR': {'buy': 531.5, 'sell': 535.5},
        'RUB': {'buy': 4.99, 'sell': 5.09},
        'KGS': {'buy': 5.41, 'sell': 5.81},
        'GBP': {'buy': 633.0, 'sell': 653.0},
    }

    if 'history' not in request.session:
        request.session['history'] = []

    result = None
    profit = None
    error = None
    amount = None
    currency = None
    operation = None
    operation_name = None
    clear_pressed = False
    show_total_profit = False
    total_profit = sum(item['profit'] for item in request.session.get('history', []))

    if request.method == 'POST':
        if 'clear' in request.POST:
            # Тазалау әрқашан жұмыс істеуі керек
            request.session['history'] = []
            request.session.modified = True
            clear_pressed = True
            currency = None
            operation = None
            amount = None
            show_total_profit = False

            return redirect('exchange')

        elif 'calculate' in request.POST:
            currency = request.POST.get('currency')
            amount_str = request.POST.get('amount', '0').strip()
            operation = request.POST.get('operation')

            if not operation:
                error = "Әрекетті таңдаңыз"
            elif not currency:
                error = "Валютаны таңдаңыз"
            else:
                operation_name = 'Сатып алу' if operation == 'buy' else 'Сату'

                if not amount_str:
                    error = "Соманы енгізіңіз"
                else:
                    try:
                        amount = int(amount_str)
                        if amount <= 0:
                            error = "Сома оң сан болуы керек"
                        else:
                            rate = exchange_rates[currency]

                            if operation == 'buy':
                                result = amount * rate['buy']
                                profit = (rate['sell'] - rate['buy']) * amount
                            else:
                                result = amount * rate['sell']
                                profit = (rate['sell'] - rate['buy']) * amount

                            history_entry = {
                                'currency': currency,
                                'amount': amount,
                                'operation': operation,
                                'result': round(result, 2),
                                'profit': round(profit, 2),
                            }

                            request.session['history'] = [history_entry] + request.session['history'][:9]
                            request.session.modified = True
                            total_profit = sum(item['profit'] for item in request.session['history'])

                    except ValueError:
                        error = "Сома он сан болуы керек"

        elif 'show_profit' in request.POST:
            show_total_profit = True

    context = {
        'currencies': [
            ('USD', 'USD $'),
            ('EUR', 'EUR €'),
            ('RUB', 'RUB ₽'),
            ('KGS', 'KGS с'),
            ('GBP', 'GBP £'),
        ],
        'result': round(result, 2) if result else None,
        'profit': round(profit, 2) if profit else None,
        'error': error,
        'history': request.session.get('history', []),
        'exchange_rates': exchange_rates,
        'operation_name': operation_name,
        'amount': amount,
        'currency': currency,
        'operation': operation,
        'clear_pressed': clear_pressed,
        'show_total_profit': show_total_profit,
        'total_profit': round(total_profit, 2),
    }

    return render(request, 'main/exchange.html', context)


def history_view(request):

    history = request.session.get('history', [])


    total_profit = sum(item['profit'] for item in history)

    context = {
        'history': history,
        'total_profit': round(total_profit, 2)
    }
    return render(request, 'main/history.html', context)





def Pars_valute(country):
    URL = 'https://nationalbank.kz/ru/exchangerates/ezhednevnye-oficialnye-rynochnye-kursy-valyut'
    data = requests.get(URL)
    sorpa = bs4.BeautifulSoup(data.text, "html.parser")
    items = sorpa.select("td")
    tds = []
    for item in items:
        tds.append(item.text)
    valute_value = 0
    for td in range(0, len(tds)):
        if tds[td].startswith(country):
            valute_value = tds[td+1]
    return valute_value


def pars(request):
    Dollar = ""
    Euro = ""
    Iyan = ""
    Rubl = ""
    Clear = True
    if request.method == 'POST':
        if 'calculate' in request.POST:
            Dollar = Pars_valute('USD')
            Euro = Pars_valute('EUR')
            Iyan = Pars_valute('CNY')
            Rubl = Pars_valute('RUB')
        elif 'clear' in request.POST:
            Clear = False
    return render(request, 'main/pars.html', {
        'dollar': Dollar,
        'euro': Euro,
        'rubl': Rubl,
        'iyan': Iyan,
    })




NORWAY_CITIES = [
    "Oslo", "Bergen", "Trondheim", "Stavanger", "Drammen", "Fredrikstad",
    "Kristiansand", "Sandnes", "Tromsø", "Sarpsborg", "Skien", "Ålesund",
    "Sandefjord", "Haugesund", "Tønsberg", "Moss", "Porsgrunn", "Bodø",
    "Arendal", "Hamar"
]

API_KEY = "3f60c0aaa5da2a27c618036e814f88c6"
Prognozes = []
Kol = 0

def tempp(request):
    global Prognozes, Kol
    summary = ""
    city = ""

    if request.method == 'POST':
        if 'clear' in request.POST:
            Prognozes = []
            Kol = 0
            summary = "Деректер тазартылды!"

        elif 'run' in request.POST or 'task' in request.POST:
            Prognozes = []
            Kol = 0
            cold_cloudy_count = 0

            for city_name in NORWAY_CITIES:
                Kol += 1
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid={API_KEY}"
                try:
                    data = requests.get(url).json()
                    if data.get("cod") != 200:
                        temp = desc = wind = pressure = humidity = country = "-"
                        cold_cloudy = False
                    else:
                        temp = round(data['main']['temp'], 1)
                        country = data['sys']['country']
                        desc = data['weather'][0]['description']
                        wind = data['wind']['speed']
                        pressure = data['main']['pressure']
                        humidity = data['main']['humidity']


                        cloudy_keywords = ["cloud", "overcast", "fog", "mist"]
                        is_cloudy = any(k in desc.lower() for k in cloudy_keywords)
                        cold_cloudy = (temp < 0) and is_cloudy
                        if cold_cloudy:
                            cold_cloudy_count += 1
                except:
                    temp = desc = wind = pressure = humidity = country = "Қате"
                    cold_cloudy = False

                if 'task' in request.POST and not cold_cloudy:
                    continue

                Prognozes.append({
                    'nomer': Kol,
                    'city': city_name,
                    'country': country,
                    'temp': temp,
                    'desc': desc.capitalize(),
                    'wind': wind,
                    'pressure': pressure,
                    'humidity': humidity,
                    'cold_cloudy': cold_cloudy
                })
                if 'task' in request.POST:
                    for i, item in enumerate(Prognozes, start=1):
                        item['nomer'] = i

            if 'task' in request.POST:
                summary = f"Тапсырма бойынша: Температура 0°C төмен және күн бұлтты: {cold_cloudy_count} қала"
            else:
                summary = f"Барлық қалалар: Температура 0°C төмен және күн бұлтты: {cold_cloudy_count} қала"

    return render(request, 'main/temp.html', {
        'prognozes': Prognozes,
        'city': city,
        'summary': summary
    })




def run_parser_planshety():
    BASE_URL = "https://www.sulpak.kz"
    URL = "https://www.sulpak.kz/f/planshetiy"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    session = requests.Session()
    session.headers.update(HEADERS)
    session.cookies.update({'current_region': '750000000', 'current_city': 'almaty'})

    all_data = []
    try:
        response = session.get(URL, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        products = soup.find_all("div", class_="product__item")

        for product in products:
            try:

                name = product.find("div", class_="product__item-name").get_text(strip=True)


                brand = "—"
                for b in ["Samsung", "Apple", "Xiaomi", "Lenovo", "Huawei", "Asus", "Honor"]:
                    if b.lower() in name.lower():
                        brand = b
                        break


                article = "—"
                patterns = [r'[A-Z]{1,2}\d+[A-Z]+[A-Z0-9]*', r'\d{2}[A-Z]{2,}\d+[A-Z]*']
                for p in patterns:
                    match = re.findall(p, name.upper())
                    if match:
                        article = match[0]
                        break




                kod_tovara = product.get("data-code") or "—"


                if not kod_tovara or kod_tovara == "—":
                    parent_with_code = product.find_parent(lambda tag: tag.get("data-code"))
                    if parent_with_code:
                        kod_tovara = parent_with_code.get("data-code") or "—"


                if not kod_tovara or kod_tovara == "—":
                    compare_btn = product.find("button", class_=lambda x: x and "compare" in x.lower() if x else False)
                    if compare_btn:
                        kod_tovara = compare_btn.get("data-code") or "—"


                img_tag = product.find("img")
                img_url = "—"
                if img_tag:
                    img_src = img_tag.get("data-src") or img_tag.get("src")
                    if img_src:
                        if img_src.startswith("//"):
                            img_url = "https:" + img_src
                        elif img_src.startswith("/"):
                            img_url = BASE_URL + img_src
                        else:
                            img_url = img_src


                link_tag = product.find("a", href=True)
                product_url = BASE_URL + link_tag["href"] if link_tag and link_tag.get("href") else "—"

                all_data.append({
                    "Ati": name,
                    "brend": brand,
                    "artikul": article,
                    "kod_tovara": kod_tovara,
                    "kartinka": img_url,
                    "ssylka_na_tovar": product_url
                })

                print(f"Найден товар: {name} | Код: {kod_tovara}")

            except Exception as e:
                print("Ошибка при обработке товара:", e)
                continue

        return all_data

    except Exception as e:
        print("Ошибка при парсинге:", e)
        return []


def planshety_parser_view(request):
    products_data = []
    error_message = None

    if request.method == "POST":
        if 'parse' in request.POST:
            try:
                products_data = run_parser_planshety()
                if not products_data:
                    error_message = "Не удалось получить данные (возможно, сайт изменился или интернет медленный)."
            except Exception as e:
                error_message = f"Ошибка: {str(e)}"

        elif 'download' in request.POST:
            try:
                products_data = run_parser_planshety()
                if products_data:

                    df = pd.DataFrame(products_data, columns=[
                        "Ati", "brend", "artikul", "kod_tovara", "kartinka"
                    ])
                    filename = "sulpak_planshety.xlsx"
                    df.to_excel(filename, index=False, engine='openpyxl')

                    with open(filename, "rb") as f:
                        response = HttpResponse(
                            f.read(),
                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                        response["Content-Disposition"] = f"attachment; filename={filename}"
                        return response
                else:
                    error_message = "Нет данных для Excel файла."
            except Exception as e:
                error_message = f"Ошибка при создании файла: {str(e)}"

    return render(request, "main/export.html", {
        "products": products_data,
        "error_message": error_message,
        "total_products": len(products_data)
    })



def aud6(request):
    numbers = []
    negative_numbers = []
    negative_count = 0
    saved = False

    step = request.session.get('aud6_step', 1)

    if request.method == 'GET' and 'reset' in request.GET:
        request.session['aud6_step'] = 1
        if 'aud6_numbers' in request.session:
            del request.session['aud6_numbers']
        return redirect('/')

    if request.method == 'POST':
        if request.FILES.get('file') and step == 1:
            uploaded_file = request.FILES['file']
            content = uploaded_file.read().decode('utf-8')

            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            input_path = os.path.join(project_root, 'input.txt')

            with open(input_path, 'w', encoding='utf-8') as f:
                f.write(content)

            numbers = [line.strip() for line in content.splitlines() if line.strip()]
            request.session['aud6_numbers'] = numbers

            step = 2

        elif 'show_spring_dates' in request.POST and step == 2:
            try:
                project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                input_path = os.path.join(project_root, 'input.txt')

                with open(input_path, 'r', encoding='utf-8') as f:
                    lines = [line.strip() for line in f if line.strip()]

                negative_numbers = []
                for line in lines:
                    try:
                        num = float(line)
                        if num % 2 == 0 and num < 0:
                            negative_numbers.append(line)
                    except ValueError:
                        continue

                negative_count = len(negative_numbers)
                step = 3


                request.session['aud6_negative_numbers'] = negative_numbers
                request.session['aud6_negative_count'] = negative_count

            except FileNotFoundError:
                numbers = ["input.txt файлы табылмады! Файлды жүктеуді қайталаңыз."]


        elif 'save_file' in request.POST and step == 3:
            try:
                project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                input_path = os.path.join(project_root, 'input.txt')

                with open(input_path, 'r', encoding='utf-8') as f:
                    lines = [line.strip() for line in f if line.strip()]

                negative_numbers = request.session.get('aud6_negative_numbers', [])
                negative_count = request.session.get('aud6_negative_count', 0)

                content_lines = []
                content_lines.append("Файлдан оқылған сандар:")
                content_lines.extend(lines)
                content_lines.append("")
                content_lines.append("Теріс сандар:")
                content_lines.extend(negative_numbers)
                content_lines.append("")
                content_lines.append(f"Теріс сандардың жалпы саны: {negative_count}")

                content = "\n".join(content_lines)

                output_path = r"C:\Users\lenov\PycharmProjects\output.txt"
                with open(output_path, 'w', encoding='utf-8') as out_file:
                    out_file.write(content)

                saved = True


                step = 1
                numbers = []
                negative_numbers = []
                negative_count = 0

            except FileNotFoundError:
                numbers = ["input.txt файлы табылмады! Файлды жүктеуді қайталаңыз."]
            except Exception as e:
                numbers = [f"Қате: {str(e)}"]


    request.session['aud6_step'] = step

    if not numbers and step >= 2:
        numbers = request.session.get('aud6_numbers', [])
    if not negative_numbers and step >= 3:
        negative_numbers = request.session.get('aud6_negative_numbers', [])
        negative_count = request.session.get('aud6_negative_count', 0)

    context = {
        "dates": numbers,
        "spring_dates": negative_numbers,
        "negative_count": negative_count,
        "saved": saved,
        "step": step,
    }
    return render(request, "main/aud6.html", context)







def aud7(request):
    brands = ["Samsung", "LG", "Sony", "Xiaomi", "Haier"]
    types = ["LED", "OLED", "QLED", "LCD"]
    colors = ["Black", "Grey", "Silver"]

    rows = request.session.get("aud7_rows", [])
    errors = []

    if request.method == "POST":
        if "add_row" in request.POST:
            brand = request.POST.get("brand")
            type_ = request.POST.get("type")
            height = request.POST.get("height")
            color = request.POST.get("color")
            price = request.POST.get("price")

            if not (brand and type_ and height and color and price):
                errors.append("Барлық мәліметтерді таңдаңыз!")
            else:
                try:
                    h_val = int(height)
                    p_val = float(price)
                    rows.append({
                        "no": len(rows) + 1,
                        "brand": brand,
                        "type": type_,
                        "height": h_val,
                        "color": color,
                        "price": p_val,
                    })
                    request.session["aud7_rows"] = rows
                except:
                    errors.append("Сан енгізіңіз!")

        elif "clear_all" in request.POST:
            rows = []
            request.session["aud7_rows"] = []


        elif "filter" in request.POST:
            selected_brand = request.POST.get("type")
            if selected_brand:
                request.session["selected_brand"] = selected_brand
                return redirect("aud7_result")
            else:
                errors.append("Тапсырма үшін бренд таңдаңыз!")

    return render(request, "main/aud7.html", {
        "brands": brands,
        "types": types,
        "colors": colors,
        "rows": rows,
        "errors": errors
    })


def aud7_result(request):
    rows = request.session.get("aud7_rows", [])


    selected_brand = request.session.get("selected_brand", "")


    filtered_tv = [
        r for r in rows
        if r["type"] == selected_brand
    ]

    if request.method == "POST":
        if "clear" in request.POST:
            filtered_tv = []
        elif "exit" in request.POST:
            return redirect("aud7")

    return render(request, "main/aud7_result.html", {
        "filtered_tv": filtered_tv,
        "selected_brand": selected_brand,
    })


def aud7_tapsyrma(request):
    return render(request, "main/aud7_tapsyrma.html")


##################################################################################################################
# main/views.py - ТОЛЫҚ ДҰРЫС НҰСҚА
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Prefetch
from .forms import RegisterForm, AdForm
from .models import Ad, AdImage, Category, City, User


# Басты бет
def headd(request):
    return render(request, 'main/headd.html')


# Тіркелу
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Қош келдіңіз! Тіркелу сәтті өтті.")
            return redirect('all_ads')
    else:
        form = RegisterForm()
    return render(request, 'main/auth/register.html', {'form': form})


# Шығу
def logout_view(request):
    auth_logout(request)

    return redirect('login')


# Профиль
@login_required
def profile(request):
    user_ads_count = Ad.objects.filter(user=request.user).count()
    sold_ads_count = Ad.objects.filter(user=request.user, is_moderated=True).count()
    total_views = Ad.objects.filter(user=request.user).aggregate(total=Sum('views'))['total'] or 0

    context = {
        'user': request.user,
        'user_ads_count': user_ads_count,
        'sold_ads_count': sold_ads_count,
        'total_views': total_views,
    }
    return render(request, 'main/profile.html', context)


# Профиль өңдеу
@login_required
def edit_profile(request):
    if request.method == 'POST':
        # Деректерді жаңарту
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.phone = request.POST.get('phone', '')
        request.user.company_name = request.POST.get('company_name', '')

        # Қала
        city_id = request.POST.get('city')
        if city_id:
            request.user.city_id = city_id

        # Аватар
        if request.FILES.get('avatar'):
            request.user.avatar = request.FILES['avatar']

        request.user.save()
        messages.success(request, "✅ Профиль сәтті жаңартылды!")
        return redirect('profile')  # ← ПРОФИЛЬГЕ ҚАЙТАРУ!

    # GET - форманы көрсету
    cities = City.objects.all()
    context = {
        'cities': cities,
    }
    return render(request, 'main/edit_profile.html', context)


# views.py - қос
@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')

        if request.user.check_password(old_password):
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, "Құпия сөз өзгертілді!")
            return redirect('profile')
        else:
            messages.error(request, "Ескі құпия сөз қате!")

    return render(request, 'main/change_password.html')


# views.py - қос
@login_required
def analytics(request):
    if not request.user.is_director():
        messages.error(request, "Сізде рұқсат жоқ!")
        return redirect('headd')

    # СТАТИСТИКА
    total_ads = Ad.objects.count()
    total_users = User.objects.count()
    pending_ads = Ad.objects.filter(is_moderated=False).count()
    approved_ads = Ad.objects.filter(is_moderated=True).count()

    # ҚАЛАЛАР БОЙЫНША
    city_stats = Ad.objects.values('city__name').annotate(count=Count('id')).order_by('-count')

    # КАТЕГОРИЯЛАР БОЙЫНША
    category_stats = Ad.objects.values('category__name').annotate(count=Count('id')).order_by('-count')

    context = {
        'total_ads': total_ads,
        'total_users': total_users,
        'pending_ads': pending_ads,
        'approved_ads': approved_ads,
        'city_stats': city_stats,
        'category_stats': category_stats,
    }
    return render(request, 'main/analytics.html', context)


# Профиль жаңарту
@login_required
def profile_update(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        company_name = request.POST.get('company_name')
        address = request.POST.get('address')

        request.user.phone = phone
        request.user.company_name = company_name
        request.user.address = address

        if 'avatar' in request.FILES:
            request.user.avatar = request.FILES['avatar']

        request.user.save()
        messages.success(request, "Профиль сәтті жаңартылды!")
        return redirect('profile')#-date_joined

    return render(request, 'main/auth/profile_update.html')


@login_required
def manage_users(request):
    if not request.user.is_admin_user():
        messages.error(request, "Тек әкімшіге рұқсат!")
        return redirect('headd')

    users = User.objects.all().order_by('id')

    context = {
        'users': users,
    }
    return render(request, 'main/manage_users.html', context)


@login_required
def change_user_role(request, user_id):
    if not request.user.is_admin_user():
        messages.error(request, "Тек әкімшіге рұқсат!")
        return redirect('headd')

    if request.method == 'POST':
        user = User.objects.get(id=user_id)
        new_role = request.POST.get('role')

        if new_role in ['user', 'director', 'admin']:
            user.role = new_role
            user.save()
            messages.success(request, f"{user.username} рөлі өзгертілді!")

    return redirect('manage_users')


@login_required
def delete_user(request, user_id):
    if not request.user.is_admin_user():
        messages.error(request, "Тек әкімшіге рұқсат!")
        return redirect('headd')

    user = User.objects.get(id=user_id)

    if user == request.user:
        messages.error(request, "Өзіңізді өшіре алмайсыз!")
        return redirect('manage_users')

    # Растау үшін session қолдану
    confirm_key = f'confirm_delete_{user_id}'

    if request.session.get(confirm_key):
        # Екінші рет басқан - өшіру
        user.delete()
        messages.success(request, f"{user.username} өшірілді!")
        del request.session[confirm_key]
    else:
        # Бірінші рет - растау
        request.session[confirm_key] = True
        messages.warning(request, f"{user.username} өшіру үшін қайта басыңыз!")

    return redirect('manage_users')


# ========== OLX ФУНКЦИЯЛАРЫ ==========
def all_ads(request):
    ads = Ad.objects.filter(is_moderated=True)

    # ІЗДЕУ (search query)
    search_query = request.GET.get('search', '')
    if search_query:
        ads = ads.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # КАТЕГОРИЯ бойынша фильтр
    category_id = request.GET.get('category', '')
    if category_id:
        ads = ads.filter(category_id=category_id)

    # ҚАЛА бойынша фильтр
    city_id = request.GET.get('city', '')
    if city_id:
        ads = ads.filter(city_id=city_id)

    # Соңғылары бірінші
    ads = ads.order_by('-created_at')

    categories = Category.objects.all()
    cities = City.objects.all()

    context = {
        'ads': ads,
        'categories': categories,
        'cities': cities,
        'search_query': search_query,
        'selected_category': category_id,
        'selected_city': city_id,
    }
    return render(request, 'main/olx/all_ads.html', context)


# Жарнама толық (КІРУ КЕРЕК ЕМЕС!)
def ad_detail(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)

    if not ad.is_moderated and (not request.user.is_authenticated or ad.user != request.user):
        messages.error(request, "Бұл жарнама әлі модерациядан өтпеген!")
        return redirect('all_ads')

    # Көрулер санын арттыру (тек кірген адамдар үшін, өзінікін санамайды)
    if request.user.is_authenticated and request.user != ad.user:
        ad.views += 1
        ad.save()

    back_url = request.META.get('HTTP_REFERER', '/')

    context = {
        'ad': ad,
        'back_url': back_url,
    }
    return render(request, 'main/olx/ad_detail.html', context)


# Жарнама қосу
@login_required
def create_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            images = request.FILES.getlist('images')
            for img in images[:5]:
                AdImage.objects.create(ad=ad, image=img)
            messages.success(request, "Жарнама жарияланды! Модерациядан өткенше күте тұрыңыз.")
            return redirect('my_ads')
    else:
        form = AdForm()

    context = {
        'form': form,
        'categories': Category.objects.all(),
        'cities': City.objects.all(),
    }
    return render(request, 'main/olx/create_ad.html', context)


# Менің жарнамаларым
@login_required
def my_ads(request):
    ads = Ad.objects.filter(user=request.user).prefetch_related(
        Prefetch('images', queryset=AdImage.objects.only('image'))
    ).order_by('-created_at')
    return render(request, 'main/olx/my_ads.html', {'ads': ads})


# Модерация
@login_required
def moderate_ads(request):
    if not (request.user.role == 'director' or request.user.role == 'admin'):
        messages.error(request, "Сізде рұқсат жоқ!")
        return redirect('headd')

    ads = Ad.objects.filter(is_moderated=False)
    if request.method == 'POST':
        ad_id = request.POST.get('ad_id')
        action = request.POST.get('action')
        ad = Ad.objects.get(id=ad_id)
        if action == 'approve':
            ad.is_moderated = True
            ad.save()
            messages.success(request, f"Бекітілді: {ad.title}")
        elif action == 'reject':
            ad.delete()
            messages.error(request, f"Өшірілді: {ad.title}")
    return render(request, 'main/olx/moderate.html', {'ads': ads})


# Жарнама өңдеу
@login_required
def edit_ad(request, ad_id):
    ad = Ad.objects.get(id=ad_id, user=request.user)

    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES, instance=ad)
        if form.is_valid():
            form.save()
            images = request.FILES.getlist('images')
            for img in images[:5]:
                AdImage.objects.create(ad=ad, image=img)
            messages.success(request, "Жарнама жаңартылды!")
            return redirect('my_ads')
    else:
        form = AdForm(instance=ad)

    return render(request, 'main/olx/edit_ad.html', {'form': form, 'ad': ad})


# Жарнама жою
@login_required
def delete_ad(request, ad_id):
    ad = Ad.objects.get(id=ad_id, user=request.user)

    if request.method == 'POST':
        ad.delete()
        messages.success(request, f"'{ad.title}' жарнамасы өшірілді!")
        return redirect('my_ads')

    return render(request, 'main/olx/confirm_delete.html', {'ad': ad})