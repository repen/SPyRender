### Описание проекта 

Рендер динамических страниц. (Selenium + Chrome)


1. Создать рендер запросом.

```
import requests

url = "http://0.0.0.0:5000/render"

payload={
	'url': 'https://realty.yandex.ru/tyumenskaya_oblast/kupit/kvartira/odnokomnatnaya/',
	'jscript': 'document.querySelector("body");console.log("test")',
	'wait': '1'
}

response = requests.request("POST", url, data=payload)

print(response.json())

```

Ответ с токеном

```
{
    "data": [
        "576803713daa46e6b0a1e5a57cd2feba"
    ],
    "response": true
}
```

2. Забрать результат (html) через токен:

```
import requests

url = "http://0.0.0.0:5000/result/576803713daa46e6b0a1e5a57cd2feba"

response = requests.request("GET", url)

print(response.json())
```

3. Получать обновление со страницы. 
Запрос возвращает html текущей активной вкладки браузера. Возможно выполнять произвольный javascript код.

```
import requests

url = "http://0.0.0.0:5000/a_content"

payload={'jscript': 'setTimeout(()=>{console.log("test");}, 300);'}

response = requests.request("POST", url, data=payload)

print(response.json())
```

### Запуск

- запуск в обычном режиме

`python main.py`

- запуск в безголовом режиме

`python main.py -head or python main.py --headless`