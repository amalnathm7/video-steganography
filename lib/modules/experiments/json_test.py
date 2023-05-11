import json

selected_frames = []
for i in range(0, 300):
    selected_frames.append(i)

selected_regions = {}

for i in range(1, 300):
    selected_regions[i] = []
    for j in range(0, 396):
        selected_regions[i].append((j, j))

data = {
    'f': selected_frames,
    'r': selected_regions
}

# Specify the file path where you want to save the JSON file
file_path = 'data.json'

# Open the file in write mode
with open(file_path, 'w') as json_file:
    # Write the dictionary as JSON to the file
    json.dump(data, json_file)

print('JSON file created successfully.')