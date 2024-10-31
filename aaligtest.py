import csv
import subprocess
import os

# Path to the CSV file
csv_file_path = 'video_subtitle_alignment.csv'

# Output directory for the video clips
clips_directory = 'bobsl_clips'

# Path to the new CSV file for clips information
clips_csv_path = 'clips_subtitle_alignment.csv'

# Ensure the clips directory exists (commented out as requested)
# if not os.path.exists(clips_directory):
#     os.makedirs(clips_directory)

# Function to split the video into clips using ffmpeg
def split_video(video_path, start_time, end_time, clip_output_path):
    try:
        # Constructing the ffmpeg command to cut the video
        command = [
            'ffmpeg',
            '-i', video_path,
            '-ss', start_time,
            '-to', end_time,
            '-c', 'copy',  # Copy the video and audio streams without re-encoding
            clip_output_path,
            '-y'  # Overwrite output files without asking
        ]
        # Execute the command
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while splitting the video: {e}")
        return False

# Open the CSV for recording clip information
with open(clips_csv_path, 'w', newline='', encoding='utf-8') as clips_csvfile:
    clips_csvwriter = csv.writer(clips_csvfile)
    clips_csvwriter.writerow(['Clip Path', 'Start Time', 'End Time', 'Subtitle'])

    # Read the input CSV file
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader, None)  # Skip the header row
        
        # Track processed clips for each video
        for row in csvreader:
            video_path, start_time, end_time, subtitle = row
            # Add 'bobsl_videos/' before the video path
            video_path = os.path.join('bobsl_videos/', video_path)

            # Construct the clip name
            clip_name = f"{os.path.splitext(os.path.basename(video_path))[0]}_{start_time.replace(':', '-')}-{end_time.replace(':', '-')}.mp4"
            clip_output_path = os.path.join(clips_directory, clip_name)

            # Check if the current clip has already been created
            if os.path.exists(clip_output_path):
                print(f"Clip {clip_name} already exists, adding to CSV.")
                # Write the existing clip to the CSV
                clips_csvwriter.writerow([os.path.basename(clip_output_path), start_time, end_time, subtitle])
            else:
                # Create the clip if it does not exist
                if split_video(video_path, start_time, end_time, clip_output_path):
                    print(f"Created clip {clip_name}, adding to CSV.")
                    # Write the new clip information to the CSV
                    clips_csvwriter.writerow([os.path.basename(clip_output_path), start_time, end_time, subtitle])

print('All clips have been processed and logged in the CSV.')
