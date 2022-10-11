from azure.cosmos import  CosmosClient, PartitionKey

def cosmes_token():
    endpoint = "XXXX"
    key = 'XXXXX'
    client = CosmosClient(endpoint, key)
    database_name = 'Notify_Data'
    database = client.create_database_if_not_exists(id=database_name)
    container_name = 'Notify_access_token'
    container = database.create_container_if_not_exists(
        id=container_name,
        partition_key=PartitionKey(path="/access_token"),
        offer_throughput=400)
    query3 = "SELECT c.access_token FROM c "
    All_cosmes_token = list(container.query_items(query=query3, enable_cross_partition_query=True))
    return All_cosmes_token