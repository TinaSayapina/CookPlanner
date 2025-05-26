import requests
import base64
from io import BytesIO

# importing os module for environment variables
import os
# importing necessary functions from dotenv library
from dotenv import load_dotenv, dotenv_values

# loading variables from .env file
load_dotenv()

# Достаем апи ключ openai из файла .env
DEEPINFRA_TOKEN = os.getenv("DEEPINFRA_TOKEN")

def generate_image(prompt):
    url = "https://api.deepinfra.com/v1/inference/stabilityai/sdxl-turbo"
    headers = {
        "Authorization": f"Bearer {DEEPINFRA_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": prompt,
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        output = response.json()
        base64_image = output['images'][0]
        if base64_image.startswith('data:image'):
            base64_image = base64_image.split(",")[1]
        image_data = base64.b64decode(base64_image)
        image_file = BytesIO(image_data)
        image_file.name = f"{prompt}.png"

        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        save_dir = os.path.join(project_root, 'static', 'images')

        # Создать папку, если её нет
        os.makedirs(save_dir, exist_ok=True)

        # Далее, когда сохраняете изображение:
        save_path = os.path.join(save_dir, image_file.name)
        # Предположим, у вас есть image_data — байты картинки
        with open(save_path, 'wb') as f:
            f.write(image_data)

    else:
        print("Ошибка генерации:", response.text)
        return None
