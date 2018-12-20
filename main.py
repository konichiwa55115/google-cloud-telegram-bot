import json
import urllib
import urllib2
import config

# standard app engine imports
from google.appengine.api import urlfetch
import webapp2

# Set requests timeout (default is 15)
def setTimeout(numSec = 60):
    urlfetch.set_default_fetch_deadline(numSec)

# Deserialise object and serialise it to JSON formatted string
def formatResp(obj):
    return json.dumps(json.load(obj), indent=4, sort_keys=True)

# Lambda functions to parse updates from Telegram
def getText(update):            return update['message']['text']
def getChatId(update):          return update['message']['chat']['id']
def getName(update):            return update['message']['from']['first_name']
def getResult(update):          return update['result']

# --------------- Request handlers ---------------
ConfiguredRequestHandler = config.getConfiguredClass(webapp2.RequestHandler, 'config.ini')

def getForwardHandler(path):
    # Return basic information about the bot
    class ForwardHandler(ConfiguredRequestHandler):
        def get(self):
            setTimeout()
    
            respBuf = urllib2.urlopen(self.base_url + path)
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write(formatResp(respBuf))
    return ForwardHandler

# Set a webhook url for Telegram to POST to
class SetWebhookHandler(ConfiguredRequestHandler):
    def get(self):
        setTimeout()
        self.logger.info('Setting new webhook to: %s' % self.hook_url)

        respBuf = urllib2.urlopen(self.base_url + 'setWebhook', urllib.urlencode({
            'url': self.hook_url
        })) 
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(formatResp(respBuf))

# Handler for the webhook, called by Telegram
class WebhookHandler(ConfiguredRequestHandler):
    def post(self):
        setTimeout()
        self.logger.info('Received request: %s from %s' % (self.request.url, self.request.remote_addr))

        if self.hook_token not in self.request.url:
            # Not coming from Telegram
            self.logger.error('Post request without token from IP: %s' % self.request.remote_addr)
            return
 
        body = json.loads(self.request.body)
        
        chatId = getChatId(body)
        self.logger.info('Response body: ' + str(body))

        try:
            text = getText(body)
        except Exception as e:
            self.logger.info('No text field in update.')
            return
      
        if text == '/start':
            keyboard = self.buildKeyboard(['/test1', '/test2', '/test3'])
            self.sendMessage('Hello %s! Why not try the commands below:'  % getName(body), chatId, keyboard)
        # elif text == ...:

    # Send URL-encoded message to chat id
    def sendMessage(self, text, chatId, interface=None):
        params = {
            'chat_id': str(chatId),
            'text': text.encode('utf-8'),
            'parse_mode': 'Markdown',
        }
        if interface:
            params['reply_markup'] = interface
        
        resp = urllib2.urlopen(self.base_url + 'sendMessage', urllib.urlencode(params)).read()

    # Build a one-time keyboard for on-screen options
    def buildKeyboard(self, items):
        keyboard = [[{'text':item}] for item in items]
        replyKeyboard = {'keyboard':keyboard, 'one_time_keyboard': True}
        self.logger.debug(replyKeyboard)
        return json.dumps(replyKeyboard)


app = webapp2.WSGIApplication([
    ('/me', getForwardHandler('getMe')),
    ('/set_webhook', SetWebhookHandler),
    ('/get_webhook', getForwardHandler('getWebhookInfo')),
    ('/del_webhook', getForwardHandler('deleteWebhook')),
    (r'/TG.*' , WebhookHandler),
], debug=True)
