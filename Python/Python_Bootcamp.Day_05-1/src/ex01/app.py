import os
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    list_of_files = os.listdir('./static')
    return render_template('index.html', files=list_of_files)


@app.route('/list')
def mlist():
    list_of_files = os.listdir('./static')
    list_of_files = '\n'.join(list_of_files)
    return list_of_files


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    print(request.files)
    print(request.files['file'])
    if 'file' not in request.files:
        # Проверка, был ли передан файл
        return "Нет файлов для загрузки", 404  # Возвращаем ошибку 400 Bad Request
    file = request.files['file']
    if file.filename == '':
        # Проверка, было ли выбрано имя файла
        return "Выберите файл", 400  # Возвращаем ошибку 400 Bad Request

    if not file:
        return "Произошла ошибка при загрузке файла", 500

    if file.mimetype[:5] != 'audio':
        return 'Non-audio file detected', 415

    file.save(f'static/{secure_filename(file.filename)}')

    return redirect('/')


if __name__ == '__main__':
    app.run(host='localhost', port=8888, debug=True)
