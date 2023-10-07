import os
import glob
import re

def extract_and_print_annotation_values(directory_path: str):
    delimiter = 'TIER_ID="Translation Speaker'
    annotation_pattern = re.compile(r'<ANNOTATION_VALUE>(.*?)</ANNOTATION_VALUE>', re.DOTALL)
    brackets_pattern = re.compile(r'\[.*?\]')
    question_pattern = re.compile(r'\(\?\?\?\)')
    laughs_pattern = re.compile(r'\(laughs\)')

    for foldername, subfolders, filenames in os.walk(directory_path):
        for filename in glob.glob(os.path.join(foldername, '*.txt')):
            with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
                segments = content.split(delimiter)
                
                if len(segments) < 2:
                    print(f"Skipping {filename} as it doesn't contain enough segments")
                    continue  # skip files with less than 2 segments
                
                german_segments = []
                english_segments = []

                for i, segment in enumerate(segments, start=1):
                    annotation_values = annotation_pattern.findall(segment)
                    cleaned_annotation_values = [brackets_pattern.sub('', value) for value in annotation_values]
                    cleaned_annotation_values = [question_pattern.sub('', value) for value in cleaned_annotation_values]
                    cleaned_annotation_values = [laughs_pattern.sub('', value) for value in cleaned_annotation_values]
                    cleaned_annotation_values = [value.replace('\n', ' ') for value in cleaned_annotation_values]
                    cleaned_annotation_values = [value for value in cleaned_annotation_values if value]  # filtering out empty strings

                    if i % 2 != 0:  # Assuming odd segments are in German
                        german_segments.extend(cleaned_annotation_values)
                    else:  # Assuming even segments are in English
                        english_segments.extend(cleaned_annotation_values)

                with open('german_translation.txt', 'w', encoding='utf-8') as output_file:
                    output_file.write('\n'.join(german_segments))
                with open('english_original.txt', 'w', encoding='utf-8') as output_file:
                    output_file.write('\n'.join(english_segments))

if __name__ == "__main__":
    current_directory = os.getcwd()
    extract_and_print_annotation_values(current_directory)
