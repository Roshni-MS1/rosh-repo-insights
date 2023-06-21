input purembeddings
input purvectors
input purpinecone
input purreaddocs



# get list of retrieved text
# items retrieved from pinecone 
def getContentsFromVector():
    contexts = [item['metadata']['text'] for item in res['matches']]

    augmented_query = "\n\n---\n\n".join(contexts)+"\n\n-----\n\n"+query
     print(augmented_query)


def purRAGconfigure():
    #initialize    
    configureTextSplitter()
    purpineconeinitindex()


    #Load Vector DB 
    datalist = readInputDocs()
   
    for data in datalist({
            chunklist = splitContentsIntoChunks(data)
            for chunk in chunklist({
                    response = purcreateembeddings(chunk)

                    # no of data elements
                    len(response[data])
                    #length of structure of data
                    len(response['data'][0]['embedding']), len(response['data'][1]['embedding'])
                    
                        purpineconeaddvectors (response[data])
    
                })
        })
   
  
 

def purRAGinput():
   purpineconeretrievevectors(query)




   