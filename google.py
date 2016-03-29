import urllib2,urllib
import simplejson

seachstr = 'car'

for x in range(5):
    print "page:%s"%(x+1)
    page = x * 4

    url =('https://ajax.googleapis.com/ajax/services/search/web'
                  '?v=1.0&q=%s&rsz=8&start=%s') %(urllib.quote(seachstr),page)
    try:
        request = urllib2.Request(
        url, None, {'Referer': 'http://www.sina.com'})
        response = urllib2.urlopen(request)

    # Process the JSON string.
        results = simplejson.load(response)
        infoaaa = results['responseData']['results']
    except Exception,e:
        print e
    else:
        for minfo in infoaaa:
	    print minfo['url']
# http://blog.sina.com.cn/s/blog_88e0154d01019fkf.html
