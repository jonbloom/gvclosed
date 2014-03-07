from flask import Flask, render_template
from bs4 import BeautifulSoup
from urllib2 import urlopen, Request

app = Flask(__name__)

@app.route("/")
def index():
        url = 'http://www.gvsu.edu/'
        req = Request(url)
        req = urlopen(req)
        soup = BeautifulSoup(req.read())
        closed_div = soup.find("div", {"id": "gvsu-crisis_alert"})
        if closed_div:
            closed_div.h2.extract()
            details = closed_div.text
            closed = "Yes."
        else:
            closed = "No."
            details = ""
        return render_template('closed.html',closed=closed,details=details)

if __name__ == "__main__":
    app.run()