import feedparser
import PyRSS2Gen
import datetime
import os
from datetime import datetime
import github3

owner = os.environ['GITHUB_ACTOR']

pen = {}
q = []
feeds = [ 'https://status.aws.amazon.com/rss/ecs-us-east-1.rss', 'https://status.aws.amazon.com/rss/elasticfilesystem-us-east-1.rss', 'https://status.aws.amazon.com/rss/elb-us-east-1.rss', 'https://status.aws.amazon.com/rss/rds-us-east-1.rss', 'https://status.aws.amazon.com/rss/route53.rss', 'https://status.aws.amazon.com/rss/ses-us-east-1.rss', 'https://status.aws.amazon.com/rss/sns-us-east-1.rss', 'https://status.aws.amazon.com/rss/s3-us-standard.rss', 'https://status.aws.amazon.com/rss/vpc-us-east-1.rss', 'https://status.aws.amazon.com/rss/autoscaling-us-east-1.rss', 'https://status.aws.amazon.com/rss/account.rss', 'https://status.aws.amazon.com/rss/certificatemanager-us-east-1.rss', 'https://status.aws.amazon.com/rss/cloudformation-us-east-1.rss', 'https://status.aws.amazon.com/rss/cloudtrail-us-east-1.rss', 'https://status.aws.amazon.com/rss/lambda-us-east-1.rss', 'https://status.aws.amazon.com/rss/management-console.rss', 'https://status.aws.amazon.com/rss/signin-us-east-1.rss' ]
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


# Connect to GitHub API and push the changes.
github = github3.login(token=os.environ['token'])
repository = github.repository(owner, 'aws-status-rss')

with open('AWS.xml', 'rb') as fd:
        contents = fd.read()

contents_object = repository.file_contents('AWS.xml')

push_status = contents_object.update('automatic', contents)
print(push_status)
