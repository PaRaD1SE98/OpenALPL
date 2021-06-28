import os
import numpy as np
from PIL import Image

from settings import DEBUG, ENABLE_TF_SERVING
from utils.image_cropper import crop_jpeg
from os import environ

# np.set_printoptions(linewidth=np.inf, threshold=np.inf)

"""
设置日志输出级别

 Level  | Level for Humans | Level Description                  
 -------|------------------|------------------------------------ 
  0     | DEBUG            | [Default] Print all messages       
  1     | INFO             | Filter out INFO messages           
  2     | WARNING          | Filter out INFO & WARNING messages 
  3     | ERROR            | Filter out all messages      
"""
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0' if DEBUG else '1'


def get_classname():
    num = '23456789'  # 01
    # print(len(num))
    # alphabet = 'abcdefghjklmnpqrstuvwxyz'  # io
    # print(len(alphabet))
    alphabet_c = 'ABCDEFGHJKLMNPQRSTUVWXYZ'  # IO
    # print(len(alphabet_c))
    my_str = num + alphabet_c  # + alphabet
    class_names = []
    for i in my_str:
        class_names.append(i)
    # print(class_names)
    return class_names


def predict():
    #  构建数据
    crop_jpeg()
    data = np.ones((len(os.listdir('/tmp/cropped_image')), 46, 34))
    for j, i in enumerate(os.listdir('/tmp/cropped_image')):
        image = Image.open(f'/tmp/cropped_image/{j}.JPEG')
        # print(f'/tmp/cropped_image/{j}.JPEG')
        image_arr = np.array(image)
        data[j, :, :] = image_arr / 255.0
    # print(data)

    if not ENABLE_TF_SERVING:
        import tensorflow as tf
        model = tf.keras.models.load_model('src/saved_model/valid_code_model')
        predictions = model.predict(data)
    else:
        import requests
        import json
        headers = {"content-type": "application/json"}
        data = json.dumps({"signature_name": "serving_default", "instances": data.tolist()})
        json_response = requests.post(
            environ['TF_API_URL'],
            data=data,
            headers=headers
        )
        predictions = json.loads(json_response.text)['predictions']
    return predictions


def tf_result():
    result = ''
    for i in predict():
        predicted_label = np.argmax(i)
        # print(class_names[predicted_label])
        result += get_classname()[predicted_label]
    if DEBUG:
        print('tf_result', result)
    return result


if __name__ == '__main__':
    tf_result()
