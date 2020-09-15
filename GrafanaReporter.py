import requests
from datetime import datetime
from urllib import parse
from os import path
from os import mkdir

dir = 'result'
if not path.exists(dir) or not path.isdir(dir):
    mkdir(dir)


def parcingDate(timeToParse: str):
    """
    Функция парсит полученную дату формата ДД.ММ.ГГГГ ЧЧ:ММ в удобочитаемую для Grafana Дату
    :param timeToParse: возвращает дату вопринимаемую Grafana для отправки запроса
    :return:
    """
    return str(int(datetime.strptime(timeToParse, '%d.%m.%Y %H:%M').timestamp() * 1000))


def getUrl(url: str, timeStart: str, timeEnd: str, **kwargs):
    """
    Функция парсит полученный url и изменяет в ней передаваемые параметры в запросе
    :param url: url в котором необходимо изменить определенные параметры
    :param width: длинна необходимой для получения картинки
    :param height: высота необходимой для получения картинки
    :param kwargs: дополнительные парметры необходимые для изменения или добавления в запрос
    :return: возвращает измененный url с добавленными параметрами
    """
    urlStr: parse.ParseResult = parse.urlparse(url)
    urlDict = parse.parse_qs(urlStr.query)

    urlDict['theme'] = ['light']
    urlDict['from'] = [parcingDate(timeStart)]
    urlDict['to'] = [parcingDate(timeEnd)]
    for k, v in kwargs.items():
        urlDict[k] = [v]

    urlStr = urlStr._replace(query=parse.urlencode(urlDict, doseq=True))

    return urlStr.geturl()


def getFile(urlForFile, fileName: str):
    """
    Функция скачивает с Grafana срендереный файл в png формате
    :param urlForFile: url до файла который необходимо скачать
    :param fileName: наименование файла в который необходимо записать изображение
    :return:
    """
    response = requests.get(urlForFile, headers={'Authorization': 'Bearer ' + config.TOKEN})
    if response.status_code == 200:
        with open(
                path.join(dir, fileName if fileName.endswith('.png')
                else f'{fileName}.png'), 'wb') as f:
            f.write(response.content)
            f.seek(0)
    else:
        print("Чтот то пошло не так с графиком: response code: " + str(response.status_code))


if __name__ == '__main__':
    import ConfigApp as config

    for test in config.tests:
        print(test['name'])

        for graf in config.graphics:
            count = 0
            for url in config.graphics[graf]:
                urlToFile = getUrl(url=url, timeStart=test['timeStart'], timeEnd=test['timeEnd'])
                print(urlToFile)
                getFile(urlToFile,
                        f'{test["name"]}{graf}{count}from{parcingDate(test["timeStart"])}to{parcingDate(test["timeEnd"])}')
                count += 1
