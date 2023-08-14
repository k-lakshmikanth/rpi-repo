import os
from shutil import copyfile

print("Initialising...")
print("Libs importing...")

from picamera import PiCamera
import uuid
from azure.storage.blob import BlobServiceClient
print("Libs Imported")

connect_str = "DefaultEndpointsProtocol=https;AccountName=lkadls;AccountKey=IVBb4S1GUiE2+YILePq6QYVU/HC55G3olUmubKBq8FKH1ZbuN1fUKxpnkmV1az2MJUAIEOPVN6Xk+AStXk5oBA==;EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connect_str)

container_name = "cicd-data"
local_file_name = uuid.uuid4().hex + ".jpg"
upload_file_name = "image.jpg"
upload_file_path = f"/home/lucky/Desktop/img_uploader/{upload_file_name}"

print("Camera initiating...")
camera = PiCamera()
print("Camera initiated")
camera.capture(upload_file_path)
camera.close()

print("Image captured")
print("Image uploading...")

try:
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)
    with open(file=upload_file_path, mode="rb") as data:
        blob_client.upload_blob(data)
    print("_\|/_ Image uploaded successfully  _\|/_ ")
    os.remove(upload_file_path)
except Exception as e:
    print(e)
    print("!!! Failed to upload !!!")
    copyfile(upload_file_path, f"/home/lucky/Desktop/img_uploader/Images/{upload_file_name}")
