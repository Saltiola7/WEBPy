import subprocess

def convert_m4v_to_webm(m4v_file_path, webm_file_path):
    """
    Convert a .m4v file to .webm using ffmpeg.

    Args:
    m4v_file_path (str): The file path of the source .m4v file.
    webm_file_path (str): The desired file path for the output .webm file.
    """
    try:
        command = [
            'ffmpeg',
            '-i', m4v_file_path,  # Input file
            '-c:v', 'libvpx-vp9',  # Video codec (VP9)
            '-crf', '30',  # Constant Rate Factor (quality level, where lower means better quality)
            '-b:v', '0',  # Target bitrate (0 allows the CRF setting to adjust bitrate as needed)
            '-c:a', 'libopus',  # Audio codec
            webm_file_path  # Output file
        ]
        subprocess.run(command, check=True)
        print(f"Conversion successful: '{m4v_file_path}' to '{webm_file_path}'")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")

# Specify your .m4v file path here
m4v_file = '/Users/tis/Movies/webm/InHunt.mov'
# Specify your desired output .webm file path here
webm_file = '/Users/tis/Movies/webm/InHunt.webm'

# Convert the file
convert_m4v_to_webm(m4v_file, webm_file)