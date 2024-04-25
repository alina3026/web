from io import BytesIO

from PIL import Image
import requests

from geocoder import get_coords


def send_Img(adr):


    address_coords = get_coords(adr)

    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

    address_ll = address_coords

    search_params = {
        "apikey": api_key,
        "text": "институт",
        "lang": "ru_RU",
        "ll": address_ll,
        "type": "biz"
    }

    response = requests.get(search_api_server, params=search_params)
    if not response:
        print('problems...')

    # Преобразуем ответ в json-объект
    json_response = response.json()

    # Получаем первую найденную организацию.
    organization = json_response["features"][0]
    # Название организации.
    org_name = organization["properties"]["CompanyMetaData"]["name"]
    # Адрес организации.
    org_address = organization["properties"]["CompanyMetaData"]["address"]

    # Получаем координаты ответа.
    point = organization["geometry"]["coordinates"]
    org_point = "{0},{1}".format(point[0], point[1])
    delta = "0.001"

    # Собираем параметры для запроса к StaticMapsAPI:
    map_params = {
        # позиционируем карту центром на наш исходный адрес
        "ll": address_ll,
        "spn": ",".join([delta, delta]),
        "l": "map",
        # добавим точку, чтобы указать найденную аптеку
        "pt": '~'.join([f"{org_point},pm2dbl",
                        f"{address_coords},pm2dgl"])
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    # ... и выполняем запрос
    response = requests.get(map_api_server, params=map_params)
    img = BytesIO(response.content).read()
    return img
    # print(BytesIO(response.content).read())

    # Image.open(BytesIO(
    #     response.content)).show()
