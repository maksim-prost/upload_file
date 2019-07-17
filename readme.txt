Приложение состоит из 2 частей:
	Пользовательская (папка upload_file):
		-app 
			-index.html для запуска через браузер
			-package.json настройки приложения для linux64
		-build
			-upload file to server
				-linux64
					-upload file to server для запуска приложением на linux64

	Cервер:
		- requiremets - библиотеки python3 необходимые для работы
		- config.py файл с настройками
		- file_storage папка для хранения загружаемых файлов
		- templates  папка для шаблонов отображения (html)
		- static (скрипты js b стили сss)
		- views.py логика сервера


config настройка flask приложения
__init__ сборка компонентов
search_by_doc.py поиск по документам
models.py  представление бд
request необходимые для работы библиотеки (но это не точно)
views модуль отображения, для запуска сайта  его нужно запустить

