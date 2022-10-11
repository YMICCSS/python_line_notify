# 紀錄客戶 follow 的資料
# 建立 cosmes 資料庫連結初始狀態
from datetime import datetime
from azure.cosmos import  CosmosClient, PartitionKey
import requests
from get_token import cosmes_token

# 取得時間
today_str = datetime.now().strftime('%Y-%m-%d')
today_list = today_str.split("-")
today_timestamp = int(datetime(int(today_list[0]), int(today_list[1]), int(today_list[2])).timestamp())
yesterday_start_timestamp = int(datetime(int(today_list[0]), int(today_list[1]), int(today_list[2])-1).timestamp())
yesterday_end_timestamp = int(datetime(int(today_list[0]), int(today_list[1]), int(today_list[2])-1).timestamp())+int(86400)

#cosmes資料庫位置以及金鑰
endpoint = "XXXX"
key = 'XXXXX'
client = CosmosClient(endpoint, key)
database_name_3 = 'Linebot_Cosmes'
database = client.create_database_if_not_exists(id=database_name_3)
container_name_3 = 'Save_follow_user_data'
# container_3 = 紀錄客戶 follow 時的資料庫容器
container_3 = database.create_container_if_not_exists(
    id=container_name_3,
    partition_key=PartitionKey(path="/user_id"),
    offer_throughput=400)

# 本日及昨日時間截點
# print(today_timestamp)
# print(yesterday_timestamp)

query1 = "SELECT * FROM c where c._ts>(%d) AND c._ts<(%d)"%(yesterday_start_timestamp,yesterday_end_timestamp)
Count_newFriends = list(container_3.query_items(query=query1, enable_cross_partition_query=True))
client = CosmosClient(endpoint, key)
database_name_2 = 'Linebot_Cosmes'
database = client.create_database_if_not_exists(id=database_name_2)
container_name_2 = 'Messagedata'
container_2 = database.create_container_if_not_exists(
    id=container_name_2,
    partition_key=PartitionKey(path="/user_id"),
    offer_throughput=400)

query2 = "SELECT * FROM c where c._ts>(%d) AND c._ts<(%d)"%(yesterday_start_timestamp,yesterday_end_timestamp)
Count_yesterday_message = list(container_2.query_items(query=query2, enable_cross_partition_query=True))
# 昨日好友新增人數
print("昨日好友增加 : "+str(len(Count_newFriends))+" 人\n"+"昨日互動次數 : "+str(len(Count_yesterday_message ))+" 次")
token_list = cosmes_token()
params = {"message": "\n昨日好友增加 : "+str(len(Count_newFriends))+" 人\n"+"昨日互動次數 : "+str(len(Count_yesterday_message ))+" 次"}

 # 從資料庫撈取token，發送訊息，如果只要發送訊息，改params就可以
for person in token_list:
    headers = {
        "Authorization": "Bearer " + person.get("access_token"),
        "Content-Type": "application/x-www-form-urlencoded"}
    r = requests.post("https://notify-api.line.me/api/notify",headers=headers, params=params)
    print(r.status_code)  # 200

