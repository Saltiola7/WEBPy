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
        cloudconvert.configure(api_key='eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiMTQyZjFhMDVjNjM5ZGJiZjdiMDJkODdiZWE2ZDA4NWIwZGZmZmY0ZTg4NWI1OWIyYTE1ZTE5Y2JkZjZmZTMzMmM5YTk3NjUxY2JmMzdmYTAiLCJpYXQiOjE3MDkwMDI2OTguMDA4NDI0LCJuYmYiOjE3MDkwMDI2OTguMDA4NDI2LCJleHAiOjQ4NjQ2NzYyOTguMDAxMDU1LCJzdWIiOiI2NzM2MzQxMSIsInNjb3BlcyI6WyJ1c2VyLnJlYWQiLCJ1c2VyLndyaXRlIiwidGFzay5yZWFkIiwidGFzay53cml0ZSIsIndlYmhvb2sucmVhZCIsIndlYmhvb2sud3JpdGUiLCJwcmVzZXQucmVhZCIsInByZXNldC53cml0ZSJdfQ.FvwcJ93QMvW8mG_oTCuf7-JKhvhpWNl0djw3iUr8Hiy9hniX_FXxof4M13VWVnfXpepgMFYo0BP8KO_X9wZIY_dtnSA8oRpia9FVYsk_SwW6tY8tpReQwYCLkF-n_aGJPkuhRIP3CQ7avNEhIwUGVBG90u6PrnB9D1k-khIbp_fu60CSH0-SwHy2-LoYIc9hhM5Z69ZblmVxi4tlkbgw5WRveL5dSCVRcEEOfBxxVxVn5rX2E9JnWefOVxJO5LnkMA9k-fn80Ltv1it_MJWQ-tS6qrFsRWJH0bzkZi-U1kOqS5CDJ4jqDAK_MnsVDPejTjxy3cp5hwFkjZkRtKBm2OhLXckOKvJ865VG-xmSrlK7KYP3VNHwDz4x_nDMpHR-iUN3cwByWTdHtzMr3cQct6HjAbzRQ650t60M1L4lseet89XWpWRbmT4ZyVS91gNcBdlEchbqKbESpJEp6bJP06tjPwFZZzSmvXRuWzQknuudEvSIOuS1tA1Zk3mUsoxrQM8SJuwOVSyDbGzjtddv4LRXnxuYwk0ntfAvnleWs2Qylq1yKL4y4bBccONe5DVRRWMH-lEnbqxWD43rIoSs2nes1OWCQnUNRKoSrFkVBzO6DbSNStolwEwBbMeVlP2z8gvonKd9VM2E5r3Q3Np43x26jYW7zfAZqK9vOLkiNXU', sandbox=True)
        assert os.path.isfile(m4v_file_path), f"File not found at {m4v_file_path}"
        logging.info("Creating job...")
        job = cloudconvert.Job.create(payload={
            "tasks": {
                "import-my-file": {
                    "operation": "import/upload"
                },
                "convert-my-file": {
                    "operation": "convert",
                    "input": "import-my-file",
                    "input_format": "mkv",
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
        upload_response = cloudconvert.Task.upload(file=m4v_file_path, task=upload_task)
        logging.debug(f"File upload completed. Response: {upload_response}")

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
