from azure.cosmos import  CosmosClient, PartitionKey

class DB:
    # 把tokn存起來，才能用此token發送訊息
    def save_data(data):
        # Initialize the Cosmos client
        endpoint = "https://XXXXX"
        key = 'XXXXXXX'
        # <create_cosmos_client>
        client = CosmosClient(endpoint, key)
        # </create_cosmos_client>
        # Create a database
        # <create_database_if_not_exists>
        database_name = 'Notify_Data'
        database = client.create_database_if_not_exists(id=database_name)
        # </create_database_if_not_exists>
        # Create a container
        # Using a good partition key improves the performance of database operations.
        # <create_container_if_not_exists>
        container_name = 'Notify_access_token'
        container = database.create_container_if_not_exists(
            id=container_name,
            partition_key=PartitionKey(path="/access_token"),
            offer_throughput=400)
        container.create_item(body=data)

