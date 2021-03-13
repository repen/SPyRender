### Описание проекта 

Минимальный набор для создания различных скриптов на Python.


пример запроса с js кодом
document.querySelector("#a-match-head-2-head").click()

http://0.0.0.0:5000/page?url=https://www.flashscore.ru/match/4IYBxbu7/#match-summary&jscript=document.querySelector("#a-match-head-2-head").click()


http://0.0.0.0:5000/page


id: str
url: str
param: dict
expiration_date: int
wait: float = 1.1
jscript: str = ""


запуск в обычном режиме
python main.py

запуск в безголовом режиме
python main.py -head or python main.py --headless