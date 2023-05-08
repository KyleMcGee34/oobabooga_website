import streamlit as st
import json
import requests

'''# HEllO ''' 

URI = 'https://oobabooga.chris-mckinley.website/api/v1/generate'

headers = {
    'CF-Access-Client-Id': st.secrets["clientID"],
    'CF-Access-Client-Secret': st.secrets["clientSecret"]
}

prompt = "In order to make homemade bread, follow these steps:\n1)"

request = {
    'prompt': prompt,
    'max_new_tokens': 250,
    'do_sample': True,
    'temperature': 1.3,
    'top_p': 0.1,
    'typical_p': 1,
    'repetition_penalty': 1.18,
    'top_k': 40,
    'min_length': 0,
    'no_repeat_ngram_size': 0,
    'num_beams': 1,
    'penalty_alpha': 0,
    'length_penalty': 1,
    'early_stopping': False,
    'seed': -1,
    'add_bos_token': True,
    'truncation_length': 2048,
    'ban_eos_token': False,
    'skip_special_tokens': True,
    'stopping_strings': []
}

response = requests.post(URI, json=request, headers=headers)

if response.status_code == 200:
    try:
        json_data = json.loads(response.text)
        result = json_data['results'][0]['text']
        st.markdown(prompt + result)
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error parsing response: {e}")
        print(response.text)
elif response.status_code == 404:
    print('404: Not Found')

elif response.status_code == 401:
    print('Denied: Check your API key')
else:
    print(f"Unexpected status code: {response.status_code}")