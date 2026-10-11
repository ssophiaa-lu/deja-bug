from fastembed import TextEmbedding
model = TextEmbedding("BAAI/bge-small-en-v1.5")
print(len(list(model.embed(["React app crashes when loading user data"]))[0]))