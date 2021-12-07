import os
import io
from io import BytesIO
from PIL import Image
from flask import Flask, render_template, request, redirect, jsonify
import base64

# check for image files
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


app = Flask(__name__)
# __file__ refers to the file settings.py
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_STATIC = os.path.join(APP_ROOT, 'static/')


def touxiang(touxiang):
    guoqi = Image.open(APP_STATIC + 'china.png')
    touxiang = touxiang.resize((900, 900))
    # 获取国旗的尺寸
    # x, y = guoqi.size
    # # quyu = guoqi.crop((262,100, y+62,y-100))
    # # quyu.show()

    # 获取头像的尺寸
    w, h = touxiang.size
    # 将区域尺寸重置为头像的尺寸
    quyu = guoqi.resize((w, h))
    # 透明渐变设置
    for i in range(w):
        for j in range(h):
            color = quyu.getpixel((i, j))
            alpha = 255 - i // 3
            if alpha < 0:
                alpha = 0
            color = color[:-1] + (alpha,)
            quyu.putpixel((i, j), color)
    # 粘贴到头像
    touxiang.paste(quyu, (0, 0), quyu)
    # touxiang.show()
    return touxiang


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file:
            return
        figfile = io.BytesIO(file.read())
        image = Image.open(figfile)
        ori_img = base64.b64encode(figfile.getvalue()).decode('ascii')
        image = touxiang(image)
        # read added information
        user_input = request.form.get("name")

        # deep learning process image
        # res_img = model.forward(image)

        # img = base64.b64encode(figfile.getvalue()).decode('ascii')        # for byte type
        output_buffer = BytesIO()  # for PIL.Image
        image.save(output_buffer, format='JPEG')
        img = base64.b64encode(output_buffer.getvalue()).decode('ascii')

        return render_template('result.html', user_input=user_input, img=img, ori_img=ori_img)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=8866)
