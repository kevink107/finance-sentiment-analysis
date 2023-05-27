import os
import requests
import time
import json

API_URL = "https://api-inference.huggingface.co/models/ProsusAI/finbert"
headers = {"Authorization": f"Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


def get_sentiments_json(directory): 
    WORDS_PER_CHUNK = 500
    sentiments = {}

    for file in os.listdir(directory):
        f = os.path.join(directory, file)

        if os.path.isfile(f):
            file_path = str(f)
            print(file_path)

            # opens one of the text files (e.g., Apple 10-K MD&A, Tesla 10-K Risks)
            with open(file_path, 'r') as text_file:
                words_read = 0
                
                # Initialize the variables to track scores and batches for each file
                running_score_positive = 0
                running_score_neutral = 0
                running_score_negative = 0
                num_batches = 0

                while True:
                    chunk = text_file.read(WORDS_PER_CHUNK)

                    if not chunk:
                        break

                    # print(chunk)
                    payload = {"text": chunk}
                    response = query(payload)

                    if 'error' in response and response['error'] == 'Model ProsusAI/finbert is currently loading':
                        estimated_time = response['estimated_time']
                        print(f"Model is loading. Retrying after {estimated_time} seconds...")
                        time.sleep(estimated_time + 10)
                        response = query(payload)
                    
                    print(response)

                    # Update the running scores for the current file
                    running_score_positive += response[0]['score']
                    running_score_neutral += response[1]['score']
                    running_score_negative += response[2]['score']
                    num_batches += 1

                    words_read += len(chunk.split())
                    if words_read >= WORDS_PER_CHUNK:
                        break

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

    # Save the JSON to a file
    output_file = "sentiments/" + str(directory) + "_sentiments.json"
    with open(output_file, 'w') as json_file:
        json.dump(sentiments, json_file, indent=4)


# get_sentiments_json('mda1')
# get_sentiments_json('mda2')
# get_sentiments_json('mda3')
# get_sentiments_json('risks1')
# get_sentiments_json('risks2')
get_sentiments_json('risks3')
