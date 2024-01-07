from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import numpy as np
from PIL import Image
from flask_bootstrap import Bootstrap5
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('APPKEY')
app.config['ALLOWED EXTENSIONS'] = ['.jpg', '.png', '.jpeg', '.gif', '.JPG', '.PNG', '.JPEG', '.PNG']
Bootstrap5(app)


directory = os.environ.get('DIRECTORY')


def empty_directory():
    try:
        for i in os.listdir(directory):
            os.remove(os.path.join(directory, i))
    except IndexError:
        pass


@app.route('/', methods=['GET', 'POST'])
def home():
    try:
        image = os.listdir(directory)[0]
    except IndexError:
        image = ''
    if request.method == 'POST':
        empty_directory()

        file = request.files['picture']
        num_of_colors = request.form.get('Numbers')
        if file:
            ext = os.path.splitext(file.filename)[1]
            if not ext in app.config['ALLOWED EXTENSIONS']:
                print('zingankivu')
            else:
                file.save(os.path.join(directory, secure_filename(file.filename)))

        return redirect(url_for('extract_colors', num_of_colors=num_of_colors))

    return render_template('index.html', image=image)


@app.route('/<img_name>', methods=['GET', 'POST'])
def show_image(img_name):
    return send_from_directory(directory, img_name)


@app.route('/extract/<int:num_of_colors>', methods=['GET', 'POST'])
def extract_colors(num_of_colors):
    try:
        img = os.listdir(directory)[0]
    except IndexError:
        return redirect('/')

    my_img = Image.open(os.path.join(directory, img))
    img_array = np.array(my_img)

    empty_list = []
    for i in img_array:
        for s in i:
            empty_list.append(s)

    colors = []
    r = num_of_colors
    f = 0
    for p in range(r):
        colors.append(empty_list[f])
        f += int(len(empty_list) / r)
    return render_template('extract.html', colors=colors, image=img)


if __name__ == "__main__":
    app.run(debug=True)
