Задания по курсу «Научное программирование на языке Python» — 2019/2020


#8 Погода в КГО


"Напишите сервис, который каждый час запрашивает какой-нибудь погодный ресурс о погоде в КГО и сохраняет информацию о текущей погоде и прогнозе.
Это задание может выполняться разными студентами, каждый должен выбрать свой источник данных о погоде"


Програма под названием weath.py - это код, позволяющий получать характеристики погодых условий в определенном месте Земли. Она запрашивает кординаты интересующего Вас места и то, с какой частотой Вы хотите сохранять полученные данные (поминутное, почасовое сохранение). 


Для работы необходимо зарегестрироваться на https://openweathermap.org/ сгенерировать в личном кабинете и сохранить свой API ключ в файл "api_key.txt" в той директории, из которой запускаете основной скрипт weath.py.


Вам нужно запустить weath.py (>>>python weath.py), и по мере запроса программы передать ей следующие параметры:

1) Задайте нужное Вам название csv файла, которое будет иметь сохраняемый в конце файл с записанными данными. Необходимо написать слово или предложение (разделять слова в предложении нижним подчеркиванием).

Например, вводим: hourly_weather_KGO

Получаем в итоге файл в текущей директории с именем: hourly_weather_KGO.csv


2) Координаты КГО или любого другого интересующего Вас места:

43.74611 #(широта КГО) 

42.6675 #(долгота КГО)


3) Режим записи:


Введите или 'minute' ('min' допустимо) или 'hour' по желанию. Этот параметр укажет программе с какой частотой записывать данные в файл.


Приостановка программы прерывает запись параметров погодных условий, доступной в виде csv таблицы. 


Единицы измерения параметров: 


-temperature [Celsius]

-temperature_feel [Celsius]

-pressure [hPa]

-humidity [%]

-clouds [%]

-wind_speed [meter/sec]

-wind_degree [degrees (meteorological)]