import os
import pickle
import pandas as pd

# Load the data with a column for video paths
data = pd.read_csv("data/How2Sign/how2sign_realigned_train.csv", sep='\t')
how2sign_train = {}
# Define the input and output paths and file extension
# videos_folder_path = "data/How2Sign/raw_videos/"
frames_folder_path = "data/How2Sign/Frames/train/"
# ext = "mp4"
# count = 0

# Loop over each row of the data
for index, row in data.iterrows():
    # Extract the video name from the csv
    video_name = row["SENTENCE_NAME"]
    # video_path = videos_folder_path + video_name + ".mp4"
    # Define the output directory for the frames
    frames_path = os.path.join(frames_folder_path, video_name)
    # Create the output directory if it doesn't exist
    os.makedirs(frames_path, exist_ok=True)
    # Define the full path to the output frame files
    output_file_pattern = os.path.join(frames_path, "%05d.jpg")
    # Define the command to extract the frames
    ffmpeg_path = "/usr/bin/ffmpeg" 
    command = f'{ffmpeg_path} -i "{video_path}" -filter:v fps=30 "{output_file_pattern}"'
    # Execute the command
    if len(os.listdir(frames_path)) == 0:
     os.system(command)
     os.remove(video_path)
    else:
        print("Images already extracted")
        count += 1

    # Update the row with the output directory for the frames
    data.at[index, "frames_features"] = os.path.join("Frames/train", video_name)

    d = {
            'name': video_name,
            'gloss': row["SENTENCE"],
            'text': row["SENTENCE"],
            'length': len(os.listdir(frames_path)),
            'imgs_path': [os.path.join(frames_path, i) for i in os.listdir(frames_path)]
    }
    how2sign_train[video_name] = d 

# data/How2Sign/how2sign_train.pickle
# Save the dictionary of dictionaries to the pickle file
with open("how2sign_train.pickle", "wb") as f:
    pickle.dump(how2sign_train, f)

# Save the updated data to a new file
data.to_csv("how2sign_with_frames_train.csv", index=False)