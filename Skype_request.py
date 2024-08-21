import requests
import pandas as pd


token_file='Skype_token.txt'
if os.path.exists(token_file):
  with open(token_file, 'r') as f:
    Skype_token = f.read().strip()
else:
  raise FileNotFoundError("Token file not found")

# Define the URL and headers for the POST request
url = 'https://msgsearch.skype.com/v2/query'
headers = {
    'accept': 'application/json',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'connection': 'keep-alive',
    'content-type': 'application/json',
    'host': 'msgsearch.skype.com',
    'origin': 'https://web.skype.com',
    'pragma': 'no-cache',
    'referer': 'https://web.skype.com/',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'x-ms-correlation-id': '29a5a63552e546c6bab652495b76af74',
    'x-skypetoken': f'{Skype_token}'
}

# Load the Excel file
input_file = 'Reaction_content.xlsx'  # Replace with your Excel file path
df = pd.read_excel(input_file)
print(df.columns)

# Process each row
for index, row in df.iterrows():
    content = row['Content']
    payload = {
        "OPTION": {
            "RESULTBASE": 0,
            "RESULTCOUNT": 40
        },
        "QUERYSTRING": {
            "AND": [
                {
                    "OR": [
                        {"Content": content}
                    ]
                },
                {"ThreadId": "19:176e12cbc383446da407c30a64cd88cf@thread.skype"}
            ]
        }
    }

    # Send the POST request
    response = requests.post(url, json=payload, headers=headers)
    print(f'Processing content {content}')
    
    if response.status_code == 200:
        data = response.json()

        # Initialize variables
        user_count = 0
        user_values = set()

        # Iterate through each message
        for message in data:
            # Iterate through each MetadataList entry
            for metadata in message.get('MetadataList', []):
                # Check if MetadataType is not 'reactionsConsumptionHorizon'
                if metadata.get('MetadataType') != 'reactionsConsumptionHorizon':
                    # Iterate through each MetadataPropertyList entry
                    for property in metadata.get('MetadataPropertyList', []):
                        if property.get('Key') == 'user':
                            # Count occurrences
                            user_count += 1
                            # Add distinct values with '8:' removed
                            user_value = property.get('Value')
                            if user_value.startswith('8:'):
                                user_value = user_value[2:]  # Remove '8:'
                            user_values.add(user_value)

        # Update the DataFrame with results
        df.at[index, 'num_react'] = user_count
        df.at[index, 'num_people'] = len(user_values)

    else:
        print(f"Request failed for content '{content}' with status code: {response.status_code}")

# Save the updated DataFrame to a new Excel file
output_file = 'output.xlsx'  # Replace with your desired output file path
df.to_excel(output_file, index=False)

print("Processing complete. Results saved to:", output_file)


# import requests
# import json
# import pandas as pd

# # Define the URL and payload
# url = 'https://msgsearch.skype.com/v2/query'
# payload = {
#     "OPTION": {
#         #fetch from begining (result bas: 0)
#         "RESULTBASE": 0,
#         #fetch 40 results maximum
#         "RESULTCOUNT": 40},
#     "QUERYSTRING": {
#         "AND": [
#             {"OR": [
#                 {"Content": "[Summer Trip] THÔNG BÁO DI CHUYỂN VÀ CHUẨN BỊ CHO CHUYẾN ĐI"},
#             ]},
#             {"ThreadId": "19:176e12cbc383446da407c30a64cd88cf@thread.skype"}
#         ]
#     }
# }

# # Define the headers
# headers = {
#     'accept': 'application/json',
#     'accept-encoding': 'gzip, deflate, br, zstd',
#     'accept-language': 'en-US,en;q=0.9',
#     'cache-control': 'no-cache',
#     'connection': 'keep-alive',
#     'content-length': str(len(json.dumps(payload))),  # Automatically compute content-length
#     'content-type': 'application/json',
#     'host': 'msgsearch.skype.com',
#     'origin': 'https://web.skype.com',
#     'pragma': 'no-cache',
#     'referer': 'https://web.skype.com/',
#     'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
#     'sec-fetch-dest': 'empty',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'same-site',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
#     'x-ms-correlation-id': '29a5a63552e546c6bab652495b76af74',
#     'x-skypetoken': 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjYwNUVCMzFEMzBBMjBEQkRBNTMxODU2MkM4QTM2RDFCMzIyMkE2MTkiLCJ4NXQiOiJZRjZ6SFRDaURiMmxNWVZpeUtOdEd6SWlwaGsiLCJ0eXAiOiJKV1QifQ.eyJpYXQiOjE3MjQyMDMzNzQsImV4cCI6MTcyNDI4OTc3NCwic2t5cGVpZCI6ImxpdmU6LmNpZC5lYWQ1ZDFkNWMwNGVlYjU3Iiwic2NwIjo5NTYsImNzaSI6IjE3MjQyMDMzNzQiLCJjaWQiOiJlYWQ1ZDFkNWMwNGVlYjU3IiwiYWF0IjoxNzIzOTc4Mjc3fQ.jgEloxkELruPDYLt0n1kTJqkNvui72cHky7e6mQ3HpjmG7vJnx9nIKG5-23oh7m_3u9L-uaLUSlhOxDPd26HkoLlMKXxjTznC7rMXbzRibZcYnG6zL14l2Ls6Imd8eUc8jtyg8uUaTS3dT0LUtgLenOEnS6xfuyA7rfl2swcwaujZTsi67eR_madn8yvvQflq_C1D4WxkLFrnKs-nJFakcPgz9KQZ7Vd3i5pSn4OezZ-k9PJ1ztzILLwG_8bqUvAXh8kAkBqCCSf-Zvdhx8fttGk4T4wPwkS2BOLlF_yUIToM7REhnwfXXOqNF-msPHRjGiF69Pa6EDPH7D1zngEgg'
# }

# # Send the POST request
# response = requests.post(url, json=payload, headers=headers)
# # Load the Excel file
# input_file = 'input.xlsx'  # Replace with your Excel file path
# df = pd.read_excel(input_file)


# # Check if the request was successful
# if response.status_code == 200:
#     data = response.json()
#     # Save the JSON response to a file
#     with open('response.json', 'w') as file:
#         json.dump(response.json(), file, indent=4)
#     print("Response saved to 'response.json'")

#     # Initialize variables
#     user_count = 0
#     user_values = set()

#     # Iterate through each message
#     for message in data:
#         # Iterate through each MetadataList entry
#         for metadata in message.get('MetadataList', []):
#             # Check if MetadataType is 'user'
#             if metadata.get('MetadataType'):
#               if metadata.get('MetadataType') != 'reactionsConsumptionHorizon':
#                 # Iterate through each MetadataPropertyList entry
#                 for property in metadata.get('MetadataPropertyList', []):
#                     if property.get('Key') == 'user':
#                         # Count occurrences
#                         user_count += 1
#                         # Add distinct values
#                         user_value = property.get('Value')
#                         user_value = user_value[2:]  # Remove '8:'
#                         # user_values.add(property.get('Value'))
#                         user_values.add(user_value)

#     # Output results
#     print(f"Total number reactions: {user_count}")
#     print(f"Distinct user reacted: {len(user_values)}")
#     print(f"Distinct 'user' values list: {list(user_values)}")

# else:
#     print(f"Request failed with status code: {response.status_code}")

