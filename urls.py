import os
import re 
import requests
import json 
import socket 


startpos = 0
urlsTotal = []
ports = []
urlsmax = 0
proxiestotal = []

def main():
    global urlsTotal
    global startpos 
    global proxiestotal 
    global ports 
    global urlsmax 
    help = '1. start\n'
    help += '2. show list\n'
    help += "3. save list\n"
    help += "4. quit\n"
    print(help)

    a = input('.:').rstrip()
    if a == '1':

        proxcheck = input('Check proxies on what ports? (frmt: 80,8080\n').rstrip()
        if proxcheck.find(',') == -1:
            ports = [int(proxcheck)]
        else:
            ports = proxcheck.split(',')

        urlsmacks = input('Enter max URLs to gather before starting:\n').rstrip()
        try:
            urlsmax = int(urlsmacks)
        except Exception:
            print(Exception)


        term = input('Search term: \n').rstrip()
        startpos = 0
        urls = grablinks(term, startpos)

        while len(urls) > 0:
            if startpos >= urlsmax:
                break 

            for x in urls:
                if x not in urlsTotal:
                    urlsTotal.append(x)
                    print(x)
            startpos += 10
            urls = grablinks(term, startpos)
            if len(urls) > 0:
                for x in urls:
                    if x not in urlsTotal:
                        urlsTotal.append(x)
                        print(x)
        print('Full list of urls gotten, now executing grep for proxies..\n')
        for x in urlsTotal:
            rge = '\b(?:(?:2(?:[0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9])\.){3}(?:(?:2([0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9]))\b'
            
            proxylist = grabproxies(x)
            if proxylist is list: 
                for y in proxylist:
                    reg = re.compile(rge)
                    if reg.match(rge):
                        print('Testing Proxy: ' + y)
                        test = checkproxy(y)
                        if test == 'Not Ok':
                            print('Bad proxy: ' + y)
                        elif test == 'Ok':
                            proxiestotal.append(y)
                            print('Good proxy found: ' + y)

                    else:
                        print('Not matched as an IP: ' + x)
            else:
                print(proxylist) #this will be an error.
        
        print('Checking proxies\n')
        


    if a == '2':
        for x in proxiestotal:
            print(x)

    if a == '3':
        filepath = input('Save To(' + os.getcwd() + '\)').rstrip()
        thisdir = os.getcwd() + '/' 
        savefile = thisdir + filepath 
        bigstring = ''
        for y in proxiestotal:
            bigstring += y + '\n'
        b = open(savefile, 'w')
        b.write(bigstring)
        b.close()
        print('Saved To: ' + os.getcwd + '/' + filepath)

    if a == '4' or a == 'quit':
        quit()
    
    main()

def grabproxies(page):
    #write the regex and search for it
    rge = '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    #get the page:
    print('Grabbing google page: ' + page + ' \n')

    pages = requests.get(page, timeout=4)
    txtpage = ''
    if pages.ok:
        txtpage = pages.text
    else:
        print("Error grabbing page.")

    if len(txtpage) == 0:
        print('Page could not be gathered')

    proxylist = re.findall(rge, txtpage)

    if len(proxylist) > 0:
        print('Proxies found on/at: ' + page)
        return(proxylist)
    else:
        print('No proxies on page: ' + page)

def checkproxy(proxy):
    global ports
    print('Testing proxy (' + str(proxy) + ')...\n')

    grabpageURL = "https://google.com/search?q=proxy+servers"
    for x in ports:
        proxydict = {'host': proxy, "port": int(ports[x])}
    try:
        thisr = requests.get(grabpageURL, timeout=5, proxies=proxydict)
    except Exception:
        print(Exception)
        return('Error')

    if thisr.status_code == 200:
        return('Ok')
    elif thisr.status_code != 200:
        return('Not Ok')

def grablinks(term, startpos):
    ##returns a list of links on the page
    urlsTotal2 = []
    url = "https://google.com/search?q=" + term + '&start=' + str(startpos)
    resp = requests.get(url, timeout=4)
    txt = ''
    if resp.ok:
        txt = resp.text
    else:
        print('Error gathering')
        quit()

    if len(txt) > 0:
        if txt.find('url?q=') == -1: ##return blank if no links are found
            return urlsTotal2

        urls = txt.split('url?q=')
        for x in urls:
            url2 = x.split('&amp')[0]
            if url2.startswith('https') and url2.find('google.') == -1:
                if url2 not in urlsTotal:
                    print(url2)
                    urlsTotal.append(url2)

                urlsTotal2.append(url2)
        return(urlsTotal2)


if __name__ == '__main__':
    main()