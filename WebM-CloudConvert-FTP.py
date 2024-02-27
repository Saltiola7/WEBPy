import ftplib
import os
import cloudconvert
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

import logging

logging.basicConfig(level=logging.DEBUG)

def convert_m4v_to_webm(m4v_file_path, webm_file_path):
    """
    Converts a .m4v file to .webm using CloudConvert.

    Args:
        m4v_file_path (str): The file path of the source .m4v file.
        webm_file_path (str): The desired file path for the output .webm file.
    """
    try:
        logging.info("Starting conversion process...")
        cloudconvert.configure(api_key='your-api-key', sandbox=True)

        logging.info("Creating job...")
        job = cloudconvert.Job.create(payload={
            "tasks": {
                "import-my-file": {
                    "operation": "import/upload"
                },
                "convert-my-file": {
                    "operation": "convert",
                    "input": "import-my-file",
                    "output_format": "webm",
                    "engine": "ffmpeg"
                },
                "export-my-file": {
                    "operation": "export/url",
                    "input": "convert-my-file"
                }
            }
        })

        logging.info("Waiting for upload task...")
        upload_task = cloudconvert.Task.wait(id=job['tasks'][0]['id'])

        logging.debug("Starting file upload...")
        cloudconvert.Task.upload(file=m4v_file_path, task=upload_task)
        logging.debug("File upload completed.")

        logging.info("Waiting for job...")
        cloudconvert.Job.wait(id=job['id'])

        logging.info("Getting export task...")
        export_task = [t for t in job['tasks'] if t['name'] == 'export-my-file'][0]

        logging.info("Downloading converted files...")
        converted_files = cloudconvert.Task.download_urls(id=export_task['id'])

        logging.info("Downloading first file...")
        cloudconvert.download.download_file(converted_files[0]['url'], webm_file_path)

        logging.info(f"Conversion successful: '{m4v_file_path}' to '{webm_file_path}'")
        upload_to_ftp(webm_file_path)
    except Exception as e:
        logging.error(f"Error during conversion: {e}")

def upload_to_ftp(file_path):
    """
    Uploads a file to a FTP server.

    Args:
        file_path (str): The file path of the file to be uploaded.
    """
    try:
        # Establish a connection to the FTP server
        ftp = ftplib.FTP('se.storage.bunnycdn.com', 'stockholm-video-storage', '7cd876f1-e6fe-4d64-b08b0b074fcb-0bfa-4606')
        # Open the file in binary mode and upload it
        with open(file_path, 'rb') as f:
            ftp.storbinary('STOR ' + os.path.basename(file_path), f)
        # Close the connection
        ftp.quit()
        print(f"Upload successful: '{file_path}'")
    except ftplib.all_errors as e:
        print(f"Error during upload: {e}")

# Specify your .m4v file path here
m4v_file = '/Users/tis/Movies/test.mkv'
# Specify your desired output .webm file path here
webm_file = '/Users/tis/Movies/webm/test2.webm'

# Convert the file
convert_m4v_to_webm(m4v_file, webm_file)
