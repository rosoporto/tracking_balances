## Проект "Контроль остатков товара"
Приложение парсит данные с сайта донора (ссылки на требуемуе товары указываются в отдельном файле) и выводит данные по остаткам в Телеграм бот в указанное время (берется из настроек проекта) строго определенным пользователям (так же указывается в настройках кому)
<hr>

### В проекте использованы технологии:
![](https://img.shields.io/badge/language-python-blue)

## Установка
```
git clone https://github.com/rosoporto/tracking_balances.git
cd python-project-49
make package-install
```

## Настройка
1. В папке `data` в файл `example.json` (приложен в качестве примера) вставьте свои данные по сайту донару.
2. В корне проекта создайте файл `.env` и заполните его данными (пример):
```
DATA_FILE_PATH="optima_tg_stock/data/example.json"
TELEGRAM_TOKEN='1234567890:AaBbCcDd...'
TELEGRAM_USER_ID='9876543321'
DAYS_OFF=5,6
RUN_TIME="09:00"
MIN_STOCK_QUANTITY=0 
```
где
```
DATA_FILE_PATH=      #путь до файлы с ссылками из п.1
TELEGRAM_TOKEN=      #токен от телеграм бота
TELEGRAM_USER_ID=    #ID пользователя, кому бот будет отсылать уведомления (свой id можете узнать у [@userinfobot](https://t.me/userinfobot))
DAYS_OFF=            #дни когда бот не будет отсылать вам уведомления: 5 - Saturday, 6 - Sunday
RUN_TIME=            #в какое время присылать уведомления
MIN_STOCK_QUANTITY=  #при достижении этой цифры бот вам сообщить, что остатки меньше указанного числа. 0 - остатки будет присылать по факту
```

## Запуск
```
make load
```

### Цель проекта
Упростить себе работу по дропшиппинг.
Код написан в корыстных целях ;) c использование AI.