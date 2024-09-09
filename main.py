import os
from src import VideoProcessor

def main():
    input_folder = "data/videos"
    output_folder = "output/processed_videos"

    # Check if input folder exists and has videos
    if not os.path.exists(input_folder):
        print(f"Error: Input folder '{input_folder}' does not exist.")
        print("Please create the folder and add your video files to it.")
        return

    video_files = [f for f in os.listdir(input_folder) if f.endswith(('.mp4', '.avi', '.mov'))]
    if not video_files:
        print(f"Error: No video files found in '{input_folder}'.")
        print("Please add your video files to the input folder.")
        return

    os.makedirs(output_folder, exist_ok=True)

    processor = VideoProcessor()
    processor.process_all_videos(input_folder, output_folder)

if __name__ == "__main__":
    main()