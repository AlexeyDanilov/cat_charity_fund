О проекте
```
Проект QRKot предназначен для сбора пожертвований
для благотворительного фонла на помощь котикам.
API и краткая докуентация для возможности интеграции с другими приложениями
доступны по адресу: http://127.0.0.1:8000/docs
```


**Как развернуть**

Клонировать репозиторий и перейти в него в командной строке:

```
git clone 
```

```
cd cat_charity_fund
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Применить миграции:

```
alembic upgrade head
```

Запустить проект на локальном сервере:

```
uvicorn app.main:app --reload
```

**Автор:** [Алексей Данилов](https://github.com/AlexeyDanilov/)

Проект доступен [по ссылке](https://github.com/AlexeyDanilov/cat_charity_fund)
