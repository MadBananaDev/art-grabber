import os
import urllib.request
import time
import socket

def download_image(url, save_path, retries=5):
    attempt = 0
    while attempt < retries:
        try:
            with urllib.request.urlopen(url) as response:
                if response.status == 200:
                    with open(save_path, 'wb') as file:
                        file.write(response.read())
                    print(f"Downloaded: {save_path}")
                    return True
                else:
                    print(f"Failed to download: {url} - Status code: {response.status}")
                    return False
        except (urllib.error.URLError, socket.gaierror) as e:
            print(f"Error downloading {url}: {e}")
            attempt += 1
            wait_time = 2 ** attempt  # Exponential backoff
            print(f"Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
    return False

def main():
    base_url = "https://tbziw4f7f4.execute-api.us-west-2.amazonaws.com/dev/images/"
    save_directory = "images"
    retries = 5

    # Create the save directory if it doesn't exist
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    for i in range(10001):  # Download from 0.png to 10000.png
        image_name = f"{i}.png"
        image_url = f"{base_url}{image_name}"
        save_path = os.path.join(save_directory, image_name)
        if download_image(image_url, save_path, retries):
            time.sleep(5)  # Add a 5-second delay between successful requests
        else:
            print(f"Failed to download {image_name} after {retries} retries. Skipping...")

if __name__ == "__main__":
    main()
