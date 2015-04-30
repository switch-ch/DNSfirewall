#!/usr/bin/python
# Get Top 500 ch domains from alexa
# Change baseURL for other countries or categories.
#
# Original made by Linus Särud, source from
# https://gist.github.com/zulln/266de436c67a2cd178f9

import requests, re

baseURL = "http://www.alexa.com/topsites/countries;{id}/CH"
regex = r'<a href="/siteinfo/(.+?)">'

domains = []
for id in range(20):
    url = baseURL.format(id=id)
    text = requests.get(url).text
    domains += re.findall(regex, text)

open("top500.txt", "w").write("\n".join(domains))
