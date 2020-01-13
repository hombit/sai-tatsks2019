#! /usr/bin/env python3
import requests
import json
import random
import sys
import time
from astropy import units as u
from astropy.coordinates import SkyCoord

def form_file_request(filename, args={}):
    try:
        f = open(filename, 'rb')
        file_args = (filename, f.read())
    except IOError:
        print('File %s does not exist' % filename)
        raise

    boundary_key = ''.join([random.choice('0123456789') for i in range(19)])
    boundary = '===============%s==' % boundary_key
    headers = {'Content-Type':
               'multipart/form-data; boundary="%s"' % boundary}
    data_pre = (
        '--' + boundary + '\n' +
        'Content-Type: text/plain\r\n' +
        'MIME-Version: 1.0\r\n' +
        'Content-disposition: form-data; name="request-json"\r\n' +
        '\r\n' +
        json.dumps(args) + '\n' +
        '--' + boundary + '\n' +
        'Content-Type: application/octet-stream\r\n' +
        'MIME-Version: 1.0\r\n' +
        'Content-disposition: form-data; name="file"; filename="%s"' % 
        file_args[0] + '\r\n' + '\r\n')
    data_post = ('\n' + '--' + boundary + '--\n')
    data = data_pre.encode() + file_args[1] + data_post.encode()
    f.close()
    return (headers, data)


if __name__ == '__main__':
	try:
	    with open("key") as key_file:
	        key = key_file.readline()
	except FileNotFoundError:
	    print("You should put a file named 'key' (with appropriate" + 
	    	  "astrometry API key in it) in the folder with this script")
	    sys.exit(0)

	print("Connectig to server...")
	try:
	    R = json.loads(requests.post('http://nova.astrometry.net/api/login', 
	    	                         data={'request-json': json.dumps({"apikey": key})}).text)
	except:
	    print("Can't connect to server")
	    sys.exit(0)

	if R["status"] == "error":
	    print(R["errormessage"])
	    sys.exit(0)
	    
	session = R['session']
	print("Connected to astrometry server")

	print("Session id is ", session)

	args = {"session": session}

	file_req = form_file_request(sys.argv[1], args=args)

	print("Uploading file...")
	try:
	    R2 = json.loads(requests.post('http://nova.astrometry.net/api/upload',
	                                  data=file_req[1], headers=file_req[0]).text)
	    
	except:
	    print("Connection error")
	    sys.exit(0)

	if R2["status"] == "error":
	    print(R2["errormessage"])
	    sys.exit(0)

	subid = R2['subid']
	print("Successfully uploaded file")
	print("Submission id is ", subid)


	start_t = time.time()
	nerrors = 0

	while (nerrors < 10):
	    try:
	        R2D = json.loads(requests.get('http://nova.astrometry.net/api/submissions/'
	                                      + str(subid)).text)
	    except:
	        nerrors += 1
	        print("Connection error ", nerrors)
	    else:
	        if 'error_message' in R2D:
	            print("File processing error!")
	            print(R2D['error_message'])
	            sys.exit(0)
	        nerrors = 0;
	        print('Processing time is: ', 
	        	time.strftime('%H:%M:%S', time.gmtime(time.time() - start_t)))
	        if (len(R2D["job_calibrations"]) > 0):
	            print("Successfully calibrated")
	            break
	        
	    time.sleep(10)
	    
	if (nerrors >= 10):
	    print("Lost connection")
	    sys.exit(0)
	    

	job = R2D["jobs"][0]
	try:
	    R2D2 = json.loads(requests.get('http://nova.astrometry.net/api/jobs/' 
	    	                           + str(job) + '/calibration').text)
	except:
	    print("Cant't obtain calibration data")
	    sys.exit(0)
	    
	RA = R2D2['ra']*u.deg
	DEC = R2D2['dec']*u.deg

	w = R2D2["width_arcsec"]*u.arcsec
	h = R2D2["height_arcsec"]*u.arcsec

	coord = SkyCoord(ra=RA, dec=DEC)
	print()
	print("Center coordinates: ", coord.to_string('hmsdms'))

	print('Image width: ', w)
	print('Image height ', h)
	print()