import os
import tensorflow as tf
import numpy as np
from PIL import Image

from settings import DEBUG
from utils.image_cropper import crop_jpeg

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
    model = tf.keras.models.load_model('src/saved_model/valid_code_model')

    #  构建数据
    crop_jpeg()
    data = np.ones((len(os.listdir('/tmp/cropped_image')), 46, 34))
    for i, j in zip(os.listdir('/tmp/cropped_image'), range(len(os.listdir('/tmp/cropped_image')))):
        image = Image.open(f'/tmp/cropped_image/{j}.JPEG')
        # print(f'/tmp/cropped_image/{j}.JPEG')
        image_arr = np.array(image)
        data[j, :, :] = image_arr / 255.0
    # print(data)

    probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])

    predictions = probability_model.predict(data)
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
