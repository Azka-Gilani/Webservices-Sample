#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "yahooWeatherForecast":
        return {}
    baseurl = "https://fazendanatureza.com/bot/botarz.php"
    result = urllib.urlopen(baseurl).read()
    data = json.loads(result)
    res = makeWebhookResult(data)
    return res


def makeWebhookResult(data):
    query = data.get('title')
    if query is None:
        return {}

    # print(json.dumps(item, indent=4))

    speech = "This is the response from server... " + query
    print("Response:")
    print(speech)
    message= {
      "attachment": {
         "type": "template",
          "payload": {
               "template_type": "generic",
               "elements": [{
               "title": "rift",
               "subtitle": "Next-generation virtual reality",
               "item_url": "https://www.oculus.com/en-us/rift/",               
               "image_url": "http://messengerdemo.parseapp.com/img/rift.png",
                "buttons": [{
                "type": "web_url",
                "url": "https://www.oculus.com/en-us/rift/",
                "title": "Open Web URL"
            }, 
                    {
                "type": "postback",
                "title": "Call Postback",
                "payload": "Payload for first bubble",
            }],
          }, 
                   {
                "title": "touch",
                "subtitle": "Your Hands, Now in VR",
                "item_url": "https://www.oculus.com/en-us/touch/",               
                "image_url": "http://messengerdemo.parseapp.com/img/touch.png",
                "buttons": [{
                "type": "web_url",
                "url": "https://www.oculus.com/en-us/touch/",
                "title": "Open Web URL"
            },
                    {
                "type": "postback",
                "title": "Call Postback",
                "payload": "Payload for second bubble",
            }]
          }]
        }
      }
    }
    return {
        "speech": speech,
        "displayText": speech,
        "data": {"facebook": message},
        # "contextOut": [],
        #"source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=False, port=port, host='0.0.0.0')
