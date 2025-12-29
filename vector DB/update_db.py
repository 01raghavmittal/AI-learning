import chromadb

client =chromadb.PersistentClient()

Collection = client.get_or_create_collection("my_collection")

new_docs = ["This is a new document.", "Another new doc"]
new_ids = ["1001", "1002"]


