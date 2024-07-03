import requests
from tqdm import tqdm
import os

def download_file(url, output_path):
    # Send a HTTP request to the given URL
    response = requests.get(url, stream=True)
    # Get the total file size
    total_size = int(response.headers.get('content-length', 0))

    # Create the output directory if it does not exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Open the output file in write mode
    with open(output_path, 'wb') as file:
        # Use tqdm to display a progress bar
        with tqdm(total=total_size, unit='B', unit_scale=True, desc=output_path, ascii=True) as progress_bar:
            for data in response.iter_content(1024):
                # Write data to the file
                file.write(data)
                # Update the progress bar
                progress_bar.update(len(data))

if __name__ == "__main__":
    url = input("Enter the URL of the file to download: ")
    output_path = input("Enter the output path (e.g., /path/to/file.ext): ")
    
    download_file(url, output_path)
    print(f"Download completed and saved to {output_path}")
