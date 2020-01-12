#!/usr/bin/env python
import gcn
import logging
import telegram
import datetime as dt

try:
    with open('./handle') as f:
        my_handle = f.read().strip()
except OSError:
    print('no handle, can\'t work')
    exit(1)

try:
    with open('./token') as f:
        my_token = f.read().strip()
except OSError:
    print('no token, can\'t work')
    exit(1)
try:
    with open('./proxy') as f:
        url, un, pw = f.read().strip().split(',')
        REQUEST_KWARGS = {
            'proxy_url': '{}'.format(url),
            # Optional, if you need authentication:
            'urllib3_proxy_kwargs': {
                'username': '{}'.format(un),
                'password': '{}'.format(pw),
            }
        }
        req = telegram.utils.request.Request(**REQUEST_KWARGS)
except OSError:
    req = telegram.utils.request.Request()
    print('no proxy file, not using it')


def send(msg, chat_id, token=my_token):
    bot = telegram.Bot(token=token, request=req)
    bot.sendMessage(chat_id=chat_id, text=msg, parse_mode='Markdown')


def gcn_handler(payload, root):
    # if root.attrib['role'] == 'test':
    # return
    print(root.attrib['ivorn'])
    msg = root.attrib['ivorn']
    params = {elem.attrib['name']:
              elem.attrib['value']
              for elem in root.iterfind('.//Param')}
    for key, value in params.items():
        print(key, '=', value)
        msg = '{msg}\n\
        **{key}** = {value}'.format(msg=msg, key=key, value=value)
    try:
        pos2d = root.find('.//{*}Position2D')
        ra = float(pos2d.find('.//{*}C1').text)
        dec = float(pos2d.find('.//{*}C2').text)
        radius = float(pos2d.find('.//{*}Error2Radius').text)
        print('ra = {:g}, dec={:g}, radius={:g}'.format(ra, dec, radius))
        msg = '{msg}\n\
        Coord data available!\n\
        RA={ra}\n\
        DE={de}\n\
        EB={eb}\n'.format(msg=msg, ra=ra, de=dec, eb=radius)
    except AttributeError:
        print("no coords")
        msg = msg + '\nNo coord data'
    send(msg, my_handle, my_token)


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    send('GCN Alert system starting at {now}'.format(now=dt.datetime.now().isoformat()), my_handle, my_token)
    gcn.listen(handler=gcn_handler)
