import feedparser
import PyRSS2Gen
import datetime
from datetime import datetime
pen = {}
q = []
feeds = [ 'https://status.aws.amazon.com/rss/management-console.rss', 'https://status.aws.amazon.com/rss/ec2-us-east-1.rss', 'https://status.aws.amazon.com/rss/supportcenter.rss' ]
for feed in feeds:
    raw = feedparser.parse(feed)
    for e in raw['entries']:
        #
        # So this is terrible, but datetime gives me a ibloody headache
        #
        dt = e['published'].split()
        dts = " ".join([dt[1], dt[2], dt[3], dt[4] ])
        dto = datetime.strptime(dts, "%d %b %Y %H:%M:%S")
        single = PyRSS2Gen.RSSItem(
            title = e['title'],
            link = e['link'],
            description = e['description'],
            pubDate = e['published']
        )
        q.append(single)
rss = PyRSS2Gen.RSS2(
  title = "AWS Feed",
  link = "http://www.foo.bar/test.xml",
  description = "AWS Stuff",
  lastBuildDate = datetime.now(),
  items = q
)
rss.write_xml(open("AWS.xml", "w"))
