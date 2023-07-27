print("Initialising...")

print("Libs importing...")
import os
os.system("python -m pip install --upgrade pip")
os.system("pip install -r requirements.txt")

# Capture an image from the camera and save
from pygame import camera
import pygame.image

import uuid
from azure.storage.blob import BlobServiceClient
print("Libs Imported")

connect_str = "DefaultEndpointsProtocol=https;AccountName=lkadls;AccountKey=IVBb4S1GUiE2+YILePq6QYVU/HC55G3olUmubKBq8FKH1ZbuN1fUKxpnkmV1az2MJUAIEOPVN6Xk+AStXk5oBA==;EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connect_str)

container_name = "cicd-data"
local_file_name = uuid.uuid4().hex + ".jpg"
upload_file_path = r"./image.jpg"

print("Camera initiating...")


# Initialize the camera
camera.init()
# Use pygame to get the image
cam = camera.Camera(camera.list_cameras()[0])
cam.start()

print("Camera initiated")

# Capture the image
image = cam.get_image()
# Save the image
pygame.image.save(image, upload_file_path)
# Stop the camera
cam.stop()
# Exit the camera
camera.quit()

print("Image captured")

print("Image uploading...")

try:
    container_client = blob_service_client.get_container_client(container_name)

    blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)

    with open(file=upload_file_path, mode="rb") as data:
        blob_client.upload_blob(data)

    print("_\|/_ Image uploaded successfully  _\|/_ ")
except:
    print("!!!Failed to upload!!!")

os.remove(upload_file_path)