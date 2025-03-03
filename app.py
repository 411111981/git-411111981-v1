# -*- coding: utf-8 -*-

#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re
app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('AY3MtzOw1jwTi3/F391JQKg09Oen4chaHnwV2xYYpm0NBn13bHtN/T9D3Av5KoTVP5tD7+ylwOhcnWGUnf474y2q8kYgklg0hUgaZ+uW3TaYU9KbfNdM3W6ulPzalLLgqV0ODuB9DjzRrK0TYBMs2gdB04t89/1O/w1cDnyilFU=')

# 必須放上自己的Channel Secret
handler = WebhookHandler('bc9bb9ac52c29ba269dec9d2b18b1689')

line_bot_api.push_message('Uf96bcc7b32c11166a6d2469ad5ddf52b', TextSendMessage(text='你可以開始了'))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = text=event.message.text
    if re.match('告訴我秘密',message):
        carousel_template_message = TemplateSendMessage(
            alt_text='熱門旅行景點',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/kNBl363.jpg',
                        title='台灣',
                        text='taiwan',
                        actions=[
                            MessageAction(
                                label='熱門景點',
                                text='台北101、逢甲夜市、墾丁...'
                            ),
                            URIAction(
                                label='馬上查看',
                                uri='https://en.wikipedia.org/wiki/Taiwan'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/GBPcUEP.png',
                        title='日本',
                        text='Japan',
                        actions=[
                            MessageAction(
                                label='熱門景點',
                                text='金閣寺、淺草寺、北海道...'
                            ),
                            URIAction(
                                label='馬上查看',
                                uri='https://en.wikipedia.org/wiki/Japan'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/kRW5zTO.png',
                        title='韓國',
                        text='Korea',
                        actions=[
                            MessageAction(
                                label='熱門景點',
                                text='釜山、濟州島、首爾塔...'
                            ),
                            URIAction(
                                label='馬上查看',
                                uri='https://en.wikipedia.org/wiki/Korea'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, carousel_template_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
