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
    
    user1 = 'john@microsoft.com'
    user2 = 'alice@microsoft.com'
    user3 = 'mark@microsoft.com'

    label1 = 'Confidential data'
    label2 = 'Credit Card data'
    label3 = 'License or credit card data'

    policy1 = gen_policy( user1, label1 )
    policy2 = gen_policy( user2, label2 )
    policy3 = gen_policy( user3, label3 )

    enterprise_data = readSampleDoc()


    if request.method == 'POST':
        user_input = request.form['user_input']
        puser_id = request.form['puser_id']
        print("puser_id: ", puser_id)
        ppolicy = request.form.get('ppolicy') 
        pstrict = request.form.get('pstrict')
        
        output = user_input
        orig_prompt = generate_prompt1(user_input, enterprise_data)
        if (puser_id == user1):
            sencheck_prompt= generate_prompt_sensitivity_check(label1, enterprise_data)
        elif (puser_id == user2):
            sencheck_prompt= generate_prompt_sensitivity_check(label2, enterprise_data)
        elif (puser_id == user3):
            sencheck_prompt= generate_prompt_sensitivity_check(label3, enterprise_data)
        else:
            puser_id = 'Any'
            sencheck_prompt= generate_prompt_sensitivity_check(label3, enterprise_data)
        
        senlist_prompt = generate_prompt_sensitivity_list(enterprise_data)
        writeprompttofile(orig_prompt)
        writesencheckprompttofile(sencheck_prompt)
        writesenlistprompttofile(senlist_prompt)

        print (senlist_prompt)
        #response = openai.Completion.create(
        #    model="text-davinci-003",
            #model="text-ada-001",
        #    prompt=senlist_prompt,
        #    max_tokens=100,
        #    temperature=0.6,
        #s)
        # output = url_for("index", result=response.choices[0].text)
        output = "no output"
        #print (" reponese choice - no of elements :", len(response['choices']))
        #if 'choices' in response:
        #    if len(response['choices']) > 0:
        #        output = response.choices[0].text
        #        print("ChatGPT outputlen , output ", len(output), output)
        #    else:
        #        print("response len 0")
        #else:
        #    print("Opps sorry, you beat the AI this time")

        #print(response)
        #json string data
        policy_string = '{"Action": "Deny", "operation": "Read", "classification": "Confidential", "user":"roshni@microsoft.com"}'

        #convert string to  object
        json_object = json.loads(policy_string)

        #check new data type
        print(type(json_object))

        return render_template('index.html', output=output, input=user_input, policy_object=json_object, puser_id=puser_id, ppolicy=ppolicy, pstrict=pstrict, policy1 = policy1, policy2 = policy2, policy3 = policy3)
    return render_template('index.html', policy1 = policy1, policy2 = policy2, policy3 = policy3)



def generate_prompt1(user_input, enterprise_data):
    return f""" {user_input} \nText: {enterprise_data}"""

def generate_prompt_sensitivity_check(label, enterprise_data):
    #sample_file = readSampleDoc()
    #return f"""Does the text include {label}? Output Y if yes and N if No.Do not include description \n\nText: {enterprise_data}"""
    return f"""Does the text include Sensitive data like license or credit card ? Output Y if yes and N if No.Do not include description \n\nText: {enterprise_data}"""

def generate_prompt_sensitivity_list(enterprise_data):
    #sample_file = readSampleDoc()
    return f"""Identify the sensitive data in the text and create a JSON with the type of sensitive data and the data value.do not include any description \n\nText: {enterprise_data}"""


def gen_policy(user_id, label):
    return f""" Only {user_id} must be able to access {label}"""

def generate_prompt_chat():
    example_messages = [
        {
            "role": "system",
            "content": "You are a helpful, pattern-following assistant that translates corporate jargon into plain English.",
        },
        {
            "role": "system",
            "name": "example_user",
            "content": "New synergies will help drive top-line growth.",
        },
        {
            "role": "system",
            "name": "example_assistant",
            "content": "Things working well together will increase revenue.",
        },
        {
            "role": "system",
            "name": "example_user",
            "content": "Let's circle back when we have more bandwidth to touch base on opportunities for increased leverage.",
        },
        {
            "role": "system",
            "name": "example_assistant",
            "content": "Let's talk later when we're less busy about how to do better.",
        },
        {
            "role": "user",
            "content": "This late pivot means we don't have time to boil the ocean for the client deliverable.",
        },
    ]
    print("example_messages: ", example_messages[0])       

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
