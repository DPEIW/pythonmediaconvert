import os
import subprocess


input_directory = r"(# Specify the directory containing the songs)"

output_format = "mp4"  # Replace this with the desired format


def convert_songs(directory):
    for filename in os.listdir(directory):
        current_path = os.path.join(directory, filename)
        if os.path.isfile(current_path):
            # Check if it's a song file
            if filename.endswith(".mov"):  # Replace with your current format
                output_filepath = os.path.splitext(current_path)[0] + "." + output_format
                try:
                    # Convert the song file
                    subprocess.run(["ffmpeg", "-i", current_path, output_filepath], check=True)
                    print(f"Converted {filename} to {output_format} successfully!")
                except subprocess.CalledProcessError as error:
                    print(f"Error converting {filename}: {error}")
        else:
            # Recursively convert files in subdirectories
            convert_songs(current_path)


convert_songs(input_directory)

print("Conversion complete!")
