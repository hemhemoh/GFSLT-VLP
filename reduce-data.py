import pickle
import random

# Load the pickle file (assuming it's a dictionary)
with open('data/How2Sign/h2s_test.pickle', 'rb') as f:  # Replace with your file path
    data = pickle.load(f)

# Print the original number of items
print(len(data))

# Randomly select 7096 items from the dictionary
sampled_keys = random.sample(data.keys(), 642)
sampled_data = {key: data[key] for key in sampled_keys}

# Save the sampled data to a new pickle file
with open('data/How2Sign/h2s_reduced_test.pickle', 'wb') as f: 
    pickle.dump(sampled_data, f)

print(f"Sampled data saved with {len(sampled_data)} items.")
