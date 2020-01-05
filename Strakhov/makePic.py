from numpy import loadtxt
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import astropy.coordinates as coord
import astropy.units as u
from astropy.coordinates import Angle
import numpy as np

import cartopy.crs as ccrs
import shapely.geometry as sgeom
from copy import copy

#from cartopy.mpl.gridliner import LATITUDE_FORMATTER, LONGITUDE_FORMATTER


def find_side(ls, side):
    """
    Given a shapely LineString which is assumed to be rectangular, return the
    line corresponding to a given side of the rectangle.
    
    """
    minx, miny, maxx, maxy = ls.bounds
    points = {'left': [(minx, miny), (minx, maxy)],
              'right': [(maxx, miny), (maxx, maxy)],
              'bottom': [(minx, miny), (maxx, miny)],
              'top': [(minx, maxy), (maxx, maxy)],}
    return sgeom.LineString(points[side])


def lambert_xticks(ax, ticks,lat,ext):
    """Draw ticks on the bottom x-axis of a Lambert Conformal projection."""
    te = lambda xy: xy[0]
    if lat<0:
        tickloc="top"
    else:
        tickloc="bottom"
    lc = lambda t, n, b: np.vstack((np.zeros(n) + t, np.linspace(b[2], b[3], n))).T
    xticks, xticklabels = _lambert_ticks(ax, ticks, tickloc, lc, te,ext)
    ax.xaxis.tick_bottom()
    
    ax.set_xticks(xticks)
    ax.set_xticklabels([ax.xaxis.get_major_formatter()(xtick) for xtick in xticklabels])
    

def lambert_yticks(ax, ticks,ext):
    """Draw ricks on the left y-axis of a Lamber Conformal projection."""
    te = lambda xy: xy[1]
    lc = lambda t, n, b: np.vstack((np.linspace(b[0], b[1], n), np.zeros(n) + t)).T
    yticks, yticklabels = _lambert_ticks(ax, ticks, 'left', lc, te,ext)
    ax.yaxis.tick_left()
    ax.set_yticks(yticks)
    ax.set_yticklabels([ax.yaxis.get_major_formatter()(ytick) for ytick in yticklabels])

def _lambert_ticks(ax, ticks, tick_location, line_constructor, tick_extractor,ext):
    """Get the tick locations and labels for an axis of a Lambert Conformal projection."""
    outline_patch = sgeom.LineString(ax.outline_patch.get_path().vertices.tolist())
    
    axis = find_side(outline_patch, tick_location)
    
    n_steps = 30
    extent = list(ax.get_extent(ccrs.PlateCarree()))
    
    extent[0]=ext[0]
    extent[1]=ext[1]
    #extent=ext
    #print(extent)
    #if abs(extent[0])==abs(extent[0])
    _ticks = []
    for t in ticks:
        xy = line_constructor(t, n_steps, extent)
        proj_xyz = ax.projection.transform_points(ccrs.Geodetic(), xy[:, 0], xy[:, 1])
        xyt = proj_xyz[..., :2]
        
        ls = sgeom.LineString(xyt.tolist())
        
        locs = axis.intersection(ls)
        
        if not locs:
            tick = [None]
        else:
            if str(locs)[0]!="M":
                tick = tick_extractor(locs.xy)
            else:
                tick = tick_extractor(locs[0].xy)
        _ticks.append(tick[0])
    # Remove ticks that aren't visible:    
    ticklabels = copy(ticks)
    while True:
        try:
            index = _ticks.index(None)
        except ValueError:
            break
        _ticks.pop(index)
        ticklabels.pop(index)
    return _ticks, ticklabels


def makePic(st_ra,st_dec,scale,thres):
    ra,dec,mag = loadtxt('catalogue/asu.tsv',delimiter="\t", skiprows = 47 , usecols=(0,1,5),unpack=True)

    ra=-ra
    ra=ra[mag<thres]
    dec=dec[mag<thres]
    mag=mag[mag<thres]

    
    fig = plt.figure()
    
    
    
    
    
    
    mag=mag-20
    mag=abs(mag)
    minim=min(mag)
    mag=mag-min(mag)+3
    maxx=max(mag)
    mag=mag/max(mag)*5.5
    
    
    
    
    if abs(st_dec)<=85:
        central_lon, central_lat = -st_ra, st_dec
    else:
        central_lon, central_lat = -st_ra, st_dec/abs(st_dec)*85
    
    
    lonlim=np.sin(abs(central_lat)*3.1415/180)*15+10
    if abs(central_lat)>80:
    #    print("180")
        lonlim=30/np.sqrt(scale)
    
    miny=central_lat-10*scale
 
    maxy=central_lat+10*scale
    
    
    extent = [(Angle((central_lon-lonlim*scale)*u.degree).wrap_at(360 * u.deg)).deg, (Angle((central_lon+lonlim*scale)*u.degree).wrap_at(360 * u.deg)).deg, miny, maxy]
    ax = plt.axes(projection=ccrs.Orthographic(central_lon, central_lat))
    ax.set_extent(extent)
    fig.canvas.draw()
    
    if abs(central_lat)<80:
        if scale>1:
            xticks = [central_lon-i for i in range(-180,181,20)]
        else:
            xticks = [central_lon-i for i in range(-90,91,10)]
        yticks = [central_lat-i for i in range(-60,61,5) if abs(central_lat-i)>=20 and abs(central_lat-i)<=85]
    if abs(central_lat)<75:
        if abs(central_lat)>50:
            if scale>1:
                xticks = [central_lon-i for i in range(-135,136,20)]
            else:
                xticks = [central_lon-i for i in range(-60,61,10)]
            yticks = [central_lat-i for i in range(-60,61,5) if abs(central_lat-i)>=20 and abs(central_lat-i)<=85]
        else:
            
            xticks = [central_lon-i for i in range(-80,81,10)]
            yticks = [central_lat-i for i in range(-60,61,5) if abs(central_lat-i)<=85]
            
        
    if abs(central_lat)>=80:
        xticks = [i for i in range(0,-361,-20)]
        yticks = [central_lat-i for i in range(-60,61,5) if abs(central_lat-i)<=85]
        
        
        
    
    
    ax.gridlines(xlocs=xticks, ylocs=yticks)
    
    
    if scale>1:
        ext=[(central_lon-1.5*lonlim*scale), (central_lon+1.5*lonlim*scale), central_lat-2*10*scale, central_lat+2*10*scale]
    else:
        ext=[(central_lon-3*lonlim*scale), (central_lon+3*lonlim*scale), central_lat-3*10*scale, central_lat+3*10*scale]
    
    
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x,pos: str(int((Angle(abs(x)*u.degree).wrap_at(360 * u.deg)).hms[0]))+"h"+str(int((Angle(abs(x)*u.degree).wrap_at(360 * u.deg)).hms[1]))+"m")) 
    lambert_xticks(ax, xticks,central_lat,ext)
    if central_lat<0:
        ax.xaxis.tick_top()
    else:
        ax.xaxis.tick_bottom()
    
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.2f}"))
    lambert_yticks(ax, yticks,ext)
    
    scatter=ax.scatter(ra, dec,s=(mag**3),c='black',transform=ccrs.Geodetic())#PlateCarree
    ax.scatter(central_lon, st_dec,s=10,c='red',transform=ccrs.Geodetic())#PlateCarree
    
    kw = dict(prop="sizes", num=7, fmt="{x:.2f}", func=lambda s: (((s)**(1/3))/5.5*maxx-3+minim))
    a=scatter.legend_elements(**kw)
    
    for i in range(len(a[1])):
        a[1][i]=str(float(a[1][i])*(-1)+20)
    
    
    legend2 = ax.legend(*a, loc="lower right", title="Mag")
    
    
    
    return fig
    
    
if __name__ == '__main__':

    makePic(200,-48,2,6)
    plt.show()
    #i_mass=[]
    #j_mass=[]
   # 
   # for i in range(0,360,1):
   #     print(i)
   #     for j in range(-90,90,1):
   #         try:
   #             makePic(i,j,1)
   #         except:
   #             print(i,j)
   #             i_mass.append(i)
   #             j_mass.append(j)
   ##         finally:
    #            plt.close()
    #    
    
  #  plt.scatter(i_mass,j_mass)
  #  plt.show()
    #plt.show()
    
    
    
    
