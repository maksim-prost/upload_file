from flask import Flask, request, render_template, url_for
from flask_wtf.csrf  import  CSRFProtect, CSRFError
import config
from time import time
import os

# заголовок ответа сервера для того чтобы браузер принимал ответы
headers = {'Access-Control-Allow-Origin': '*',
		   'Content-type': 'text/html',	
		   'Access-Control-Allow-Headers':'X-CSRFToken',}

def check_file(file):
	# проверка файла на некоторые ограничения
	return True

# cоздаем прилдожение, загружаем настройки, подключаем проверку подлиности
app = Flask(__name__) 
app.config.from_object ( 'config' )
csrf  =  CSRFProtect ( app )

@app.route('/',methods=['GET',])
# @csrf.exempt
def index():
	return render_template('index.html'),200,headers

#обработка ошибок 
@app.errorhandler(CSRFError)
def handle_csrf_error(e):
	return e.description , 400, headers

@app.route('/upload',methods=['POST','OPTIONS'])
@csrf.exempt#TODO: разобраться с r.setRequestHeader ("X-CSRFToken" , csrf_token );
# работает в собраном приложени, НО с браузера выдает ошибку: 'The CSRF session token is missing.'
# для запуска из браузера строку @csrf.exempt расскоментировать
def upload():
	if request.method == 'OPTIONS':
		return "{'Allow':'POST'}",200,headers
	
	file = request.files.get('file')#получаем файл из запроса
	# если файл в запросе есть 
	if not file:
	# принцип слабой связаности данных, со страницы такого запроса прийти не может, но проверим
		return  'error loading file %s'%file.filename, 200, headers
	
	if check_file(file):
		# создаем имя для сохранения файла
		filename = os.path.join(app.config['DIR_SAVE_FILES'],
			'{} {}'.format(str(time()),file.filename.split(os.path.sep)[-1]))
		# сохраняем файл
		file.save(filename)
		# возвращаем ответ что файл успешно загружен
		return '% s success upload'%file.filename, 202 , headers
	# возвращаем ответ что файл не  загружен потомучто не прошел проверку
	return  'error loading %s, file failed verification'%file.filename, 200, headers

app.run()
