import os
import glob
import re

def extract_and_print_annotation_values(directory_path: str):
    delimiter = 'TIER_ID'
    annotation_pattern = re.compile(r'<ANNOTATION_VALUE>(.*?)</ANNOTATION_VALUE>', re.DOTALL)
    brackets_pattern = re.compile(r'\[.*?\]')
    question_pattern = re.compile(r'\(\?\?\?\)')
    laughs_pattern = re.compile(r'\(laughs\)')
    caps_pattern = re.compile(r'\b[A-Z]+\b')  # To match words in all caps.

    def clean_values(annotation_values):
        unwanted_strings = ['eng', 'deu', 'amb', 'xxx', '#', '&amp;']

        cleaned = [brackets_pattern.sub('', value) for value in annotation_values]
        cleaned = [question_pattern.sub('', value) for value in cleaned]
        cleaned = [laughs_pattern.sub('', value) for value in cleaned]
        cleaned = [caps_pattern.sub('', value) for value in cleaned]
        cleaned = [value.replace('%', '') for value in cleaned]  # Remove % characters
        cleaned = [value.replace('\n', ' ') for value in cleaned]

        # Remove unwanted strings
        for unwanted in unwanted_strings:
            cleaned = [value.replace(unwanted, '') for value in cleaned]
        
        cleaned = [value.strip() for value in cleaned]  # Removing leading and trailing spaces.
        cleaned = [value for value in cleaned if value]  # filtering out empty strings
        return cleaned

    for foldername, subfolders, filenames in os.walk(directory_path):
        for filename in glob.glob(os.path.join(foldername, '*.eaf')):
            with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
                segments = content.split(delimiter)

                if len(segments) < 2:
                    print(f"Skipping {filename} as it doesn't contain enough segments")
                    continue  # skip files with less than 2 segments

                german_segments = []
                english_segments = []
                trash = []

                for i, segment in enumerate(segments, start=1):
                    annotation_values = annotation_pattern.findall(segment)
                    cleaned_annotation_values = clean_values(annotation_values)

                    # Displaying the cleaned_annotation_values
                    print(f"Annotation values: {cleaned_annotation_values}")

                    user_input = input("Press e for English, g for German, or t for Trash: ").strip().lower()
                    if user_input == 'e':
                        english_segments.extend(cleaned_annotation_values)
                        english_segments.append('\n')
                    elif user_input == 'g':
                        german_segments.extend(cleaned_annotation_values)
                        german_segments.append('\n')
                    elif user_input == 't':
                        trash.extend(cleaned_annotation_values)

                with open('german_translation.txt', 'a', encoding='utf-8') as output_file:
                    output_file.write(' '.join(german_segments))
                with open('english_original.txt', 'a', encoding='utf-8') as output_file:
                    output_file.write('\n'.join(english_segments))

if __name__ == "__main__":
    current_directory = os.getcwd()
    extract_and_print_annotation_values(current_directory)