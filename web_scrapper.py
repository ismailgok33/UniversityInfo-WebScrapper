from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import re


def cityToCode(cityName):
    switcher = {
        "İSTANBUL": "1",
        "ANKARA": "2",
        "İZMİR": "3",
        "ADANA": "4",
        "ADIYAMAN": "5",
        "AFYONKARAHİSAR": "6",
        "AĞRI": "7",
        "AKSARAY": "8",
        "AMASYA": "9",
        "ANTALYA": "10",
        "ARDAHAN": "11",
        "ARTVİN": "12",
        "AYDIN": "13",
        "BALIKESİR": "14",
        "BARTIN": "15",
        "BATMAN": "16",
        "BAYBURT": "17",
        "BİLECİK": "18",
        "BİNGÖL": "19",
        "BİTLİS": "20",
        "BOLU": "21",
        "BURDUR": "22",
        "BURSA": "23",
        "ÇANAKKALE": "24",
        "ÇANKIRI": "25",
        "ÇORUM": "26",
        "DENİZLİ": "27",
        "DİYARBAKIR": "28",
        "DÜZCE": "29",
        "EDİRNE": "30",
        "ELAZIĞ": "31",
        "ERZİNCAN": "32",
        "ERZURUM": "33",
        "ESKİŞEHİR": "34",
        "GAZİANTEP": "35",
        "GİRESUN": "36",
        "GÜMÜŞHANE": "37",
        "HAKKARİ": "38",
        "HATAY": "39",
        "IĞDIR": "40",
        "ISPARTA": "41",
        "KAHRAMANMARAŞ": "42",
        "KARABÜK": "43",
        "KARAMAN": "44",
        "KARS": "45",
        "KASTAMONU": "46",
        "KAYSERİ": "47",
        "KİLİS": "48",
        "KIRIKKALE": "49",
        "KIRKLARELİ": "50",
        "KIRŞEHİR": "51",
        "KOCAELİ": "52",
        "KONYA": "53",
        "KÜTAHYA": "54",
        "MALATYA": "55",
        "MANİSA": "56",
        "MARDİN": "57",
        "MERSİN": "58",
        "MUĞLA": "59",
        "MUŞ": "60",
        "NEVŞEHİR": "61",
        "NİĞDE": "62",
        "ORDU": "63",
        "OSMANİYE": "64",
        "RİZE": "65",
        "SAKARYA": "66",
        "SAMSUN": "67",
        "ŞANLIURFA": "68",
        "SİİRT": "69",
        "SİNOP": "70",
        "SİVAS": "71",
        "ŞIRNAK": "72",
        "TEKİRDAĞ": "73",
        "TOKAT": "74",
        "TRABZON": "75",
        "TUNCELİ": "76",
        "UŞAK": "77",
        "VAN": "78",
        "YALOVA": "79",
        "YOZGAT": "80",
        "ZONGULDAK": "81",
        "KKTC-GAZİMAĞUSA": "82",
        "KKTC-LEFKOŞA": "83",
        "BAKÜ-AZERBAYCAN": "84",
        "KKTC-GİRNE": "85",
        "TÜRKİSTAN-KAZAKİSTAN": "86",
        "KKTC-GÜZELYURT": "87",
        "BİŞKEK-KIRGIZİSTAN": "88",
        "KOMRAT-MOLDOVA": "89",
        "KKTC-LEFKE": "90",
        "ÜSKÜP-MAKEDONYA": "91",
    }
    return switcher.get(cityName, "0")


f = open("university-data.txt", "a")

mainUrl = 'https://www.basarisiralamalari.com/universite-taban-puanlari-2020-ve-basari-siralamalari-osym/'
# Opens up the connection and gets the html page from it
uClient = uReq(mainUrl)
pageHtml = uClient.read()

# Closes the connection
uClient.close()

pageSoup = soup(pageHtml.decode('utf-8', 'ignore'), 'html.parser')

uniTable = pageSoup.find('table', {'id': 'basaritable'})
wholeTbody = uniTable.tbody
allRows = wholeTbody.findAll('tr')

allURLs = []

for row in allRows:
    if row.find('tr', attrs={'style': 'height: 46px;'}):
        continue
    cells = row.findAll('td')
    for cell in cells:
        href = cell.find('a')
        if href is None:
            continue
        allURLs.append(str(href.get('href')))

index = 1

for url in allURLs:
    # Opens up the connection and gets the html page from it
    uClient = uReq(url)
    pageHtml = uClient.read()

    # Closes the connection
    uClient.close()

    pageSoup = soup(pageHtml.decode('utf-8', 'ignore'), 'html.parser')

    uniTable = pageSoup.find('table', {'id': 'basaritable'})
    if uniTable is None:
        uniTable = pageSoup.find('table', {'id': 'universitego'})
    # tableHeader = uniTable.tbody.tr
    wholeTbody = uniTable.tbody
    allRows = wholeTbody.findAll('tr')

    for row in allRows:
        cells = row.findAll('td')
        if cells[0].text == 'Üniversite Adı':
            continue
        # Gets the University Name from the first column
        uni = cells[0].text.split('(')[0]
        # Gets city and isState values from the first column as well
        city_isState = re.findall(r'\((.*?) *\)', cells[0].text)
        if len(city_isState) < 2:
            city_isState.append('özel')
        f.write('new University( "uni_' + str(index) + '", "' +
                uni + '", "' + cells[1].text + '", "' + cells[4].text + '", "' +
                cells[5].text + '", "' + cells[3].text + '", ' + str(('devlet' in city_isState[1].lower())).lower() +
                ', "' + (cityToCode(city_isState[0]) if cityToCode(city_isState[0]) != '0' else cityToCode(uni.split(' ')[0])) + '", ' +
                ('2' if cells[2].text == "TYT" else '4') + ', "' + cells[2].text + '" ), \n\n')
        index = index + 1

f.close()
print('success')

# test_url = 'https://www.basarisiralamalari.com/altinbas-universitesi-istanbul-2021-taban-puanlari-ve-basari-siralamalari/'
# # test_url = 'https://www.basarisiralamalari.com/zonguldak-bulent-ecevit-universitesi-beun-2021-taban-puanlari-ve-basari-siralamalari/'

# # Opens up the connection and gets the html page from it
# uClient = uReq(test_url)
# pageHtml = uClient.read()

# # Closes the connection
# uClient.close()

# pageSoup = soup(pageHtml.decode('utf-8', 'ignore'), 'html.parser')

# uniTable = pageSoup.find('table', {'id': 'basaritable'})
# tableHeader = uniTable.tbody.tr
# wholeTbody = uniTable.tbody
# allRows = wholeTbody.findAll('tr')

# index = 1
# for row in allRows:
#     cells = row.findAll('td')
#     if cells[0].text == 'Üniversite Adı':
#         continue
#     # Gets the University Name from the first column
#     uni = cells[0].text.split('(')[0]
#     # Gets city and isState values from the first column as well
#     city_isState = re.findall(r'\((.*?) *\)', cells[0].text)
#     print('new University{ id: "uni_' + str(index) + '", "' +
#           uni + '", "' + cells[1].text + '", "' + cells[4].text + '", "' +
#           cells[5].text + '", "' + cells[3].text + '", ' + str(('devlet' in city_isState[1].lower())).lower() +
#           ', "' + (cityToCode(cityToCode(city_isState[0]) if cityToCode(city_isState[0]) != '0' else cityToCode(uni.split(' ')[0]))) + '", ' + ('2' if cells[2].text == "TYT" else '4') + ', "' + cells[2].text + '" }')
#     index = index + 1
