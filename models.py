from django.db import models

import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.models import load_model
from PIL import Image
import io, base64

graph = tf.get_default_graph()

class Photo(models.Model):
    image = models.ImageField(upload_to='photos')

    IMAGE_SIZE = 224 # 画像サイズ
    # MODEL_FILE_PATH = './carbike/ml_models/vgg16_transfer.h5'
    MODEL_FILE_PATH = './carbike/ml_models/vgg16_transfer_vehicle6.h5'
    classes = ["car", "motorbike", "bike", "ambulance", "ship", "bus"]
    num_classes = len(classes)
    print("hello Photo class")

    # 引数から画像ファイルを参照して読み込むメソッド
    def predict(self):
        print("hello predict")
        model = None # AIの分類モデルを格納する
        global graph # Tensorflowの機能。AIモデルのセッションを保持する機能。
                     # 毎回同じモデルにデータを投入して推定ができるようにする
                     # ちゃんと理解しようとすると素のTensorflowを理解しようとすることになるから割と辛い
        with graph.as_default():
            model = load_model(self.MODEL_FILE_PATH)

            img_data = self.image.read()
            img_bin = io.BytesIO(img_data)

            image = Image.open(img_bin)
            image = image.convert("RGB")
            image = image.resize((self.IMAGE_SIZE, self.IMAGE_SIZE))
            data = np.asarray(image) / 255.0 # npyファイルのサイズが増えるため、ここで浮動小数点で正規化しない。
            X = []
            X.append(data)
            X = np.array(X)

            result = model.predict([X])[0]
            predicted = result.argmax() # 値の大きい方を取る
            percentage = int(result[predicted] * 100) # パーセンテージを格納

            # print(self.classes[predicted], percentage)
            return self.classes[predicted], percentage # returnで返してあげると、Views.pyで値を使える。

    def image_src(self):
        with self.image.open() as image:
            base64_img = base64.b64encode(image.read()).decode()
        return 'data:' + image.file.content_type + ';base64,' + base64_img