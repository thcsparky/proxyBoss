import os 
import requests
import re 

def getlinks(query, startpos):
    #returns a list of urls for that page.
    url = "https://google.com/search?q=" + query + '&start=' + str(startpos)
    print('Grabbing google page: ' + url)

    req = requests.get(url, timeout=5)
    txtout = ''
    if req.ok:
        txtout = req.text
    else:
        print('status code: ' + str(req.status_code))
    links1 = []
    linksfound = []
    try:
        links1 = txtout.split('url?q=')
        for x in links1:
            link = x.split('&amp')[0]
            if link.startswith('https') and link.find('google.') == -1:
                linksfound.append(link)
        return(linksfound)
    except Exception as e:
        print('Error gathering page: ' + url + '\n')                                                                                                                            
        print(e)

def getIps(page):
    navpage = requests.get(page, timeout=5)
    txtpage = ''
    if navpage.ok: 
        txtpage = navpage.text
    else:
        return('Error: ' + str(navpage.status_code))
    
    regex = '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    matches = re.findall(regex, txtpage)
    return(matches)

def main():
    
    ports = []
    print("Press key at any point to stop searching and save list!\n")
    portGet = input('Enter ports, separated by "," unless you only wanna do one port..\n')
    if portGet.find(',') == -1:
        ports.append(str(portGet))
    else:
        portsSeparated = portGet.split(',')
        for portNumber in portsSeparated:
            ports.append(portNumber)
    
        
    a = input('Search Term:\n').rstrip()
    #maximum link pages that can be gathered without proxies is about 50...
    #10 per each page
    curpos = 0
    links = []
    proxies = []
    while curpos <= 20:
        listlinks = getlinks(a, curpos)
        if type(listlinks) is list:
            for x in listlinks:
                if x not in links:
                    #add to total links
                    links.append(x)
                    #grab proxies from page
                    print('grabbing proxies from page: ' + x)
                    proxiesSubList = getIps(x)
                    if type(proxiesSubList) == str:
                        print(proxiesSubList)
                    elif type(proxiesSubList) == list:
                        for proxy in proxiesSubList:
                            if proxy not in proxies:
                                #check proxy via ports::
                                for proxyport in ports:
                                    checker = checkProxy(proxy, proxyport)
                                    if checker == 'Not Ok':
                                        print('Bad proxy: ' + proxy + ':' + proxyport + ' ...Ignoring')
                                    elif checker == 'Ok':
                                        print('Good proxy found! :): ' + proxy + ':' + proxyport)
                                        proxies.append(proxy + ':' + proxyport)
        else:
            print(listlinks)
        curpos += 10
    print("All of these proxies found! : ")
    for x in proxies:
        print(x)
    
    print('\nTo save them, type "save"\n')
    inp = input('...').rstrip()
    if inp == 'save':
        filename = input(os.getcwd() + '/').rstrip()
        if len(filename <= 0):
            print('Invalid Filename, closing...')
            quit()
        else:
            proxystring = ''
            for x in proxies:
                proxystring += x + '\n'
            proxyOut = open(os.getcwd() + '/' + filename, 'w')
            proxyOut.write(proxystring)
            proxyOut.close()
            print('Saved list to!: ' + os.getcwd() + '/' + filename)
            quit()

    for x in links:
        print(x)

def checkProxy(proxy, port):
    url = "https://google.com/"
    proxydict = {proxy: port}
    getpage = requests.get(url, proxies=proxydict, timeout=5)
    if getpage.ok:
        return('Ok')
    else:
        return('Not Ok')

if __name__ == '__main__':
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
    main()