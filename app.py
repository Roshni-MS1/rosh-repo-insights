import os
import app
import openai
import cosmoscmds
import json
from flask import Flask, redirect, render_template, request, url_for
import purconfig
import tiktoken
from purreaddocs import *


#openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = readopenaikey()
embed_model = "text-embedding-ada-002"
tokenizer = tiktoken.get_encoding('p50k_base')
#tokenizer = tiktoken.get_encoding("cl100k_base")


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    

    policy_list = readPolicyList()

    if request.method == 'POST':
        user_input = request.form['user_input']
        
        output = user_input
        orig_prompt = generate_prompt1(user_input, policy_list) 
       
        writeprompttofile(orig_prompt)
        print (orig_prompt)

        response = openai.Completion.create(
            model="text-davinci-003",
            #model="text-ada-001",
            prompt=orig_prompt,
            max_tokens=100,
            temperature=0.6,
        )
        # output = url_for("index", result=response.choices[0].text)
        output = "no output"
        print (" response choice - no of elements :", len(response['choices']))
        if 'choices' in response:
            if len(response['choices']) > 0:
                output = response.choices[0].text
                print("ChatGPT outputlen , output ", len(output), output)
            else:
                print("response len 0")
        else:
            print("Opps sorry, you beat the AI this time")

        #print(response)
       

        return render_template('index.html', output=output, input=user_input)
    return render_template('index.html')


def generate_prompt1(user_input, policy_list):
    return f"""{user_input} \n
Example of a policy : 
{{\"Action\": \"Deny\", \"operation\": \"Read\", \"classification\": \"PII\", \"user\":\"alice@microsoft.com\",\"datasource\" : \"sql\"}}

List of all policies:
{policy_list}"""



#def generate_embeddings(text):
#    return openai.Embedding.create(
#        input=text, model="text-embedding-ada-002"
#    )["data"][0]["embedding"]

 #   len(embedding)


if __name__ == '__main__':
    app.run()



# Print response iteratively
#response = requests.get('<URL>')
#data = response.json()

#for key, value in data.items():
#    print(f'{key}: {value}')
