import urllib.request


def health_check():
    Response = urllib.request.urlopen("http://localhost:80/health")
    print(Response.read())
    
    
    
    
    
health_check()    
   