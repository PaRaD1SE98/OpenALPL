from utils.trainer.trainer import train
from utils.trainer.image_cropper import crop_jpeg

success_image = 'src/success_image'
cropped_success_image = 'src/cropped_success_image'


def train_process():
    """
    格式化裁剪原图片，处理后的图片保存到'src/cropped_success_image'

    训练模型，并将模型保存到'src/saved_model'
    """
    crop_jpeg(success_image, cropped_success_image)
    train(cropped_success_image)


if __name__ == '__main__':
    train_process()
