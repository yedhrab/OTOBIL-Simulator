import socketio  # WebSockets
import eventlet
import numpy as np  # Lineer Cebir kütüphanesi
from flask import Flask  # Web uygulamaları geliştirmek için kullanılan paket
from keras.models import load_model
import base64
from io import BytesIO
from PIL import Image
import cv2

""" 
    Websocket'i kullanmamızın nedeni client-server arasındaki değişiklikleri
    anında uygulamalarıdır.

    Kısacası her zaman belirli eventleri dinleyerek veri güncellemesi yapacak
    ve simulasyonu doğru verilerle besliyecek.
"""
sio = socketio.Server()  # SocketIo Server ımız

app = Flask(__name__)  # Web uygulamamamızı oluşturuyoruz --> '__main__'

speed_limit = 10  # Simulasyondaki hız limitimiz


# Flask ın ne olduğu iyice anlaşılsın diye bu method tanımlı..
@app.route('/deneme')
def greeting():
    return 'Welcome'


def img_preprocess(img_path):
    img = img_path[60:136, :, :]
    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    img = cv2.GaussianBlur(img, (3, 3), 0)
    img = cv2.resize(img, (200, 66))
    img = img / 255
    return img


@sio.on('telemetry')
def telemetry(sid, data):
    speed = float(data['speed'])
    image = Image.open(BytesIO(base64.b64decode(data['image'])))
    image = np.asarray(image)
    image = img_preprocess(image)
    image = np.array([image])
    steering_angle = float(model.predict(image))
    throttle = 1.0 - speed / speed_limit
    print('{} {} {}'.format(steering_angle, throttle, speed))
    send_control(steering_angle, throttle)


@sio.on('connect')  # message, disconnect
def connect(sid, environ):
    print('Connected')
    send_control(0, 1)


def send_control(steering_angle, throttle):
    # Event name in the udacity simulator
    sio.emit('steer', data={
        'steering_angle': steering_angle.__str__(),
        'throttle': throttle.__str__()
    })


if __name__ == "__main__":  # Serverımızı dinleyeceğimiz yer
    model = load_model('model.h5')  # Eğittigimiz modeli okuyoruz
    # Flask web uygulamamızla Socket server ımızı birleştiyoruz
    app = socketio.Middleware(sio, app)
    # (x, y) x->Bütün kullanılabilir ip adresinden dinleyioruz ve portumuzu belirtiyoruz
    # (x, y) y-> Web serverımız
    eventlet.wsgi.server(eventlet.listen(('', 4567)), app)
