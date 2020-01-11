from __future__ import unicode_literals
import requests
import numpy as np
from io import BytesIO
from astropy.io.votable import parse_single_table
from astropy.table import Table

def main():
    print('Ввести координаты (y) или использовать по умолчанию (n)?')
    ans = input()
    if ans == 'n':
        RA = 298.0025
        DEC = 29.87147
    elif ans == 'y': 
        print('Введите RA, DEC:')
        RA, DEC = map(float, input().split(', '))
        
    response_g = requests.get('https://irsa.ipac.caltech.edu/cgi-bin/ZTF/nph_light_curves?POS=CIRCLE ' + str(RA) + ' ' + str(DEC) + ' 0.0014&BANDNAME=g')
    if response_g.status_code == 200:
        print('OK')
        res_g = response_g.content
        obj_g = BytesIO(res_g)
        table_g = parse_single_table(obj_g)
        data_g = Table(table_g.array)
        if (len(data_g) != 0):
            objects_g = np.unique(np.array(data_g['oid']))
            mag_g = np.array(data_g['mag'])
            magerr_g = np.array(data_g['magerr'])
            for k in objects_g:
                if np.where(np.array(data_g['oid']) == k)[0][-1] - np.where(np.array(data_g['oid']) == k)[0][0] < 100:
                    mag_g = np.delete(mag_g, np.where(data_g['oid'] == k)[0])
                    magerr_g = np.delete(magerr_g, np.where(data_g['oid'] == k)[0])   
            g = np.sum(mag_g/((magerr_g)**2))/np.sum(1/((magerr_g)**2))
            gerr = np.sqrt(1/(np.sum(1/((magerr_g)**2))))
            response_r = requests.get('https://irsa.ipac.caltech.edu/cgi-bin/ZTF/nph_light_curves?POS=CIRCLE ' + str(RA) + ' ' + str(DEC) + ' 0.0014&BANDNAME=r')
            if response_g.status_code == 200:
                print('OK')
                res_r = response_r.content
                obj_r = BytesIO(res_r)
                table_r = parse_single_table(obj_r)
                data_r = Table(table_r.array)
                if (len(data_r) != 0):
                    objects_r = np.unique(np.array(data_r['oid']))
                    mag_r = np.array(data_r['mag'])
                    magerr_r = np.array(data_r['magerr'])
                    for k in objects_r:
                        if np.where(np.array(data_r['oid']) == k)[0][-1] - np.where(np.array(data_r['oid']) == k)[0][0] < 100:
                            mag_r = np.delete(mag_r, np.where(data_r['oid'] == k)[0])
                            magerr_r = np.delete(magerr_r, np.where(data_r['oid'] == k)[0]) 
                    r = np.sum(mag_r/((magerr_r)**2))/np.sum(1/((magerr_r)**2))
                    rerr = np.sqrt(1/(np.sum(1/((magerr_r)**2))))
                    gr = g-r
                    grerr = np.sqrt(gerr**2 + rerr**2)
                    print('g - r: ' + str(gr) + ' +- ' + str(grerr))
                else:
                    print('В r нет объекта с такими координатами!')
            else:
                print('err: ' + str(response_g.status_code))
        else:
            print('В g нет объекта с такими координатами!')
    else:
        print('err: ' + str(response_g.status_code))

      
if __name__ == '__main__':
    main()
    


