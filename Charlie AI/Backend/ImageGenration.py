import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import get_key
import os
import sys
from time import sleep


def open_images(prompt):
    folder_path = r"Data"
    prompt = prompt.replace(" ", "_")
    files: list[str] = os.listdir("Data")

    Files = [file for file in files if file.endswith(".jpg")]

    for jpg_file in Files:
        image_path = os.path.join(folder_path, jpg_file)

        try:
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)

        except IOError:
            print(f"Unable to open {image_path}")


API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-dev"
headers = {"Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPIKey')}"}

async def query(payload):
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
    return response.content


async def generate_images(prompt: str):
    tasks =[]


    for _ in range(1,3):
        payload = {
            "inputs": f"{prompt}, quality=4k, sharpness=maximum, Ultra High details, high resolution, seed = {randint(0, 1000000)}",
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)

    image_bytes_list = await asyncio.gather(*tasks)


    for i, image_bytes in enumerate(image_bytes_list):
        with open(fr"Data\{i + 3}.jpg", "wb") as f:
            f.write(image_bytes)


def GenerateImages(prompt: str):
    asyncio.run(generate_images(prompt))
    open_images(prompt)


# while True:

#     try:

#         with open(r"Frontend\Files\ImageGeneration.data", "r") as f:
#             Data: str = f.read()

#         Prompt, Status = Data.split(",")


#         if Status == "True":
#             print("Generating Images...")
#             ImageStatus = GenerateImages(prompt=Prompt)


#             with open(r"Frontend\Files\ImageGeneration.data", "w") as f:
#                 f.write("False,False")
#                 break

#         else:
#             sleep(1)


#     except:
#         pass
# if __name__=="__main__":
#     GenerateImages("pizza")