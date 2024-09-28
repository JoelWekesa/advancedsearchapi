import os
import json
import time
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import JSONLoader
from langchain_postgres import PGVector
from dotenv import load_dotenv
from search.read_ids import read_collection_ids

load_dotenv()

jq_schema='.[] | {id: .id, title: .title, overview: .overview, genres: .genres, poster: .poster, release_date: .release_date}'

loader = JSONLoader(
    file_path='./movies.json',
    jq_schema=jq_schema,
    text_content=False,
)

data = loader.load()



model_name = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}
embedding_function = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

vector_store = PGVector(
    embeddings=embedding_function,
    collection_name=os.environ["COLLECTION_NAME"],
    connection=os.environ["DB_CONNECTION_STRING"],
    use_jsonb=True,
)


def add_to_db_in_batches(batch_size=100):
    existing_ids = read_collection_ids()

    data_ids = [str(json.loads(item.page_content)["id"]) for item in data]

    new_ids = list(set(data_ids) - set(existing_ids))


    # print(new_ids)


    if len(new_ids) > 0:
        new_documents = [item for item in data if json.loads(item.page_content)["id"] in new_ids]


        total_products = len(new_documents)
        start_time = time.time()  # Start the timer
        
        for i in range(0, total_products, batch_size):
            batch_data = new_documents[i:i + batch_size]
            ids = [json.loads(item.page_content)["id"] for item in batch_data]
            vector_store.add_documents(batch_data, ids=ids)
            remaining = total_products - (i + len(batch_data))
            
            elapsed_time = time.time() - start_time
            batches_processed = (i // batch_size) + 1
            average_time_per_batch = elapsed_time / batches_processed if batches_processed > 0 else 0
            estimated_remaining_batches = (total_products // batch_size) - batches_processed
            estimated_remaining_time = average_time_per_batch * estimated_remaining_batches
            
            # Format estimated remaining time
            estimated_remaining_time_minutes = estimated_remaining_time // 60
            estimated_remaining_time_seconds = estimated_remaining_time % 60
            
            print(f'Added products {i + 1} to {min(i + len(batch_data), total_products)} to the database. '
                f'Remaining: {remaining}. Estimated remaining time: {int(estimated_remaining_time_minutes)} minutes and {int(estimated_remaining_time_seconds)} seconds.')

    else:
        pass