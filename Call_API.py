from datetime import datetime
import os
import requests

def upload_images_from_folder(url, folder_path):
    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y%m%d%H%M%S")
        # 检查文件是否为图片文件
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            # 构建图像文件的完整路径
            image_path = os.path.join(folder_path, filename)

            # 打开图像文件
            with open(image_path, 'rb') as file:
                # 读取图像数据
                image_data = file.read()

            # 构建请求参数
            payload = {
                'time': formatted_time,
                'name_image': filename
            }

            # 使用元组指定文件名和文件对象
            files = {
                'image': (filename, image_data),
            }

            # 发送POST请求
            response = requests.post(url, data=payload, files=files)

            # 打印上传结果
            print(f"Uploaded {filename}: {response.status_code}")
            print(response.text)  # 打印完整的响应内容





api_url = 'http://127.0.0.1:8000/API/upload_image/'
image_folder = './local_folder'

upload_images_from_folder(api_url, image_folder)
