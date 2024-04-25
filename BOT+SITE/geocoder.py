import requests


def get_coords(text, kind=None):
    geocoder_url = "http://geocode-maps.yandex.ru/1.x/"

    params = {
        'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
        'geocode': text,
        'format': 'json'
    }
    if kind is not None:
        params['kind'] = kind
    # Выполняем запрос.
    response = requests.get(geocoder_url, params=params)
    if response:
        # Преобразуем ответ в json-объект
        json_response = response.json()

        # Получаем первый топоним из ответа геокодера.
        # Согласно описанию ответа, он находится по следующему пути:
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        # Полный адрес топонима:
        toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
        # Координаты центра топонима:
        toponym_coodrinates = toponym["Point"]["pos"]
        # Печатаем извлечённые из ответа поля:
        print(toponym_address, "имеет координаты:", toponym_coodrinates)
        return ','.join(toponym_coodrinates.split())
    else:
        print("Ошибка выполнения запроса:")
        print("Http статус:", response.status_code, "(", response.reason, ")")



