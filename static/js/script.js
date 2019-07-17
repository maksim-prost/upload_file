
function checkFile (file) {
	// проверка файла на некоторые ограничения
	return true;
	console.log(`error loading ${file.filename}, file failed verification`);
	return false;
}

document.querySelector('#file-upload').onchange = function (argument) {
	// при всех изменениях в обекте для выбора файлов
	// осущесвляем POST запрос по адресу полученному из полученого html,
	// используя для защиты csrf_token для всех полученных файлов
	let url = this.getAttribute('url_upload'),
		csrf_token = this.getAttribute('csrf-token'),
		files = this.files;

	for (let i=0;i<files.length;i++){
		if (checkFile(files[i])){
			request(files[i], url, csrf_token);
		}
	}
}

function request(file, url, csrf_token) {
	// console.log(url, csrf_token)
	// POST запрос, для отправки файла
	var formData = new FormData(),
		r = new XMLHttpRequest();
	formData.append('file',file);
	// formData.append('csrf_token',csrf_token);
	r.open('POST',url,true);
	r.setRequestHeader ("X-CSRFToken" , csrf_token );
	r.onload = function(){
		console.log(r.responseText);
	}
	r.send(formData);
}
