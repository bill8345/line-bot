from linebot.models import *
import pymongo


def web_flex():
    message = FlexSendMessage(
        alt_text="選擇你想關注的網站",
        contents={
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "hero": {
        "type": "image",
        "size": "full",
        "aspectRatio": "20:12.9",
        "aspectMode": "fit",
        "url": "https://www.pts.org.tw/HomePage/_images/title_pts.jpg"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "公視新聞網",
            "weight": "bold",
            "size": "xl",
            "align": "center"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "lg",
            "spacing": "sm",
            "contents": []
          }
        ]
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
              "type": "message",
              "label": "請點這裡！",
              "text": "公視新聞網"
            }
          }
        ],
        "flex": 0
      }
    },
    {
      "type": "bubble",
      "hero": {
        "type": "image",
        "url": "https://image3.thenewslens.com/assets/web/publisher-photo-1.png",
        "size": "5xl",
        "aspectRatio": "25:21.5",
        "aspectMode": "fit"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "關鍵評論網",
            "size": "xl",
            "weight": "bold",
            "align": "center"
          }
        ]
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "請點這裡！",
              "text": "關鍵評論網"
            }
          }
        ]
      }
    },
    {
      "type": "bubble",
      "hero": {
        "type": "image",
        "url": "https://img.onesignal.com/permanent/89bb146e-1834-4fd6-aa9d-4c81f5984e4c.png",
        "size": "full",
        "aspectRatio": "20:12.5",
        "aspectMode": "fit"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "風傳媒",
            "size": "xl",
            "align": "center",
            "weight": "bold"
          }
        ]
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "請點這裡！",
              "text": "風傳媒"
            }
          }
        ]
      }
    }
  ]
})
    return message

def public_flex():
    client = pymongo.MongoClient("mongodb+srv://billsyu:freemongodb1@billsyu-database.mooky.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client['politic']
    col = db['public']
    keyword_1 = col.find()[0]['關鍵字']
    keyword_2 = col.find()[1]['關鍵字']
    keyword_3 = col.find()[2]['關鍵字']
    message = FlexSendMessage(
      alt_text="您可以選擇想看的關鍵字，或直接選擇閱讀最新的五篇文章",
      contents={
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "header": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "公視三大熱門議題",
            "size": "xl",
            "weight": "bold",
            "align": "center",
            "margin": "xxl"
          }
        ]
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": keyword_1,
              "text": '公視_關鍵字_Top1'
            },
            "margin": "sm"
          },
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": keyword_2,
              "text": '公視_關鍵字_Top2'
            },
            "margin": "sm"
          },
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": keyword_3,
              "text": '公視_關鍵字_Top3'
            },
            "margin": "sm"
          }
        ],
        "spacing": "sm",
        "paddingAll": "13px"
      }
    },
    {
      "type": "bubble",
      "hero": {
        "type": "image",
        "url": "https://media.istockphoto.com/photos/online-news-in-mobile-phone-close-up-of-smartphone-screen-man-reading-picture-id1065782416",
        "size": "full",
        "aspectMode": "cover",
        "aspectRatio": "320:213"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": []
              }
            ]
          },
          {
            "type": "text",
            "text": "公視最新文章",
            "size": "lg",
            "weight": "bold",
            "align": "center"
          },
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "我要看最新文章",
              "text": "公視_Latest"
            }
          }
        ],
        "spacing": "sm",
        "paddingAll": "13px"
      }
    }
  ]
})
    return message


def storm_flex():
    client = pymongo.MongoClient(
      "mongodb+srv://billsyu:freemongodb1@billsyu-database.mooky.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client['politic']
    col = db['storm']
    keyword_1 = col.find()[0]['關鍵字']
    keyword_2 = col.find()[1]['關鍵字']
    keyword_3 = col.find()[2]['關鍵字']
    message = FlexSendMessage(
      alt_text="您可以選擇想看的關鍵字，或直接選擇閱讀最新的五篇文章",
      contents={
        "type": "carousel",
        "contents": [
          {
            "type": "bubble",
            "header": {
              "type": "box",
              "layout": "vertical",
              "contents": [
                {
                  "type": "text",
                  "text": "風傳媒三大熱門議題",
                  "size": "xl",
                  "weight": "bold",
                  "align": "center",
                  "margin": "xxl"
                }
              ]
            },
            "body": {
              "type": "box",
              "layout": "vertical",
              "contents": [
                {
                  "type": "button",
                  "action": {
                    "type": "message",
                    "label": keyword_1,
                    "text": '風傳媒_關鍵字_Top1'
                  },
                  "margin": "sm"
                },
                {
                  "type": "button",
                  "action": {
                    "type": "message",
                    "label": keyword_2,
                    "text": '風傳媒_關鍵字_Top2'
                  },
                  "margin": "sm"
                },
                {
                  "type": "button",
                  "action": {
                    "type": "message",
                    "label": keyword_3,
                    "text": '風傳媒_關鍵字_Top3'
                  },
                  "margin": "sm"
                }
              ],
              "spacing": "sm",
              "paddingAll": "13px"
            }
          },
          {
            "type": "bubble",
            "hero": {
              "type": "image",
              "url": "https://media.istockphoto.com/photos/online-news-in-mobile-phone-close-up-of-smartphone-screen-man-reading-picture-id1065782416",
              "size": "full",
              "aspectMode": "cover",
              "aspectRatio": "320:213"
            },
            "body": {
              "type": "box",
              "layout": "vertical",
              "contents": [
                {
                  "type": "box",
                  "layout": "vertical",
                  "contents": [
                    {
                      "type": "box",
                      "layout": "baseline",
                      "spacing": "sm",
                      "contents": []
                    }
                  ]
                },
                {
                  "type": "text",
                  "text": "風傳媒最新文章",
                  "size": "lg",
                  "weight": "bold",
                  "align": "center"
                },
                {
                  "type": "button",
                  "action": {
                    "type": "message",
                    "label": "我要看最新文章",
                    "text": "風傳媒_Latest"
                  }
                }
              ],
              "spacing": "sm",
              "paddingAll": "13px"
            }
          }
        ]
      })
    return message


def lens_flex():
    client = pymongo.MongoClient(
      "mongodb+srv://billsyu:freemongodb1@billsyu-database.mooky.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client['politic']
    col = db['lens']
    keyword_1 = col.find()[0]['關鍵字']
    keyword_2 = col.find()[1]['關鍵字']
    keyword_3 = col.find()[2]['關鍵字']
    message = FlexSendMessage(
      alt_text="您可以選擇想看的關鍵字，或直接選擇閱讀最新的五篇文章",
      contents={
        "type": "carousel",
        "contents": [
          {
            "type": "bubble",
            "header": {
              "type": "box",
              "layout": "vertical",
              "contents": [
                {
                  "type": "text",
                  "text": "關鍵評論網三大熱門議題",
                  "size": "xl",
                  "weight": "bold",
                  "align": "center",
                  "margin": "xxl"
                }
              ]
            },
            "body": {
              "type": "box",
              "layout": "vertical",
              "contents": [
                {
                  "type": "button",
                  "action": {
                    "type": "message",
                    "label": keyword_1,
                    "text": '關鍵評論網_關鍵字_Top1'
                  },
                  "margin": "sm"
                },
                {
                  "type": "button",
                  "action": {
                    "type": "message",
                    "label": keyword_2,
                    "text": '關鍵評論網_關鍵字_Top2'
                  },
                  "margin": "sm"
                },
                {
                  "type": "button",
                  "action": {
                    "type": "message",
                    "label": keyword_3,
                    "text": '關鍵評論網_關鍵字_Top3'
                  },
                  "margin": "sm"
                }
              ],
              "spacing": "sm",
              "paddingAll": "13px"
            }
          },
          {
            "type": "bubble",
            "hero": {
              "type": "image",
              "url": "https://media.istockphoto.com/photos/online-news-in-mobile-phone-close-up-of-smartphone-screen-man-reading-picture-id1065782416",
              "size": "full",
              "aspectMode": "cover",
              "aspectRatio": "320:213"
            },
            "body": {
              "type": "box",
              "layout": "vertical",
              "contents": [
                {
                  "type": "box",
                  "layout": "vertical",
                  "contents": [
                    {
                      "type": "box",
                      "layout": "baseline",
                      "spacing": "sm",
                      "contents": []
                    }
                  ]
                },
                {
                  "type": "text",
                  "text": "關鍵評論網最新文章",
                  "size": "lg",
                  "weight": "bold",
                  "align": "center"
                },
                {
                  "type": "button",
                  "action": {
                    "type": "message",
                    "label": "我要看最新文章",
                    "text": "關鍵評論網_Latest"
                  }
                }
              ],
              "spacing": "sm",
              "paddingAll": "13px"
            }
          }
        ]
      })
    return message