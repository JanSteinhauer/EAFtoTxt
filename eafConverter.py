import os
import glob
import re

delimiters = [
    'TIER_ID="TRANSCRIPTION_Speaker', 
    'TIER_ID="Tokenization_Speaker', 
    'TIER_ID="Language_Speaker', 
    'TIER_ID="Normalization_Speaker', 
    'TIER_ID="LEMMA_Speaker', 
    'TIER_ID="POS_Speaker', 
    'TIER_ID="TRANSCRIPTION_Interviewer', 
    'TIER_ID="Tokenization_Interviewer', 
    'TIER_ID="Language_Interviewer', 
    'TIER_ID="Normalization_Interviewer', 
    'TIER_ID="LEMMA_Interviewer', 
    'TIER_ID="POS_Interviewer', 
    'TIER_ID="TRANSLATION_Speaker', 
    'TIER_ID="TRANSLATION_Interviewer'
]

def extract_and_print_annotation_values(directory_path: str):
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
        cleaned = [value.replace('%', '') for value in cleaned]
        cleaned = [value.replace('\n', ' ') for value in cleaned]

        for unwanted in unwanted_strings:
            cleaned = [value.replace(unwanted, '') for value in cleaned]

        cleaned = [value.strip() for value in cleaned]
        cleaned = [value for value in cleaned if value]
        return cleaned

    german_segments = []
    german_segments_sentences = []
    english_segments = []

    def split_by_delimiters(content, delimiters):
        segments = [content]  # Start with the whole content as one segment
        for delimiter in delimiters:
            pieces = []
            for segment in segments:
                pieces.extend(segment.split(delimiter))
            segments = pieces
        return segments

    for foldername, subfolders, filenames in os.walk(directory_path):
        for filename in glob.glob(os.path.join(foldername, '*.eaf')):
            with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
                segments = split_by_delimiters(content, delimiters)

                if len(segments) < 2:
                    print(f"Skipping {filename} as it doesn't contain enough segments")
                    continue
                print(len(segments))
               
 

                for i, segment in enumerate(segments, start=1):
                    annotation_values = annotation_pattern.findall(segment)
                    cleaned_annotation_values = clean_values(annotation_values)


                    if (i == 2) ^ (i == 8):
                        german_segments_sentences.extend(cleaned_annotation_values)
                        german_segments_sentences.append('\n')
                    if i in [2, 3, 5, 6, 8, 9, 11, 12]:
                        german_segments.extend(cleaned_annotation_values)
                        german_segments.append('\n')
                    if i in [14,15]:
                        english_segments.extend(cleaned_annotation_values)
                        english_segments.append('\n')

    with open('german_translation.txt', 'a', encoding='utf-8') as output_file:
        output_file.write(' '.join(german_segments))
    with open('german_sentence_translation.txt', 'a', encoding='utf-8') as output_file:
        output_file.write(' '.join(german_segments_sentences))
    with open('english_translation.txt', 'a', encoding='utf-8') as output_file:
        output_file.write(' '.join(english_segments))

if __name__ == "__main__":
    current_directory = os.getcwd()
    extract_and_print_annotation_values(current_directory)
