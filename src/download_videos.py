import os
from pytube import YouTube
from tqdm import tqdm

def download_video(url, output_path):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        
        print(f"Downloading: {yt.title}")
        stream.download(output_path)
        print(f"Download complete: {yt.title}")
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")

def main():
    video_urls = [
        "https://www.youtube.com/watch?v=V9YDDpo9LWg",
        "https://www.youtube.com/watch?v=JBoc3w5EKfI",
        "https://www.youtube.com/watch?v=aWV7UUMddCU",
        "https://www.youtube.com/watch?v=f6wqlpG9rd0",
        "https://www.youtube.com/watch?v=GNVTuLHdeSo",
        "https://www.youtube.com/watch?v=SWtmkjd45so"
    ]
    
    output_path = "data/videos"
    os.makedirs(output_path, exist_ok=True)
    
    for url in tqdm(video_urls, desc="Downloading videos"):
        download_video(url, output_path)

if __name__ == "__main__":
    main()