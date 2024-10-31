import os
import cv2
import pickle


# Load the original pickle file
with open("data/How2Sign/how2sign_train.pickle", "rb") as f:
    data = pickle.load(f)

# Check the number of entries before filtering
print(f"Number of entries before filtering: {len(data)}")

# Remove entries where the length of imgs_path is 0
filtered_data = {k: v for k, v in data.items() if len(v.get('imgs_path', [])) > 0}

# Check the number of entries after filtering
print(f"Number of entries after filtering: {len(filtered_data)}")

# Modify the 'imgs_path' entries to remove the specified prefix
for key, value in filtered_data.items():
    value['imgs_path'] = [img_path.replace("data/How2Sign/", "") for img_path in value['imgs_path']]
    # if 'imgs_path' in value:
    #     # Update each path in the list by removing the prefix
        # value['imgs_path'] = [img_path.replace("data/How2Sign", "") for img_path in value['imgs_path']]

# Save the modified dictionary back to a new pickle file
with open("data/How2Sign/h2s_train.pickle", "wb") as f:
    pickle.dump(filtered_data, f)

print(filtered_data['_-adcxjm1R4_1-8-rgb_front']['imgs_path'])
print("Filtered and modified pickle file saved successfully.")


# # Load your data
# with open("data/How2Sign/h2s_train_sample.pickle", "rb") as f:
#     data = pickle.load(f)

# base_path = "data/How2Sign/Frames/"
# declined = set()

# # Iterate over the dictionary of dictionaries
# for key, inner_dict in data.items():
#     if 'imgs_path' in inner_dict:
#         img_paths = inner_dict['imgs_path']
#         if isinstance(img_paths, list): 
#             # Prepend base path to each image path
#             inner_dict['imgs_path'] = [os.path.join(base_path, img_path) for img_path in img_paths]
            
#             # Check each image path
#             for img_path in inner_dict['imgs_path']:
#                 image = cv2.imread(img_path)               
#                 # If an image is empty or cannot be read, log the key and move to the next key
#                 if image is None:
#                     print(f"Image at {img_path} (key: {key}) is empty or cannot be read.")
#                     declined.add(key)
#                     break  # Move to the next key as soon as an empty image is found
# print(declined)




# import os
# import cv2

# # Specify the root directory containing the subdirectories with images
# root_directory = 'data/How2Sign/Frames/train'
# rotten_dir = []
# # Walk through all subdirectories and files
# for subdir, dirs, files in os.walk(root_directory):
#     for filename in files:
#         if filename.endswith(".jpg"):
#             file_path = os.path.join(subdir, filename)
            
#             # Attempt to read the image
#             image = cv2.imread(file_path)
            
#             # Check if the image is empty or could not be read
#             if image is None:
#                 print(f"Image {file_path} is empty or cannot be read.")
#                 rotten_dir.append(files)
#             # else:
#                 # print(f"Image {filename} is good.")
#         else:
#             print(filename)
# print(set(rotten_dir))
