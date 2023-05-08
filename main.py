import streamlit as st
import json
import requests

'''# HEllO ''' 

URI = 'https://oobabooga.chris-mckinley.website/api/v1/generate'

headers = {
    'CF-Access-Client-Id': st.secrets["clientID"],
    'CF-Access-Client-Secret': st.secrets["clientSecret"]
}

with st.sidebar:
    temperature = st.slider('Temperature', min_value = 0.01, max_value = 1.99, step = 0.01, value = 0.7, help = 'Randomness of sampling. High values can increase creativity but may make text less sensible. Lower values will make text more predictable but can become repetitious')
    max_new_tokens = st.slider('Token length', min_value = 1, max_value = 2000, step = 1, value = 250, help = 'Number of tokens to generate. (4 characters is about one token)')
    prompt = st.text_area('Enter Custom Prompt', help = 'You will get much better output if you provide examples of what you expect back.')
# prompt = "In order to make homemade bread, follow these steps:\n1)"

if st.button('Generate Text'):
    request = {
        'prompt': prompt,
        'max_new_tokens': max_new_tokens,
        'do_sample': True,
        'temperature': temperature,
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
            st.markdown(f"Error parsing response: {e}")
            st.markdown(response.text)
    elif response.status_code == 404:
        st.markdown('404: Not Found')

    elif response.status_code == 401:
        st.markdown('Denied: Check your API key')
    else:
        st.markdown(f"Unexpected status code: {response.status_code}")