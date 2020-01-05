from io import BytesIO
import base64
import numpy as np
from flask import Flask, Response, render_template, request
import requests
from astropy.coordinates import SkyCoord
from astropy import units as u
import makePic


app = Flask(__name__)

    
@app.route('/', methods=['POST', 'GET'])
def postreq():
    error = None
    if request.method == 'POST':
        if "ZoomOut" in request.form:
            scale=2
        else:
            scale=1
        if "Threshold" in request.form:
            thres=5
        else:
            thres=10
        if validate_request():
            if request.form["Name"]!='':
                try:
                    resp=requests.get('http://simbad.u-strasbg.fr/simbad/sim-nameresolver?Ident='+request.form['Name']+'&data=M(V),J&output=json').json()
                    min_mag=resp[0]
                    for i in resp:
                        if ('dec' in i) and ('ra' in i) and ('M.V' in i):
                            if (not 'M.V' in min_mag):
                                min_mag=i
                            if i["M.V"]<min_mag["M.V"]:
                                min_mag=i
                    
                    if scale==1:
                        if thres==10:
                            return render_template('hello.html',Name=request.form['Name'],image="data:image/png;base64,"+ base64.b64encode(create_figure(min_mag['ra'],min_mag['dec'],scale,thres)).decode("UTF-8"),RA=min_mag['ra'],DEC=min_mag['dec'],Error="Magnitude: "+min_mag['M.V'])
                        else:
                            return render_template('hello.html',Name=request.form['Name'],image="data:image/png;base64,"+ base64.b64encode(create_figure(min_mag['ra'],min_mag['dec'],scale,thres)).decode("UTF-8"),RA=min_mag['ra'],DEC=min_mag['dec'],THRES=thres,Error="Magnitude: "+min_mag['M.V'])
                    else:
                        if thres==10:
                            return render_template('hello.html',Name=request.form['Name'],image="data:image/png;base64,"+ base64.b64encode(create_figure(min_mag['ra'],min_mag['dec'],scale,thres)).decode("UTF-8"),RA=min_mag['ra'],DEC=min_mag['dec'],ZOOM=scale,Error="Magnitude: "+min_mag['M.V'])
                        else:
                            return render_template('hello.html',Name=request.form['Name'],image="data:image/png;base64,"+ base64.b64encode(create_figure(min_mag['ra'],min_mag['dec'],scale,thres)).decode("UTF-8"),RA=min_mag['ra'],DEC=min_mag['dec'],ZOOM=scale,THRES=thres,Error="Magnitude: "+min_mag['M.V'])
                except:
                    if request.form["RA"]!='' and request.form["DEC"]!='':
                        try:           
                            resp=requests.get('http://simbad.u-strasbg.fr/simbad/sim-nameresolver?coord='+request.form['RA']+'+'+request.form['DEC']+'&data=I.0,J,M(V)&output=json').json()
                            for i in resp:
                                if ('dec' in i) and ('ra' in i):
                                    if scale==1:
                                        if thres==10:
                                            return render_template('hello.html',Name=i["mainId"],image="data:image/png;base64,"+ base64.b64encode(create_figure(i['ra'],i['dec'],scale,thres)).decode("UTF-8"),RA=i['ra'],DEC=i['dec'],Error="Star with name: "+request.form["Name"]+" not found. Execution of coordinates search.\n"+"Closest star (distance={:.2f} asec): Magnitude: {:.1f}".format(float(i["distance"])*60.0,float(i["M.V"])))
                                        else:
                                            return render_template('hello.html',Name=i["mainId"],image="data:image/png;base64,"+ base64.b64encode(create_figure(i['ra'],i['dec'],scale,thres)).decode("UTF-8"),RA=i['ra'],DEC=i['dec'],Error="Star with name: "+request.form["Name"]+" not found. Execution of coordinates search.\n"+"Closest star (distance={:.2f} asec): Magnitude: {:.1f}".format(float(i["distance"])*60.0,float(i["M.V"])),THRES=thres)
                                    else:
                                        if thres==10:
                                            return render_template('hello.html',Name=i["mainId"],image="data:image/png;base64,"+ base64.b64encode(create_figure(i['ra'],i['dec'],scale,thres)).decode("UTF-8"),RA=i['ra'],DEC=i['dec'],Error="Star with name: "+request.form["Name"]+" not found. Execution of coordinates search.\n"+"Closest star (distance={:.2f} asec): Magnitude: {:.1f}".format(float(i["distance"])*60.0,float(i["M.V"])),ZOOM=scale)
                                        else:
                                            return render_template('hello.html',Name=i["mainId"],image="data:image/png;base64,"+ base64.b64encode(create_figure(i['ra'],i['dec'],scale,thres)).decode("UTF-8"),RA=i['ra'],DEC=i['dec'],Error="Star with name: "+request.form["Name"]+" not found. Execution of coordinates search.\n"+"Closest star (distance={:.2f} asec): Magnitude: {:.1f}".format(float(i["distance"])*60.0,float(i["M.V"])),ZOOM=scale,THRES=thres)
                            
                        except:
                            if scale==1:
                                if thres==10:
                                    return render_template('hello.html',Error="No data obtained for star with coordinates: "+request.form['RA']+" "+request.form['DEC'])
                                else:
                                    return render_template('hello.html',Error="No data obtained for star with coordinates: "+request.form['RA']+" "+request.form['DEC'],THRES=thres)
                            else:
                                if thres==10:
                                    return render_template('hello.html',Error="No data obtained for star with coordinates: "+request.form['RA']+" "+request.form['DEC'],ZOOM=scale)
                                else:
                                    return render_template('hello.html',Error="No data obtained for star with coordinates: "+request.form['RA']+" "+request.form['DEC'],ZOOM=scale,THRES=thres)
                    if scale==1:
                        if thres==10:
                            return render_template('hello.html',Error="No data obtained about '"+request.form['Name']+"' star")
                        else:
                            return render_template('hello.html',Error="No data obtained about '"+request.form['Name']+"' star",THRES=thres)
                    else:
                        if thres==10:
                            return render_template('hello.html',Error="No data obtained about '"+request.form['Name']+"' star",ZOOM=scale)
                        else:
                            return render_template('hello.html',Error="No data obtained about '"+request.form['Name']+"' star",ZOOM=scale,THRES=thres)

            else:
                try:
                                       
                    resp=requests.get('http://simbad.u-strasbg.fr/simbad/sim-nameresolver?coord='+request.form['RA']+'+'+request.form['DEC']+'&data=I.0,J,M(V)&output=json').json()
                    
                    for i in resp:
                        if ('dec' in i) and ('ra' in i):
                            if scale==1:
                                if thres==10:
                                    return render_template('hello.html',Name=i['mainId'],image="data:image/png;base64,"+ base64.b64encode(create_figure(i['ra'],i['dec'],scale,thres)).decode("UTF-8"),RA=i['ra'],DEC=i['dec'],Error="Closest star (distance={:.2f} asec): Magnitude: {:.1f}".format(float(i["distance"])*60.0,float(i["M.V"])))
                                else:
                                    return render_template('hello.html',Name=i['mainId'],image="data:image/png;base64,"+ base64.b64encode(create_figure(i['ra'],i['dec'],scale,thres)).decode("UTF-8"),RA=i['ra'],DEC=i['dec'],Error="Closest star (distance={:.2f} asec): Magnitude: {:.1f}".format(float(i["distance"])*60.0,float(i["M.V"])),THRES=thres)
                            else:
                                if thres==10:
                                    return render_template('hello.html',Name=i['mainId'],image="data:image/png;base64,"+ base64.b64encode(create_figure(i['ra'],i['dec'],scale,thres)).decode("UTF-8"),RA=i['ra'],DEC=i['dec'],Error="Closest star (distance={:.2f} asec): Magnitude: {:.1f}".format(float(i["distance"])*60.0,float(i["M.V"])),ZOOM=scale)
                                else:
                                    return render_template('hello.html',Name=i['mainId'],image="data:image/png;base64,"+ base64.b64encode(create_figure(i['ra'],i['dec'],scale,thres)).decode("UTF-8"),RA=i['ra'],DEC=i['dec'],Error="Closest star (distance={:.2f} asec): Magnitude: {:.1f}".format(float(i["distance"])*60.0,float(i["M.V"])),ZOOM=scale,THRES=thres)
                    
                except:
                    ra,dec=get_ra_dec_fromString(request.form['RA'],request.form['DEC'])
                    if ra!=None:
                        if scale==1:
                            if thres==10:
                                return render_template('hello.html',image="data:image/png;base64,"+ base64.b64encode(create_figure(ra,dec,scale,thres)).decode("UTF-8"),RA=request.form['RA'],DEC=request.form['DEC'],Error="No data obtained for star with coordinates: "+request.form['RA']+" "+request.form['DEC'])
                            else:
                                return render_template('hello.html',image="data:image/png;base64,"+ base64.b64encode(create_figure(ra,dec,scale,thres)).decode("UTF-8"),RA=request.form['RA'],DEC=request.form['DEC'],Error="No data obtained for star with coordinates: "+request.form['RA']+" "+request.form['DEC'],THRES=thres)
                        else:
                            if thres==10:
                                return render_template('hello.html',image="data:image/png;base64,"+ base64.b64encode(create_figure(ra,dec,scale,thres)).decode("UTF-8"),RA=request.form['RA'],DEC=request.form['DEC'],Error="No data obtained for star with coordinates: "+request.form['RA']+" "+request.form['DEC'],ZOOM=scale)
                            else:
                                return render_template('hello.html',image="data:image/png;base64,"+ base64.b64encode(create_figure(ra,dec,scale,thres)).decode("UTF-8"),RA=request.form['RA'],DEC=request.form['DEC'],Error="No data obtained for star with coordinates: "+request.form['RA']+" "+request.form['DEC'],ZOOM=scale,THRES=thres)
                    else:
                        if scale==1:
                            if thres==10:
                                return render_template('hello.html',RA=request.form['RA'],DEC=request.form['DEC'],Error="No data obtained for star with coordinates: "+request.form['RA']+" "+request.form['DEC']+". Unknown coordinates style!")
                            else:
                                return render_template('hello.html',RA=request.form['RA'],DEC=request.form['DEC'],Error="No data obtained for star with coordinates: "+request.form['RA']+" "+request.form['DEC']+". Unknown coordinates style!",THRES=thres)
                        else:
                            if thres==10:
                                return render_template('hello.html',RA=request.form['RA'],DEC=request.form['DEC'],Error="No data obtained for star with coordinates: "+request.form['RA']+" "+request.form['DEC']+". Unknown coordinates style!",ZOOM=scale)
                            else:
                                return render_template('hello.html',RA=request.form['RA'],DEC=request.form['DEC'],Error="No data obtained for star with coordinates: "+request.form['RA']+" "+request.form['DEC']+". Unknown coordinates style!",ZOOM=scale,THRES=thres)
        else:
            if scale==1:
                if thres==10:
                    return render_template('hello.html',Error="Not enough info")
                else:
                    return render_template('hello.html',Error="Not enough info",THRES=thres)
            else:
                if thres==10:
                    return render_template('hello.html',Error="Not enough info",ZOOM=scale)
                else:
                    return render_template('hello.html',Error="Not enough info",ZOOM=scale,THRES=thres)

    
    return render_template('hello.html')
    

def get_ra_dec_fromString(ra_string,dec_string):
    try:
        ra=float(ra_string)
        dec=float(dec_string)
        return ra,dec
    except:
        coords=ra_string + " " + dec_string
        coords=coords.split(":")
        if len(coords)==1:
            coords=coords[0]
            coords=coords.split("h")
            if len(coords)==1:
                coords=coords[0]
                coords=coords.split("d")
                if len(coords)==1:
                    coords=coords[0]
                    coords=coords.split()
                    if len(coords)==6:
                        coords=SkyCoord(coords[0]+"h"+coords[1]+"m"+coords[2]+" "+coords[3]+"d"+coords[4]+"m"+coords[5])
                        return coords.ra.deg,coords.dec.deg
                    return None,None
                return None,None
            try:
                coords=SkyCoord(ra_string+" "+dec_string)
                return coords.ra.deg,coords.dec.deg
            except:
                return None,None
            return None,None

        #for ::: ::: style
        if len(coords)==5:
            coords[2]=coords[2].split("+")
            if len(coords[2])==1:
                coords[2]=coords[2][0]
                coords[2]=coords[2].split("-")
                coords=SkyCoord(coords[0]+"h"+coords[1]+"m"+coords[2][0]+" -"+coords[2][1]+"d"+coords[3]+"m"+coords[4])
            else:
                print(coords)
                coords=SkyCoord(coords[0]+"h"+coords[1]+"m"+coords[2][0]+" +"+coords[2][1]+"d"+coords[3]+"m"+coords[4])
            return coords.ra.deg,coords.dec.deg
        return None,None
                


def validate_request():
    if (request.form["Name"]=='' and (request.form["RA"]=='' or request.form["DEC"]=='')):
        return False
    return True
        


def create_figure(ra,dec,scale,thres):

    data = BytesIO()
    fig=makePic.makePic(ra,dec,scale,thres)
    fig.savefig(data, format='png',dpi=160)
    makePic.plt.close()
    return data.getvalue()
    
app.run('0.0.0.0', 8888)
