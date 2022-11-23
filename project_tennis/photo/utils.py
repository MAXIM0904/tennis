from os import makedirs
from PIL import Image


def save_img(file_url, file_user, new_name):
    """Функция сохранения фото """
    try:
        makedirs(file_url, exist_ok=True)
        img = Image.open(file_user.file)
        rgb_im = img.convert("RGB")
        rgb_im.save(f"{file_url}/{new_name}", optimize=True, quality=85)
        return True, "Фото успешно загружены"
    except IOError:
        return False, "Формат файла не поддерживается."
