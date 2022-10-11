from azure.cosmos import  CosmosClient, PartitionKey

endpoint = "XXXXX"
key = 'XXXXXXX'

client = CosmosClient(endpoint, key)
database_name = 'Notify_Data'
database = client.create_database_if_not_exists(id=database_name)
container_name = 'Notify_access_token'
container = database.create_container_if_not_exists(
    id=container_name,
    partition_key=PartitionKey(path="/access_token"),
    offer_throughput=400)

def delete_token_from_cosmes(access_token):
    query = "SELECT * FROM c WHERE c.access_token IN ( '%s' )"%(access_token)
    items = list(container.query_items(
    query=query,
    enable_cross_partition_query=True
    ))
    print(items)
    for doc in items:
        container.delete_item(item=doc.get('id'),partition_key=doc.get('access_token'))
    print("Success delete")

delete_token_from_cosmes("XXXXXXXX")

