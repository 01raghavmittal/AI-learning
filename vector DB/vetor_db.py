import chromadb
chroma_client = chromadb.Client()


# create collection --> Collections are where you'll store your embeddings, documents, and any additional metadata. Collections index your embeddings and documents, and enable efficient retrieval and filtering.

collection = chroma_client.create_collection(name="my_collection")

document=[
        "This is a document about pineapple",
        "This is a document about oranges",
        "This is a document about Apples"
    ]

# Add file into collection
collection.add(
    ids=["id1", "id2","id3"],
    documents=document

)

# Query the collection
results = collection.query(
    query_texts=["This is a query document about hawaii"], # Chroma will embed this for you
    n_results=4 # how many results to return by default it is 10
)


print(results)




