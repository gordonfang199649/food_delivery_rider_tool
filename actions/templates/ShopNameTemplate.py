def shop_name_template(shop_names: list) -> dict:
    contents = list()
    for name in shop_names:
        contents.append({
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
                "type": "message",
                "label": name,
                "text": f"圖 {name}"
            }
        })

    return {
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": "https://content.shopback.com/tw/wp-content/uploads/2019/11/12152136/foodpanda.png",
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
            "action": {
                "type": "uri",
                "uri": "http://linecorp.com/"
            }
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "店家名稱搜尋結果",
                    "weight": "bold",
                    "size": "xl"
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": contents,
            "flex": 0
        }
    }