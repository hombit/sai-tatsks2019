import sys
import requests as req
from bs4 import BeautifulSoup

import time

def is_downloadable(url):
    """
    Does the url contain a downloadable resource
    """
    h = req.head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True

def main():

    nam = sys.argv[1]

    diction={
    "coords":"",
    "obname":nam,
    "outdir":"",
    "targ":"",
    "Tstart":"",
    "poserr":""
    }
    
    print(nam)
    print(diction["obname"])
    resp=req.get("https://www.swift.ac.uk/user_objects/details.php?oname="+diction["obname"])
    fields = {"coords", "targ", "Tstart", "poserr"}
    parameters =resp.text.split(';')
    print(resp.text)
    for part in parameters:
        if "=" not in part:
            continue
        field, value = part.split("=")
        if field not in fields:
            continue
        value=value[1:-1]
        diction[field] = value
            
       
    if diction["targ"]=='No observations found':
        print("no obserbation")
        exit(1)


    resp=req.get("https://www.swift.ac.uk/user_objects/")

    soup = BeautifulSoup(resp.text,'html.parser')
    diction["outdir"]=soup.find(id='outdir').get('value')


    #print(string)
    #coords=string[string.find("document.getElementById('coords').value='"):]
    #coords=coords[:coords.find("';")]
    #print(coords)
    if diction["poserr"]=='':
        diction["poserr"]='1'

    data = {
    'lc':'on',
    'obname':diction["obname"],
    'outdir':diction["outdir"],
    'name':diction["obname"],
    'whatSXPS':'2SXPS',
    'targ':diction["targ"],
    'Tstart':diction["Tstart"],
    'coords':diction["coords"],
    'cent':'yes',
    'centMeth':'2',
    'maxCentTries':'10',
    'poserr':diction["poserr"],
    'wtpuprate':'150',
    'pcpuprate':'0.6',
    'useSXPS':'2SXPS',
    'email':'',
    'too':'1',
    'wtbin':'10',
    'pcbin':'100',
    'wthrbin':'20',
    'pchrbin':'200',
    'femin':'0',
    'sigmin':'3',
    'allowUL':'3',
    'allowB':'3',
    'bayesCounts':'15',
    'bayesSNR':'2.4',
    'lctimetype':'0',
    'adv':'0',
    'soft1':'0.3',
    'soft2':'1.5',
    'hard1':'1.5',
    'hard2':'10',
    'minen':'0.3',
    'maxen':'10',
    'grades':'all',
    'specz':'no',
    'specobs':'3',
    'specobstime':'12',
    'specgrades':'all',
    'timeslice':'1',
    'rname1':'',
    'gti1':'',
    'rname2':'',
    'gti2':'',
    'rname3':'',
    'gti3':'',
    'rname4':'',
    'gti4':'',
    'enherr':'20',
    'enhobs':'3',
    'enhobstime':'12',
    'detornot':'1',
    'detMeth':'0',
    'imen':'0.3-10%2C0.3-1.5%2C1.51-10',
    'imobs':'1'
    }
    resp = req.post("https://www.swift.ac.uk/user_objects/run_userobject.php", data)
    print("https://www.swift.ac.uk/user_objects/tprods/"+diction["outdir"]+"/index.php")
    #print(BeautifulSoup(resp.text, 'lxml').find("title").text.strip().split())

    while(True):
        time.sleep(10.0)
        resp = req.get("https://www.swift.ac.uk/user_objects/tprods/"+diction["outdir"]+"/index.php")
        qeqr = BeautifulSoup(resp.text, 'lxml').find("title").text.strip()
        print(qeqr)
        if 'COMPLETE' in qeqr:
            break
            
    print("to see results please visit: "+"https://www.swift.ac.uk/user_objects/tprods/"+diction["outdir"]+"/lc/index.php")
    resp = req.get("https://www.swift.ac.uk/user_objects/tprods/"+diction["outdir"]+"/lc/index.php")
    soup=BeautifulSoup(resp.text, 'lxml')

    for a in soup.find_all('a',href=True):
        #print("Download file url:", a['href'])
        if ".tar" in a['href']:
            print("Download file url:", a['href'])
            downl=a['href']
            try:
                filename=downl.rsplit('/', 1)[1]
                link=downl
            except:
                filename=downl
                link="https://www.swift.ac.uk/user_objects/tprods/"+diction["outdir"]+"/lc/"+filename

            if is_downloadable(link):
                print("downloading")
                if downl.find('/'):
     
                    print("downloading "+filename)
                    r = req.get(link, allow_redirects=True)
                    with open(filename, 'wb') as file_result:
                        file_result.write(r.content)
                    

if __name__ == '__main__':
    main()
