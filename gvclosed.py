from flask import Flask, render_template
from bs4 import BeautifulSoup
from urllib2 import urlopen, Request
from oauth2client.client import SignedJwtAssertionCredentials
from httplib2 import Http
from apiclient.discovery import build
from config import client, key, views, metrics

with open(key) as f:
  private_key = f.read()

credentials = SignedJwtAssertionCredentials(client, private_key,
    ['https://www.googleapis.com/auth/analytics','https://www.googleapis.com/auth/analytics.readonly'], private_key_password='notasecret')
http_auth = credentials.authorize(Http())

service = build('analytics', 'v3', http=http_auth)


app = Flask(__name__)

@app.route("/")
def index():
        url = 'http://www.gvsu.edu/'
        req = Request(url)
        req = urlopen(req)
        soup = BeautifulSoup(req.read())
        closed_div = soup.find("div", {"id": "gvsu-crisis_alert"})
        is_closed = False
        if closed_div:
            closed_div.h2.extract()
            details = closed_div.text
            closed = "Yes."
            is_closed = True
        else:
            closed = "No."
            details = ""
        return render_template('closed.html',closed=closed,details=details,is_closed=is_closed, users=get_actice_users())


def get_actice_users():
    return int(service.data().realtime().get(
      ids=views,
      metrics=metrics).execute()['totalsForAllResults'][metrics])+1

if __name__ == "__main__":
    app.run()
