import pinecone
from tqdm.auto import tqdm
import datetime
from time import sleep

 #pinecone initialize index
 def purpineconeinitindex():
    index_name = 'gpt-4-langchain-docs'

    # initialize connection to pinecone
    pinecone.init(
        api_key="PINECONE_API_KEY",  # app.pinecone.io (console)
        environment="PINECONE_ENVIRONMENT"  # next to API key in console
    )

    # check if index already exists (it shouldn't if this is first time)
    if index_name not in pinecone.list_indexes():
        # if does not exist, create index
        pinecone.create_index(
            index_name,
            dimension=len(res['data'][0]['embedding']),
            metric='dotproduct'
        )
    # connect to index
    index = pinecone.GRPCIndex(index_name)
    # view index stats
    index.describe_index_stats()


#Add vectors to Pinecone
def purpineconeaddvectors(chunks):
    batch_size = 100  # how many embeddings we create and insert at once

    for i in tqdm(range(0, len(chunks), batch_size)):
        # find end of batch
        i_end = min(len(chunks), i+batch_size)
        meta_batch = chunks[i:i_end]
        # get ids
        ids_batch = [x['id'] for x in meta_batch]
        # get texts to encode
        texts = [x['text'] for x in meta_batch]
        # create embeddings (try-except added to avoid RateLimitError)
        try:
            res = openai.Embedding.create(input=texts, engine=embed_model)
        except:
            done = False
            while not done:
                sleep(5)
                try:
                    res = openai.Embedding.create(input=texts, engine=embed_model)
                    done = True
                except:
                    pass
        embeds = [record['embedding'] for record in res['data']]
        # cleanup metadata
        meta_batch = [{
            'text': x['text'],
            'chunk': x['chunk'],
            'url': x['url']
        } for x in meta_batch]
        to_upsert = list(zip(ids_batch, embeds, meta_batch))
        # upsert to Pinecone
        index.upsert(vectors=to_upsert)



#Retrieve vectors from Pinecone
def purpineconeretrievevectors(query):

    res = openai.Embedding.create(
        input=[query],
        engine=embed_model
    )

    # retrieve from Pinecone
    xq = res['data'][0]['embedding']

    # get relevant contexts (including the questions)
    res = index.query(xq, top_k=5, include_metadata=True)