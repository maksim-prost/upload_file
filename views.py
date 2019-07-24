from flask import Flask, Response, request, render_template, jsonify
from flask_wtf.csrf  import  CSRFProtect, CSRFError
import config
from time import time
import os

# заголовок ответа сервера для того чтобы браузер принимал ответы
class MyResponse(Response):
	def __init__(self, response,**args):
		base_headers = {'Access-Control-Allow-Origin': '*',
				'Content-type': 'text/html',	}
				# 'Access-Control-Allow-Headers':('X-CSRFToken',"any-field")}
		# base_headers={}
		base_headers.update(args.get('headers') or {})
		args['headers'] = base_headers
		return super(MyResponse,self).__init__(response,**args)
	
	@classmethod
	def force_type(cls, rv, environ=None):
		if isinstance(rv, dict):
			rv = jsonify(rv)
		return super(MyResponse, cls).force_type(rv, environ)


def check_file(file):
	# проверка файла на некоторые ограничения
	return True

# cоздаем прилдожение, загружаем настройки, подключаем проверку подлиности
app = Flask(__name__) 
app.config.from_object ( 'config' )
app.response_class = MyResponse
csrf  =  CSRFProtect ( app )

@app.route('/',methods=['GET',])
# @csrf.exempt
def index():
	return render_template('index.html')#,200,headers

#обработка ошибок 
@app.errorhandler(CSRFError)
def handle_csrf_error(e):
	return {'status':'error', 'msg':e.description }

@app.route('/upload',methods=['POST','OPTIONS'])
def upload():
	
	file = request.files.get('file')#получаем файл из запроса
	# если файл в запросе есть 
	if not file:
	# принцип слабой связаности данных, со страницы такого запроса прийти не может, но проверим
		return  {'status':'error loading','file':file.filename}
	
	if check_file(file):
		# создаем имя для сохранения файла
		filename = os.path.join(app.config['DIR_SAVE_FILES'],
			'{} {}'.format(str(time()),file.filename.split(os.path.sep)[-1]))
		# сохраняем файл
		file.save(filename)
		# возвращаем ответ что файл успешно загружен
		return {'status':'succes upload','file':file.filename}
	# возвращаем ответ что файл не  загружен потомучто не прошел проверку
	return  {'status':'error loading, file failed verification','file':file.filename}

app.run()
