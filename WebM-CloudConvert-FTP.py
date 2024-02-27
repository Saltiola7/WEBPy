import ftplib
import os
import cloudconvert
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def convert_mkv_to_webm(mkv_file_path, webm_file_path):
    """
    Converts a .mkv file to .webm using CloudConvert.

    Args:
        mkv_file_path (str): The file path of the source .mkv file.
        webm_file_path (str): The desired file path for the output .webm file.
    """
    try:
        logging.info("Starting conversion process...")
        cloudconvert.configure(api_key='eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiZjk3ZWYxMWEzY2IzYzgwNmM4OGYyNjA5OGQxODJmZGU3NzUxOGZiMzIyOTI2YWM4MTk1NGEyMmZiM2RkNWU2MGJmNzc4MmI2MWE3N2Y5Y2UiLCJpYXQiOjE3MDkwMDUyMTAuNTgxNDMsIm5iZiI6MTcwOTAwNTIxMC41ODE0MzEsImV4cCI6NDg2NDY3ODgxMC41NzgzMjYsInN1YiI6IjY3MzYzNDExIiwic2NvcGVzIjpbInVzZXIucmVhZCIsInVzZXIud3JpdGUiLCJ0YXNrLnJlYWQiLCJ0YXNrLndyaXRlIiwid2ViaG9vay5yZWFkIiwid2ViaG9vay53cml0ZSIsInByZXNldC5yZWFkIiwicHJlc2V0LndyaXRlIl19.Q_RyEu8YffEQ-_U7V3HOWeGKNX4XTKl7Rw3eTOrkZDUsq_zUANbyXtftVjlnqOTR2HvTLIrFvZHVwbsCCZdoHhcSvC2x0MkyU9cHlabUozjm-Yn7dHvy_DCZ1uNciDkmD8ur1B_9ZyHwno3S35KL7YlcNNHfR9kiF0PB3oaBvxgmYHGQtyXRMxtIWR0GdXcQ0NcR8wCuCI61suRbWrZ7yfqbYXSYueRjfWpJTF-6RhtT2kZMQWW24MTGQMaueBROXnivBiiQtt3I7nYxu08pjs7DN7GSoGVzr9ZhoopDqQqhG6gfOnAOjQ5gDiS27ri16mcCdfK_jqa885eTH1leqb9-JPu-E4zPhBquRVQl-7WIdpXUfpmxqvVs97fghuitXzEPAhbLf5iUi8nLv0wbKGf42zzAMnVdQhLWdrXoTRDMESAVYJkRayFFbD6wdd11jxYkkpgUjNm946n7plzAq_JUFPEkUY4kKu3xMdhIbH9No2S1UC86qwfyeXEaY-0IVC5K4FeajWcRajN3BpAfilxwbngSARawhXqU7quxUlXdphJ5-q2nfi-0zknBI7yoLBhzp1XGNubmkEMowmly2yOFmR7d_uam7NGIPSXt5nkE_Fsv2HsTT37uBgBM4wIcIbrQQNexzCBqjw71DFXjkscf8olIs8FPT5lNStUEqYM', sandbox=False)
        assert os.path.isfile(mkv_file_path), f"File not found at {mkv_file_path}"
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

        logging.info("Starting file upload...")
        upload_response = cloudconvert.Task.upload(file=mkv_file_path, task=upload_task)
        logging.info(f"File upload completed. Response: {upload_response}")

        logging.info("Waiting for job...")
        cloudconvert.Job.wait(id=job['id'])

        logging.info("Getting export task...")
        export_task = [t for t in job['tasks'] if t['name'] == 'export-my-file'][0]

        logging.info("Downloading converted files...")
        converted_files = cloudconvert.Task.download_urls(id=export_task['id'])

        logging.info("Downloading first file...")
        cloudconvert.download.download_file(converted_files[0]['url'], webm_file_path)

        logging.info(f"Conversion successful: '{mkv_file_path}' to '{webm_file_path}'")
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

# Specify your .mkv file path here
mkv_file = '/Users/tis/Movies/test.mkv'
# Specify your desired output .webm file path here
webm_file = '/Users/tis/Movies/webm/test2.webm'

# Convert the file
convert_mkv_to_webm(mkv_file, webm_file)
