Задание 11: Что видно из КГО?

У меня не получилось прямо то что нужно, но вот что получилось.

Сайт написан с помощью фреймворка Django.
Пользователь вводит название объекта(звезды) и время (UTC) в которое он хочет наблюдать.
В ответ на его запрос рисуется 2 графика: первый - высота этого объекта над горизонтом в обсерватории КГО в течении года, второй - угловое расстояние до Луны в течении года.

Фаза луны никак не учитывается.

Дополнительно на первом графике отображается параметр - Airmass.

Я не совсем поняла что значит видимость, поэтому решила рисовать высоту, если выше горизонта  - значит видно)

Как эти всем пользоваться: находясь в корневой папке kgo необходимо открыть терминал и там написать: python3 manage.py runserver
Далее необходимо перейти по адресу http://127.0.0.1:8000/

В первое окошко вбивается название звезды на английском
Во второе - время в формате HH:MM:SS

(Вообще говоря там есть placeholder-ы, но они работают только после первого ввода)



