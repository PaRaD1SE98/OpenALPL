from tensorflow import keras
import numpy as np
from PIL import Image
import os
import matplotlib.pyplot as plt
import datetime
from random import shuffle

"""设置训练次数"""
EPOCHS = 1000

# 设置np输出不省略
np.set_printoptions(linewidth=np.inf, threshold=np.inf)


def train(source_cropped_image):
    # 构建分类列表
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

    # 构建原始数据
    source_dir_list = os.listdir(source_cropped_image)
    # 随机排列
    shuffle(source_dir_list)
    data = np.ones((len(source_dir_list), 46, 34))
    # print(data)
    for i, j in zip(source_dir_list, range(len(source_dir_list))):
        image = Image.open(f'{source_cropped_image}/{i}')
        image_arr = np.array(image)
        data[j, :, :] = image_arr
    # print(data)

    # 获取标签名原始文件名
    label = source_dir_list
    # 取文件名第一个字符
    for i, j in zip(label, range(len(label))):
        label[j] = i[0]
    # 将标签名转换为分类列表的索引
    for i, j in zip(label, range(len(label))):
        label[j] = class_names.index(i)
    label = np.array(label)
    # print('label', label)

    # 切割数据，构建训练集和测试集
    print('datashape', data.shape)
    seperate_point = int(len(source_dir_list) * (2 / 4))
    print('seperate_point', seperate_point)
    train_data = data[:seperate_point]
    test_data = data[seperate_point:]
    train_data = train_data / 255.0
    test_data = test_data / 255.0
    train_label = label[:seperate_point]
    test_label = label[seperate_point:]
    # print(train_label)
    # print(test_label)
    # plt.imshow(train_data[2])
    # plt.show()

    # 构建模型
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(46, 34)),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dense(len(class_names))  # 输出值要与分类数量相等
    ])

    # 编译模型
    model.compile(optimizer='adam',
                  loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    # 训练模型
    log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    tensorboard_callback = keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)
    model.fit(
        train_data,
        train_label,
        epochs=EPOCHS,
        callbacks=[tensorboard_callback],
    )

    # 保存模型
    model.save('src/saved_model/valid_code_model')

    # 保存模型结构图
    dot_img_file = 'src/saved_model/model_1.png'
    keras.utils.plot_model(model, to_file=dot_img_file, show_shapes=True)

    # 测试模型
    test_loss, test_acc = model.evaluate(test_data, test_label, verbose=2)
    print('\nTest accuracy:', test_acc)

    # 将线性输出logits转换为概率输出
    probability_model = keras.Sequential([model, keras.layers.Softmax()])
    predictions = probability_model.predict(test_data)

    dot_img_file = 'src/saved_model/probability_model_1.png'
    keras.utils.plot_model(probability_model, to_file=dot_img_file, show_shapes=True)

    # 打印测试图
    def plot_image(image_index, predictions_array, true_label, img):
        predictions_array, true_label, img = predictions_array, true_label[image_index], img[image_index]
        plt.grid(False)
        plt.xticks([])
        plt.yticks([])

        plt.imshow(img, cmap=plt.cm.binary)

        predicted_label = np.argmax(predictions_array)
        if predicted_label == true_label:
            color = 'blue'
        else:
            color = 'red'

        plt.xlabel("{} {:2.0f}% ({})".format(
            class_names[predicted_label],
            100 * np.max(predictions_array),
            class_names[true_label]),
            color=color
        )

    def plot_value_array(label_index, predictions_array, true_label):
        predictions_array, true_label = predictions_array, true_label[label_index]
        plt.grid(False)
        plt.xticks(range(len(class_names)))
        plt.yticks([])
        thisplot = plt.bar(range(len(class_names)), predictions_array, color="#777777")
        plt.ylim([0, 1])
        predicted_label = np.argmax(predictions_array)

        thisplot[predicted_label].set_color('red')
        thisplot[true_label].set_color('blue')

    num_rows = 5
    num_cols = 3
    num_images = num_rows * num_cols
    plt.figure(figsize=(2 * 2 * num_cols, 2 * num_rows))
    for i in range(num_images):
        plt.subplot(num_rows, 2 * num_cols, 2 * i + 1)
        plot_image(i, predictions[i], test_label, test_data)
        plt.subplot(num_rows, 2 * num_cols, 2 * i + 2)
        plot_value_array(i, predictions[i], test_label)
    plt.tight_layout()
    plt.show()
