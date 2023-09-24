import tkinter as tk
from tkinter import filedialog
from pytube import YouTube
from threading import Thread
#from tqdm import tqdm
import os
from tkinter import ttk
import sys

filesize = 0

def sanitize_folder_path(input_path):
    sanitized_path = input_path.replace('/', '_').replace('\\', '_')
    sanitized_path = sanitized_path.replace(' ', '_')
    return sanitized_path

def progress_function(chunk, file_handle, bytes_remaining):
    global filesize
    current = ((filesize - bytes_remaining)/filesize)
    percent = ('{0:.1f}').format(current*100)
    progress = int(50*current)
    status = '█' * progress + '-' * (50 - progress)
    progress_bar['value'] = percent
    progress_val.config(textvariable=tk.StringVar().set(str(percent)))
    progress_val.config(text=f"{str(percent)} % Completed", bg='lightgreen')
    sys.stdout.write(' ↳ |{bar}| {percent}%\r'.format(bar=status, percent=percent))
    sys.stdout.flush()

def download_video():
    try:
        youtube_url = url_entry.get()
        yt = YouTube(youtube_url, on_progress_callback=progress_function)
        video_stream = yt.streams.get_highest_resolution()
        folder_path = filedialog.askdirectory()
        file_path = os.path.join(folder_path, yt.title + '.mp4')
        progress_bar['maximum'] = 100

        def download_thread():
            global filesize
            filesize = video_stream.filesize
            progress_val.config(text=f"Video Downloading...", bg='lightgreen')
            file_name = sanitize_folder_path(yt.title)
            video_stream.download(output_path=folder_path, filename=file_name + '.mp4')

            result_label.config(text=f"Video downloaded successfully to:\n{file_path}", bg='lightgreen')

        download_thread = Thread(target=download_thread)
        download_thread.start()
    except Exception as e:
        result_label.config(text=f"Error: {str(e)}", bg='red')

window = tk.Tk()
window.title("YouTube Video Downloader")

url_label = tk.Label(window, text="Enter YouTube URL:")
url_label.grid(padx=(20, 20), pady=(50, 0))

url_entry = tk.Entry(window, width=50)
url_entry.grid(padx=(20, 20), pady=(10, 20))

browse_button = tk.Button(window, text="Select Folder", command=download_video)
browse_button.grid(padx=(20, 20), pady=(20, 20))

progress_bar = ttk.Progressbar(window, orient="horizontal", length=300)
progress_bar.grid(padx=(20, 20), pady=(20, 0))

progress_val = tk.Message(window,width=200)
progress_val.grid(padx=(20, 20), pady=(10, 20))

result_label = tk.Message(window, text="")
result_label.grid(padx=(20, 20), pady=(0, 50))

window.mainloop()

