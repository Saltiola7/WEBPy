```
# WebP Image Converter for Mac

This Python application monitors a specified directory for new image files (JPG, JPEG, PNG) and automatically converts them to the WebP format. It's optimized for 16" Retina displays, ensuring high-quality images with reduced file sizes for web use. The application uses the Watchdog library to watch for new files and ImageMagick for the conversion process.

## Features

- **Automatic Conversion**: Monitors a user-specified directory and automatically converts new images to WebP format.
- **Retina Display Optimization**: Optimizes images for 16" Retina displays, balancing image quality with file size.
- **Aspect Ratio Preservation**: Maintains the original aspect ratio of images and does not stretch smaller images.
- **Configurable**: Allows users to configure settings like the directory to watch, max dimensions, and image quality.

## Requirements

- Python 3
- ImageMagick
- Watchdog library

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/[your_username]/webp-image-converter.git
   cd webp-image-converter
   ```

2. **Install the required packages:**
   ```bash
   pip install watchdog
   ```

3. **Ensure ImageMagick is installed:**
   - ImageMagick can be installed via Homebrew:
     ```bash
     brew install imagemagick
     ```

## Configuration

Before running the application, configure the `directory_to_watch` in the script to the directory you want to monitor:

```python
if __name__ == '__main__':
    directory_to_watch = "/Users/[you decide this path]"
    w = Watcher(directory_to_watch)
    w.run()
```

Replace `"/Users/[you decide this path]"` with the path to the directory you want to monitor.

## Usage

To run the application, navigate to the application directory in your terminal and run:

```bash
python convert_to_webp.py
```

The application will start monitoring the specified directory and automatically convert any new JPG, JPEG, or PNG files to WebP format.

## Packaging as a macOS Application

You can package this script as a standalone macOS application using `py2app`. Refer to the `py2app` documentation for detailed instructions.

## Contribution

Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
```
