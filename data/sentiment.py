import os
import requests
import time
import json

API_URL = "https://api-inference.huggingface.co/models/ProsusAI/finbert"
headers = {"Authorization": f"Bearer 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"}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


def remove_special_characters(file_path):
    # Read the file
    with open(file_path, 'r') as file:
        text = file.read()

    # Remove special characters
    clean_text = text.replace("&#160;", "")
    clean_text = clean_text.replace("&#8217;", "'")
    clean_text = clean_text.replace("&#8220;", "\"")
    clean_text = clean_text.replace("&#8221;", "\"")
    clean_text = clean_text.replace("&#8226;", "")
    clean_text = clean_text.replace("&#8482;", "")
    clean_text = clean_text.replace("&#38;", "&")
    clean_text = clean_text.replace("&#8221;", "\"")
    clean_text = clean_text.replace("&#174;", "")
    clean_text = clean_text.replace("&#8203;", "")
    clean_text = clean_text.replace("&#8212;", "")

    # Write the cleaned text back to the file
    with open(file_path, 'w') as file:
        file.write(clean_text)


def clean_up_files(directory):
    for file in os.listdir(directory):
        f = os.path.join(directory, file)

        if os.path.isfile(f):
            file_path = os.path.abspath(f)
            print("FILE PATH: " + file_path)

            remove_special_characters(file_path)


def get_sentiments_json(directory, file): 
    CHARS_PER_CHUNK = 1000
    sentiments = {}
    f = os.path.join(directory, file)

    if os.path.isfile(f):
        file_path = str(f)
        print("FILE PATH: " + file_path)

        # Read file to get total words 
        with open(file_path, 'r') as file_copy:
            total_words = len(file_copy.read().split())
            print(total_words)

        # Open file for sentiment analysis
        with open(file_path, 'r') as text_file:
            words_read = 0

            # Initialize variables to track scores and batches for each file
            running_score_positive = 0
            running_score_neutral = 0
            running_score_negative = 0
            num_batches = 0

            while words_read <= total_words:
                chunk = text_file.read(CHARS_PER_CHUNK)
                print("WORDS READ: " + str(words_read) + "/" + str(total_words))

                if not chunk:
                    print("ERROR: not chunk (line 45)")
                    break

                payload = {"text": chunk}
                response = query(payload)

                if 'error' in response and response['error'] == 'Model ProsusAI/finbert is currently loading':
                    estimated_time = response['estimated_time']
                    print(f"Model is loading. Retrying after {estimated_time} seconds...")
                    time.sleep(estimated_time + 10)
                    response = query(payload)

                print(chunk)

                # Update the running scores for the current file
                running_score_positive += response[0]['score']
                running_score_neutral += response[1]['score']
                running_score_negative += response[2]['score']
                num_batches += 1

                words_read += len(chunk.split())

                print(response)
                
                print("-----------------------")
                print("\n")

            # Calculate the average scores for the current file
            avg_positive = running_score_positive / num_batches
            avg_neutral = running_score_neutral / num_batches
            avg_negative = running_score_negative / num_batches

            # Create the JSON structure for the current file
            file_name = os.path.splitext(file)[0]
            file_entry = {
                "running_score_positive": running_score_positive,
                "running_score_neutral": running_score_neutral,
                "running_score_negative": running_score_negative,
                "chunks": num_batches,
                "avg_positive": avg_positive,
                "avg_neutral": avg_neutral,
                "avg_negative": avg_negative
            }
            sentiments[file_name] = file_entry

    print(file)
    # Save the JSON to a file
    output_file = os.path.join(f"sentiments/{directory}", f"{file}_sentiments.json")
    with open(output_file, 'w') as json_file:
        json.dump(sentiments, json_file, indent=4)


if __name__ == "__main__":
    # Run the two lines below to clean up the files and get rid of special characters
    # clean_up_files('mda_2021')
    # clean_up_files('risks_2021')

    # Below: first parameter is just the folder of the file; second is the file name
    get_sentiments_json(directory='risks_2021', file='V_risks_2021')
    get_sentiments_json(directory='risks_2021', file='WMT_risks_2021')
    pass
