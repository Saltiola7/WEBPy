import subprocess
import ftplib
import os

def convert_m4v_to_webm(m4v_file_path, webm_file_path):
    """
    Converts a .m4v file to .webm using ffmpeg with VP8/Opus codecs.

    Args:
        m4v_file_path (str): The file path of the source .m4v file.
        webm_file_path (str): The desired file path for the output .webm file.
    """
    try:
        command = [
            'ffmpeg',
            '-i', m4v_file_path,  # Input file
            '-c:v', 'libvpx-vp9',  # VP8 video codec (software-encoded)
            '-crf', '18',  # Constant Rate Factor (quality level, adjust as needed)
            '-b:v', '0',  # 0 for CRF-controlled bitrate 7000K OBS
            '-preset', 'faster',  # Use a faster preset
            '-b:a', '128k',
            '-c:a', 'libopus',  # Opus audio codec
#            '-threads', '8',  # Utilize up to 8 threads for multithreading
            '-threads', '0',  # Utilize up to 8 threads for multithreading
            '-f', 'webm',  # Explicitly specify WebM output format
            webm_file_path  # Output file
        ]
        subprocess.run(command, check=True)
        print(f"Conversion successful: '{m4v_file_path}' to '{webm_file_path}'")
        upload_to_ftp(webm_file_path)
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")

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
webm_file = '/Users/tis/Movies/webm/test.webm'

# Convert the file
convert_m4v_to_webm(m4v_file, webm_file)
