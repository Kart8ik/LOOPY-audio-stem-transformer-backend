import subprocess
import os

def separate_vocals(input_file, output_dir='separated', model='mdx_extra'):
    assert os.path.exists(input_file), "Input file doesn't exist"
    
    cmd = [
        "demucs",
        "--mp3",
        "--two-stems", "vocals",
        "-n", model,
        input_file,
        "--out", output_dir
    ]
    subprocess.run(cmd, check=True)

# # Usage
# separate_vocals("blue.mp3")