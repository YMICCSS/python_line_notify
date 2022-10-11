from flask import Flask,render_template,request
import uuid
import requests
import json
from Connect_line_notify_html import db

app = Flask(__name__)
# client_id 跟main.html一樣
# client_secret 填網頁上的那個，詳情可參考https://medium.com/@r3850355/%E7%AD%86%E8%A8%98-line-notify-c9cead119dc1
# redirect_uri 填跟 main.html一樣(就是這個服務的id+port),並將此redirect_uri寫回註冊頁面的 callback url
# 務必要將 token 存起來，才能用此token發送訊息
# redirect_uri 在有人連動時會收到一個帶有 code 的 POST 請求
@app.route('/',methods=["GET"])
def index():
    code = request.args.get('code')
    # 此處的 redirect_uri用意是要確認是要與服提供者所指定的redirect_uri來做確認是否一樣
    client = {'grant_type': 'authorization_code', 'code': code, 'redirect_uri': 'XXXXX',
              'client_id': 'XXXX', 'client_secret': 'XXXXX'}
    # 拿code換成token , 用 ClientID 跟 ClientSecret 去換 token 回來
    r = requests.post('https://notify-bot.line.me/oauth/token', data=client)
    access_token = json.loads(r.text)["access_token"]
    req = json.loads(r.text)
    if req['status'] == 200:
        data = {"id": str(uuid.uuid4()),
                "access_token": access_token,}
        # 將使用者資料存到NoSQL-DB
        db.DB.save_data(data)
        return render_template("success_page.html")
    else:
        return render_template("fail_page.html")
if __name__ == "__main__":
    app.run()


