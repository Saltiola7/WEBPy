import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import os

class Watcher:
    def __init__(self, directory_to_watch):
        self.directory_to_watch = directory_to_watch
        self.observer = Observer()

    def run(self):
        event_handler = ImageConversionHandler()
        self.observer.schedule(event_handler, self.directory_to_watch, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:  # Gracefully handle Ctrl+C
            self.observer.stop()
            print("Observer Stopped")
        self.observer.join()

class ImageConversionHandler(FileSystemEventHandler):
    @staticmethod
    def on_created(event):
        if not event.is_directory and event.src_path.lower().endswith(('.jpg', '.jpeg', '.png')):
            print(f"Received created event - {event.src_path}.")
            output_path = os.path.splitext(event.src_path)[0] + '.webp'
            # Max dimensions for 16" Retina display optimization
            max_width = 2880
            max_height = 1920
            subprocess.run([
                "magick", "convert", event.src_path,
                "-strip",  # Remove metadata
                "-quality", "74",  # Adjust quality setting
                "-define", "webp:lossless=false",  # Use lossy compression for better file size
                "-resize", f"{max_width}x{max_height}>",  # Resize if larger than max dimensions, preserve aspect ratio
                output_path
            ])
            print(f"Converted {event.src_path} to {output_path}.")

if __name__ == '__main__':
    directory_to_watch = "/Users/[you decide this path]"
    w = Watcher(directory_to_watch)
    w.run()
