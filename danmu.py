from bilibili_api import Credential, Danmaku, sync
from bilibili_api.live import LiveDanmaku, LiveRoom

# 自己直播间号
ROOMID = 5440
# 凭证 根据回复弹幕的账号填写
credential = Credential(
    sessdata="e28a1a81%2C1753610339%2Cfcd2f%2A11CjA4XBD-DHQenD4vae1XPmg5dPb0x0vmonldyOxaSAt8Hi7AvuxSGeUL6ajDz_x3y5USVnloTVB3VlpHaEJYeEM2UEQweWdfbkVhMkVHa1ZXWnVlRUxJS1lsLUE4RnNhazE5TWYyOEkyMWw3ajV1RmZDVWNsWXl3dEZBLUhYVnJfUm9oajg2cEhRIIEC",
    bili_jct="0b74cf5c4460a6edef0add7864ea23ba"
)
# 监听直播间弹幕
monitor = LiveDanmaku(ROOMID, credential=credential)
# 用来发送弹幕
sender = LiveRoom(ROOMID, credential=credential)
# 自己的UID 可以手动填写也可以根据直播间号获取
UID = sync(sender.get_room_info())["room_info"]["uid"]


@monitor.on("DANMU_MSG")
async def recv(event):
    # print(event.data)
    # 发送者UID
    uid = event["data"]["info"][2][0]
    # 排除自己发送的弹幕
    if uid == UID:
        return
    # 弹幕文本
    content = event["data"]["info"][1]
    name = event["data"]["info"][0][15]['user']['base']['name']
    print(f'{name}: {content}')
    sender = LiveRoom(ROOMID, credential=credential)
    await sender.send_danmaku(Danmaku("哈哈哈"))
    import time
    time.sleep(5)

# 启动监听
sync(monitor.connect())
