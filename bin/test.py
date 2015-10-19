import urllib.request

proxy_support = urllib.request.ProxyHandler({"http":"http://proxy.univ-lille1.fr:3128"})
opener = urllib.request.build_opener(proxy_support)
urllib.request.install_opener(opener)

html = urllib.request.urlopen("http://vps205524.ovh.net/").read()
print(html)
