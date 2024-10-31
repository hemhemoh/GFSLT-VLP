import os
import csv
import re

# Directory where your videos are stored
video_directory = 'bobsl_videos'

# Directory where your .vtt files are stored
subtitle_directory = 'bobsl_subtitles'

# Output CSV file
csv_file_path = 'video_subtitle_alignment.csv'

# CSV headers
csv_headers = ['Video Name', 'Start Time', 'End Time', 'Subtitle']

# Function to parse .vtt files
def parse_vtt_file(vtt_file_path):
    with open(vtt_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    entries = []
    buffer = []
    time_info = re.compile(r'(\d{2}:\d{2}:\d{2}.\d{3}) --> (\d{2}:\d{2}:\d{2}.\d{3})')

    for line in lines[1:]:  # Skip first line which is 'WEBVTT'
        if time_info.match(line.strip()):
            if buffer:
                entries.append(buffer)
                buffer = [line.strip()]
            else:
                buffer.append(line.strip())
        else:
            if line.strip() != '':
                buffer.append(line.strip())

    # Don't forget to add the last buffer
    if buffer:
        entries.append(buffer)

    # Convert buffer lists to tuple (Start Time, End Time, Subtitle)
    parsed_entries = []
    for entry in entries:
        start_time, end_time = entry[0].split(' --> ')
        subtitle_text = ' '.join(entry[1:])
        parsed_entries.append((start_time, end_time, subtitle_text))

    return parsed_entries

# Prepare CSV file
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(csv_headers)

    # Process each video and its corresponding .vtt file
    for video_file in os.listdir(video_directory):
        if video_file.endswith('.mp4'):
            base_name = os.path.splitext(video_file)[0]
            vtt_file_name = base_name + '.vtt'
            vtt_file_path = os.path.join(subtitle_directory, vtt_file_name)
            
            if os.path.exists(vtt_file_path):  # Check if the subtitle file exists
                # Use only the base name of the video file
                video_file_name = video_file  # This keeps only the filename without path
                subtitles = parse_vtt_file(vtt_file_path)
                
                for start_time, end_time, subtitle in subtitles:
                    # Write to CSV using just the video file name instead of the full path
                    csvwriter.writerow([video_file_name, start_time, end_time, subtitle])

print('CSV file has been created.')

