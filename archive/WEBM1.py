import subprocess

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
            '-b:v', '7000k',  # 0 for CRF-controlled bitrate
            '-b:a', '128k',
            '-c:a', 'libopus',  # Opus audio codec
            '-threads', '8',  # Utilize up to 8 threads for multithreading
            '-f', 'webm',  # Explicitly specify WebM output format
            webm_file_path  # Output file
        ]
        subprocess.run(command, check=True)
        print(f"Conversion successful: '{m4v_file_path}' to '{webm_file_path}'")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")

# Specify your .m4v file path here
m4v_file = '/Users/tis/Movies/knowurbiz.mkv'
# Specify your desired output .webm file path here
webm_file = '/Users/tis/Movies/webm/knowurbiz.webm'

# Convert the file
convert_m4v_to_webm(m4v_file, webm_file)
