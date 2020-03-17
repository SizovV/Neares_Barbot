import requests
import math
import Config
import data
from transliterate import translit
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

string_ya_api = "https://geocode-maps.yandex.ru/1.x/?apikey={}&geocode=".format(Config.API_YA)

def get_html(url, user_agent=None, timeout=4): #function for get page source
    user_agent = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.136 YaBrowser/20.2.3.213 Yowser/2.5 Safari/537.36"
    r = requests.get(url, headers={'User-Agent': user_agent})
    return r.text


def get_ip(dolgota, shirina):  # send you info about your ip and user_agent
    #crome_path = "chromedriver.exe"
    string_url = "https://yandex.ru/maps/213/moscow/category/pub_bar/filter/open_now/?ll={}%2C{}&sll={}%2C{}&sspn=0.004897%2C0.002205&z=17".format(dolgota, shirina, dolgota, shirina) #search for bars
    try:
        driver = webdriver.Firefox()
        AcCh = webdriver.common.action_chains.ActionChains(driver)
        driver.get(string_url)
        movi = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[4]/div[1]/div[1]/div/div/div[2]/div[2]")
        movin = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[4]/div[1]/div[1]/div/div/div[1]/div/div/div[3]")
        el = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[4]/div[1]/div[1]/div/div/div[1]/div/div/div[2]/div/div[1]/div/div[2]/button/span")
        AcCh.move_to_element(el).click().pause(2).drag_and_drop_by_offset(movi, movin).pause(2).perform()
        i = 0
        while 2*len(strings[stri]) > len(driver.current_url):
            time.sleep(1)
            i+=1
            if i>4:
                AcCh.move_to_element(el).click().perform()
        soup = BeautifulSoup(driver.page_source, 'lxml')
        driver.quit()
    except:
        soup = BeautifulSoup(get_html(string_url), 'lxml')
    bar_res = [[],[],[],[],[],[]] #.text.strip()  # .text.strip() в текст превращает все что и так текст), но надо избавится от окружения
    pannels = soup.find_all('li', class_='search-snippet-view')
    for pann in pannels:
        adres = pann.find('div', class_='search-business-snippet-view__address').text.strip()
        adres_ru = adres
        try:
            int(adres.split()[-1])
            adres = str(adres) + "+Moscva"
        except:
            adres = str(adres)
        adres = translit(adres, 'ru', reversed=True)
        adres = adres.replace(" ", "+").replace("'", "").replace(",", "")
        soup_url = BeautifulSoup(get_html(string_ya_api + adres), 'lxml')
        try:
            koords = soup_url.find("pos").text.split()
            dist = distance(shirina, dolgota, float(koords[1]), float(koords[0]))
        except:
            continue
        if dist > 1900:
            continue
        try:
            raiting = pann.find('span', class_="business-rating-badge-view__rating-text _size_m").text.strip()
        except:
            raiting = "Unknown"
        try:
            name = pann.find('div', class_="search-business-snippet-view__title _with-badge").text#try to find tre name
        except Exception:
            name = pann.find('div', class_ ="search-business-snippet-view__title").text
        except:
            name = "NoName"
        link = pann.find('a', class_="link-wrapper")
        urlka = link.get('href')
        open_or_not = pann.find('div', class_="business-working-status-view__text").text.strip()
        bar_res[5].append(open_or_not)
        bar_res[0].append(adres_ru)
        bar_res[1].append(raiting)
        bar_res[2].append(name)
        bar_res[3].append(urlka)
        bar_res[4].append(dist)
    return bar_res

def get_ip_new(dolgota, shirina):  # send you info about your ip and user_agent
    string_url = "https://yandex.ru/maps/213/moscow/category/pub_bar/?ll={}%2C{}&sll={}%2C{}&sspn=0.004897%2C0.002205&z=17".format(dolgota, shirina, dolgota, shirina)
    print(string_url)
    driver = webdriver.Firefox("/home/Sizov/chromedriver/exe")
    AcCh = ActionChains(driver)
    driver.get(string_url)
    print(driver.page_source)
    movi = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[4]/div[1]/div[1]/div/div/div[2]/div[2]")
    movin = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[4]/div[1]/div[1]/div/div/div[1]/div/div/ul/li[1]")
    el = driver.find_element_by_xpath(
        "/html/body/div[1]/div[2]/div[4]/div[1]/div[1]/div/div/div[1]/div/div/div[2]/div/div[1]/div/div[2]/button/span")
    #action = AcCh.move_to_element(el).click()
    action = action.move_to_element(movi)
    action = action.drag_and_drop(movi, movin)
    action = action.perform()
    time.sleep(10)
    print("wre")
    soup = BeautifulSoup(driver.page_source, 'lxml')
    print("EEEE")
    driver.quit()
    #soup = BeautifulSoup(get_html(string_url), 'lxml')
    bar_res = [[],[],[],[],[],[]] #.text.strip()  # .text.strip() в текст превращает все что и так текст), но надо избавится от окружения
    pannels = soup.find_all('li', class_='search-snippet-view')
    for pann in pannels:
        adres = pann.find('div', class_='search-business-snippet-view__address').text.strip()
        adres_ru = adres
        try:
            int(adres.split()[-1])
            adres = str(adres) + "+Moscva"
        except:
            adres = str(adres)
        adres = translit(adres, 'ru', reversed=True)
        adres = adres.replace(" ", "+").replace("'", "").replace(",", "")
        soup_url = BeautifulSoup(get_html(string_ya_api + adres), 'lxml')
        try:
            koords = soup_url.find("pos").text.split()
            dist = distance(shirina, dolgota, float(koords[1]), float(koords[0]))
        except:
            continue
        if dist > 1900:
            print("dist")
            continue
        raiting = pann.find('span', class_="business-rating-badge-view__rating-text _size_m").text.strip()
        try:
            name = pann.find('div', class_="search-business-snippet-view__title _with-badge").text  # try to find tre name
        except Exception:
            name = pann.find('div', class_="search-business-snippet-view__title").text
        except:
            name = "NoName"
        link = pann.find('a', class_="link-wrapper")
        urlka = link.get('href')
        open_or_not = pann.find('div', class_="business-working-status-view__text").text.strip()
        bar_res[0].append(adres_ru)
        bar_res[2].append(name)
        bar_res[1].append(raiting)
        bar_res[5].append(open_or_not)
        bar_res[3].append(urlka)
        bar_res[4].append(dist)
    return bar_res

def get_name(name, dolgota, shirina):  #add the new object in favorites
    string_url = "https://yandex.ru/maps/213/moscow/search/{}/?ll={}%2C{}".format(translit(name, 'ru', reversed=True), dolgota, shirina)#find him in Ya
    soup = BeautifulSoup(get_html(string_url), 'lxml')
    html=soup.find("a", class_="link-wrapper").get("href")#find url
    soup = BeautifulSoup(get_html("https://yandex.ru" + str(html)), 'lxml')
    adres = soup.find_all('div', class_="orgpage-header-view__contact")[2].find("span").text.strip()
    adres_ru = adres
    try:
        int(adres.split()[-1])# just because in Ya all cities instead of Moscow have city's name in the address
        adres = str(adres) + "+Moscva"
    except:
        adres = str(adres)
    adres = translit(adres, 'ru', reversed=True)
    adres = adres.replace(" ", "+").replace("'", "").replace(",", "")
    soup_url = BeautifulSoup(get_html(string_ya_api + adres), 'lxml')
    koords = soup_url.find("pos").text.split()
    print(koords)
    name = name.split('  ')[0]
    raiting = soup.find('span', class_="business-rating-badge-view__rating-text _size_m").text.strip()
    soup1=soup.find("div", class_="orgpage-info-view__columns")
    try:
        price = soup1.find_all('div', class_="orgpage-info-view__feature")[1].find("div", class_="orgpage-info-view__feature-content").text.strip()
    except:
        price = "ХЗ)"
    upd = (str(name), str(raiting), str(price), str(adres_ru.replace(",", "")), str(html), koords[1], koords[0])
    s="SELECT * FROM bars_fav WHERE (name = %s AND longitude = %s AND latitude = %s) "
    data.mycursor.execute(s, (str(name), koords[1], koords[0]))
    if len(data.mycursor.fetchall())==0:
        sql_formula = "INSERT INTO bars_fav (name, rait, price, adress, url, longitude, latitude) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        data.mycursor.execute(sql_formula, upd)
        data.mydb.commit()
        data.mycursor.execute("SELECT * FROM bars_fav")
        resa = data.mycursor.fetchall()
        for i in resa:
            print(i)
    else:
        upd_str = "UPDATE bars_fav SET name=%s, rait=%s, price=%s, adress=%s, url=%s, longitude=%s, latitude=%s WHERE  (name = '{}' AND longitude = {} AND latitude = {})".format(str(name), koords[1], koords[0])
        data.mycursor.execute(upd_str, upd)
        data.mydb.commit()
        data.mycursor.execute("SELECT * FROM bars_fav")
        resa = data.mycursor.fetchall()
        for i in resa:
            print(i)
    names = []
    names.append(name)
    names.append(str(adres_ru.replace(",", "")))
    return names

def distance(Ash, Ado, Bsh, Bdo): #function that return distance between user and parsed object
    EARTH_RADIUS = 6372795
    pi = 3.141592653589793238462643383279

    lat1 = Ash * pi / 180
    lat2 = Bsh * pi / 180
    long1 = Ado * pi / 180
    long2 = Bdo * pi / 180

    # косинусы и синусы широт и разницы долгот
    cl1 = math.cos(lat1)
    cl2 = math.cos(lat2)
    sl1 = math.sin(lat1)
    sl2 = math.sin(lat2)
    delta = long2 - long1
    cdelta = math.cos(delta)
    sdelta = math.sin(delta)

    # вычисления длины большого круга
    y = math.sqrt(pow(cl2 * sdelta, 2) + pow(cl1 * sl2 - sl1 * cl2 * cdelta, 2))
    x = sl1 * sl2 + cl1 * cl2 * cdelta

    ad = math.atan2(y, x)
    dist = ad * EARTH_RADIUS

    return dist



#dat = ((56.859114, 35.910207), (55.770952, 37.617518), (56.340555, 30.521304), (54.513119, 36.261161), (59.934069, 30.306274))

#print(get_ip_new(dat[2][1], dat[2][0]))

