from io import BytesIO
import base64
import numpy as np
from flask import Flask, Response, render_template, request
import requests
from astropy.coordinates import SkyCoord
from astropy import units as u
import makePic
from astroquery.simbad import Simbad

app = Flask(__name__)

@app.route('/', methods=['GET'])
def getreq():
    return render_template('hello.html',Error=None)
    
@app.route('/', methods=['POST'])
def postreq():

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
                
                result_table = simbad_object()
                
                if not result_table is None:
                    return render_page(str_html='hello.html',Name=request.form['Name'],image="data:image/png;base64,"+ base64.b64encode(create_figure(result_table["RA_d"][0],result_table["DEC_d"][0],scale,thres)).decode("UTF-8"),RA=result_table["RA_d"][0],DEC=result_table["DEC_d"][0],ZOOM=scale,THRES=thres,Error="Magnitude: {:.1f}".format(result_table["FLUX_V"][0]))
                else:
                    raise ValueError
                
            except ValueError:
                if request.form["RA"]!='' and request.form["DEC"]!='':
                    try:           
                        
                        ra_unit,dec_unit=get_ra_dec_units_fromString(request.form["RA"],request.form["DEC"])
                        
                        result_table=simbad_region(ra_unit,dec_unit)
                        
                        c1=SkyCoord(request.form["RA"],request.form["DEC"],unit=(ra_unit,dec_unit),frame='icrs')
                        
                        if not result_table is None:
                            
                            c2=SkyCoord(result_table["RA_d"][0],result_table["DEC_d"][0],unit=(u.deg,u.deg),frame='icrs')
                            dist=c1.separation(c2).arcsecond
                            return render_page(str_html='hello.html',Name=str(result_table["MAIN_ID"][0]),image="data:image/png;base64,"+ base64.b64encode(create_figure(result_table["RA_d"][0],result_table["DEC_d"][0],scale,thres)).decode("UTF-8"),RA=result_table["RA_d"][0],DEC=result_table["DEC_d"][0],Error="Star with name: "+request.form["Name"]+" not found. Execution of coordinates search.\n"+"Closest star (distance={:.2f} asec): Magnitude: {:.1f}".format(dist,result_table["FLUX_V"][0]),ZOOM=scale,THRES=thres)
                        else:
                            return render_page(str_html='hello.html',image="data:image/png;base64,"+ base64.b64encode(create_figure(c1.ra.deg,c1.dec.deg,scale,thres)).decode("UTF-8"),RA=request.form['RA'],DEC=request.form['DEC'],Error="No data obtained for star with coordinates: "+request.form['RA']+" "+request.form['DEC'],ZOOM=scale,THRES=thres)
                                
                        
                    except ValueError:
                        return render_page(str_html='hello.html',RA=request.form['RA'],DEC=request.form['DEC'],Error="No data obtained for star with coordinates: "+request.form['RA']+" "+request.form['DEC']+". Unknown coordinates style!",ZOOM=scale,THRES=thres)
                        
                                
                return render_page(str_html='hello.html',Error="No data obtained about '"+request.form['Name']+"' star",ZOOM=scale,THRES=thres)
                        

        else:
            try:
                ra_unit,dec_unit=get_ra_dec_units_fromString(request.form["RA"],request.form["DEC"])
                result_table=simbad_region(ra_unit,dec_unit)
                c1=SkyCoord(request.form["RA"],request.form["DEC"],unit=(ra_unit,dec_unit),frame='icrs')
                
                if not result_table is None:
                    c2=SkyCoord(result_table["RA_d"][0],result_table["DEC_d"][0],unit=(u.deg,u.deg),frame='icrs')
                    dist=c1.separation(c2).arcsecond
                    return render_page(str_html='hello.html',Name=result_table["MAIN_ID"][0].decode("UTF-8"),image="data:image/png;base64,"+ base64.b64encode(create_figure(result_table["RA_d"][0],result_table["DEC_d"][0],scale,thres)).decode("UTF-8"),RA=result_table["RA_d"][0],DEC=result_table["DEC_d"][0],Error="Closest star (distance={:.2f} asec): Magnitude: {:.1f}".format(dist,result_table["FLUX_V"][0]),ZOOM=scale,THRES=thres)
                else:
                    return render_page(str_html='hello.html',image="data:image/png;base64,"+ base64.b64encode(create_figure(c1.ra.deg,c1.dec.deg,scale,thres)).decode("UTF-8"),RA=request.form['RA'],DEC=request.form['DEC'],Error="No data obtained for star with coordinates: "+request.form['RA']+" "+request.form['DEC'],ZOOM=scale,THRES=thres)
                    
                
            except ValueError:
                    return render_page(str_html='hello.html',RA=request.form['RA'],DEC=request.form['DEC'],Error="No data obtained for star with coordinates: "+request.form['RA']+" "+request.form['DEC']+". Unknown coordinates style!",ZOOM=scale,THRES=thres)
                    
    else:
        return render_page(str_html='hello.html',Error="Not enough info",THRES=thres, ZOOM=scale)        
        

    
def simbad_region(ra_unit,dec_unit):
    customSimbad=Simbad()
    customSimbad.TIMEOUT=5
    customSimbad.add_votable_fields('ra(d)','dec(d)','flux(V)')
    customSimbad.remove_votable_fields('coordinates')
    
    if ra_unit is None:
        raise ValueError
    else:
        result_table = customSimbad.query_region(SkyCoord(request.form["RA"],request.form["DEC"],unit=(ra_unit,dec_unit),frame='icrs'), radius='0d2m0s')
        return result_table
                
def simbad_object():
    customSimbad=Simbad()
    customSimbad.TIMEOUT=5
    customSimbad.add_votable_fields('ra(d)','dec(d)','flux(V)')
    customSimbad.remove_votable_fields('coordinates')
    result_table=customSimbad.query_object(request.form["Name"])
    return result_table
    
    
def render_page(str_html,RA=None,DEC=None,Error=None,image=None,ZOOM=None,THRES=None,Name=None):
    if ZOOM==1:
        if THRES==10:
            return render_template(str_html,RA=RA,DEC=DEC,Error=Error,Name=Name,image=image)
        else:
            return render_template(str_html,RA=RA,DEC=DEC,Error=Error,Name=Name,image=image,THRES=THRES)
    else:
        if THRES==10:
            return render_template(str_html,RA=RA,DEC=DEC,Error=Error,Name=Name,image=image,ZOOM=ZOOM)
        else:
            return render_template(str_html,RA=RA,DEC=DEC,Error=Error,Name=Name,image=image,ZOOM=ZOOM,THRES=THRES)

def get_ra_dec_units_fromString(ra_string,dec_string):
    try:
        float(ra_string)
        ra_unit=u.deg
    except:
        if len(ra_string.split())==3:
            ra_unit=u.hour
        elif len(ra_string.split(":"))==3:
            ra_unit=u.hour
        elif len(ra_string.split("h"))==2:
            ra_unit=u.hour
        elif len(ra_string.split("d"))==2:            
            ra_unit=u.deg
        else:
            return None,None
    try:
        float(dec_string)
        dec_unit=u.deg
    except:
        if len(dec_string.split())==3:
            dec_unit=u.deg
        elif len(dec_string.split(":"))==3:
            dec_unit=u.deg
        elif len(dec_string.split("h"))==2:
            dec_unit=u.hour
        elif len(dec_string.split("d"))==2:            
            dec_unit=u.deg
        else:
            return None,None
    
    return ra_unit,dec_unit
                


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


if __name__ == '__main__':
    app.run('0.0.0.0', 8888)
