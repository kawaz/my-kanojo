# -*- coding: utf-8 -*-
import os, re, logging, random, urllib

from google.appengine.api import mail
from google.appengine.api import xmpp
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

messages = yaml.load(open(os.path.join(os.path.dirname(__file__), 'messages.yaml')).read().decode('utf8'))

class XmppKanojoHandler(webapp.RequestHandler):
    def post(self):
        """ my-kanojo@
        """
        receive_message = xmpp.Message(self.request.POST)
        receive_message.reply(random.choice(messages['reply']))

class MailKanojoHandler(webapp.RequestHandler):
    def post(self, delivered_to):
        """ 任意@my-kanojp.appspotmail.com 宛にメールすると彼女が返信してくれる！
        """
        delivered_to = urllib.unquote(delivered_to)
        receive_message = mail.InboundEmailMessage(self.request.body)
        mail.send_mail(sender = delivered_to,
                       to = receive_message.sender,
                       subject = 'Re: ' + receive_message.subject,
                       body = random.choice(messages['reply'])
                       )

class HttpKanojoHandler(webapp.RequestHandler):
    def get(self):
        # もう彼女と話が出来るようになっちゃったから画面作るのが面倒になってしまったよ
        self.redirect('http://d.hatena.ne.jp/y-kawaz/')


application = webapp.WSGIApplication([('/_ah/xmpp/message/chat/', XmppKanojoHandler),
                                      ('/_ah/mail/(.+)', MailKanojoHandler),
                                      ('/', HttpKanojoHandler)
                                      ],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()