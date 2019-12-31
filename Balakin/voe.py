#!/usr/bin/env python3
import gcn
from discord_webhook import DiscordWebhook, DiscordEmbed
import datetime
import re
import sys
import lxml

discord_key = 'discordkey_empty'
if discord_key == '' or discord_key == 'discordkey_empty':
    try:
        with open("./discord_apikey", 'r') as pw_file:
            discord_key = pw_file.read().strip()
    except FileNotFoundError:
        print('api key is not set and ./discord_apikey is absent, discord notifications will not work')
        exit(1)

socket_name = {1: 'BATSE_ORIGINAL',
               2: 'Test coords',
               3: 'Imalive',
               4: 'Kill',
               11: 'BATSE_MAXBC',
               21: 'Bradford Test',
               22: 'BATSE_FINAL',
               24: 'BATSE_LOCBURST',
               25: 'ALEXIS',
               26: 'XTE-PCA Alert',
               27: 'XTE-PCA Source',
               28: 'XTE-ASM Alert',
               29: 'XTE-ASM Source',
               30: 'COMPTEL',
               31: 'IPN_Raw',
               32: 'IPN_Segment',
               33: 'SAX-WFC Alert',
               34: 'SAX-WFC Source',
               35: 'SAX-NFI Alert',
               36: 'SAX-NFI Source',
               37: 'RXTE-ASM_XTRANS',
               38: 'spare for development testing',
               39: 'IPN_Position',
               40: 'HETE_S/C_ALERT Source',
               41: 'HETE_S/C_UPDATE Source',
               42: 'HETE_S/C_LAST Source',
               43: 'HETE_GROUND_ANALYSIS Source',
               44: 'HETE_Test Source',
               45: 'GRB_COUNTERPART Source',
               46: 'SWIFT_TOO_FOM_OBSERVE',
               47: 'SWIFT_TOO_SC_SLEW',
               48: 'DOW_TOD Test',
               51: 'INTEGRAL_POINTDIR',
               52: 'INTEGRAL_SPIACS',
               53: 'INTEGRAL_WAKEUP Source',
               54: 'INTEGRAL_REFINED Source',
               55: 'INTEGRAL_OFFLINE Source',
               56: 'INTEGRAL_WEAK Source',
               57: 'AAVSO Event',
               58: 'MILAGRO Source',
               59: 'KONUS_Lightcurve',
               60: 'SWIFT_BAT_GRB_ALERT',
               61: 'SWIFT_BAT_GRB_POSITION Source',
               62: 'SWIFT_BAT_GRB_NACK_POSITION',
               63: 'SWIFT_BAT_GRB_LIGHTCURVE',
               64: 'SWIFT_BAT_SCALED_MAP',
               65: 'SWIFT_FOM_OBSERVE',
               66: 'SWIFT_SC_SLEW',
               67: 'SWIFT_XRT_POSITION Source',
               68: 'SWIFT_XRT_SPECTRUM',
               69: 'SWIFT_XRT_IMAGE',
               70: 'SWIFT_XRT_LIGHTCURVE',
               71: 'SWIFT_XRT_NACK_POSITION',
               72: 'SWIFT_UVOT_IMAGE',
               73: 'SWIFT_UVOT_SRC_LIST',
               76: 'SWIFT_BAT_GRB_LIGHTCURVE_PROC',
               77: 'SWIFT_XRT_SPECTRUM_PROC',
               78: 'SWIFT_XRT_IMAGE_PROC',
               79: 'SWIFT_UVOT_IMAGE_PROC',
               80: 'SWIFT_UVOT_SRC_LIST_PROC',
               81: 'SWIFT_UVOT_POSITION Source',
               82: 'SWIFT_BAT_GRB_POS_TEST Source',
               83: 'SWIFT_POINTDIR',
               84: 'SWIFT_BAT_TRANS Source',
               85: 'SWIFT_XRT_THRESHPIX',
               86: 'SWIFT_XRT_THRESHPIX_PROC',
               87: 'SWIFT_XRT_SPER',
               88: 'SWIFT_XRT_SPER_PROC',
               89: 'SWIFT_UVOT_NACK_POSITION',
               97: 'SWIFT_BAT_QUICKLOOK_POSITION Source',
               98: 'SWIFT_BAT_SUBTHRESHOLD_POSITION Source',
               99: 'SWIFT_BAT_SLEW_GRB_POSITION Source',
               100: 'SuperAGILE_GRB_POS_WAKEUP Source',
               101: 'SuperAGILE_GRB_POS_GROUND Source',
               102: 'SuperAGILE_GRB_POS_REFINED Source',
               103: 'SWIFT_ACTUAL_POINTDIR',
               105: 'AGILE_MCAL_ALERT',
               107: 'AGILE_POINTDIR',
               109: 'SuperAGILE_GRB_POS_TEST Source',
               110: 'FERMI_GBM_ALERT',
               116: 'FERMI_GBM_ALERT_INT',
               111: 'FERMI_GBM_FLT_POS Source',
               117: 'FERMI_GBM_FLT_INT Source',
               112: 'FERMI_GBM_GND_POS Source',
               114: 'FERMI_GBM_GND_INT Source',
               115: 'FERMI_GBM_FINAL_POS Source',
               119: 'FERMI_GBM_POS_TEST Source',
               120: 'FERMI_LAT_GRB_POS_INI Source',
               121: 'FERMI_LAT_GRB_POS_UPD Source',
               122: 'FERMI_LAT_GRB_POS_DIAG Source',
               123: 'FERMI_LAT_TRANS Source',
               124: 'FERMI_LAT_GRB_POS_TEST Source',
               125: 'FERMI_LAT_MONITOR',
               126: 'FERMI_SC_SLEW',
               144: 'FERMI_SC_SLEW_INT',
               127: 'FERMI_LAT_GND Source',
               128: 'FERMI_LAT_OFFLINE Source',
               129: 'FERMI_POINTDIR',
               130: 'SIMBAD/NED Search Results',
               131: 'FERMI_GBM_SUBTHRESHOLD transient',
               133: 'SWIFT_BAT_MONITOR',
               134: 'MAXI_UNKNOWN_SOURCE',
               135: 'MAXI_KNOWN_SOURCE',
               136: 'MAXI_TEST',
               137: 'OGLE',
               139: 'MOA',
               140: 'SWIFT_BAT_SUB_SUB_THRESH_POS',
               141: 'SWIFT_BAT_KNOWN_SOURCE_POS',
               145: 'Coincidence',
               146: 'FERMI_GBM_FINAL_POS_INT Source',
               148: 'SUZAKU_Lightcurve',
               149: 'SNEWS',
               150: 'LVC_PRELIMIARY',
               151: 'LVC_INITIAL',
               152: 'LVC_UPDATE',
               153: 'LVC_TEST',
               154: 'LVC_COUNTERPART',
               157: 'AMON_ICECUBE_COINC',
               158: 'AMON_ICECUBE_HESE',
               159: 'AMON_ICECUBE_TEST',
               160: 'CALET_GBM_FLT_LC',
               161: 'CALET_GBM_GND_LC',
               164: 'LVC_RETRACTION',
               166: 'AMON_ICECUBE_CLUSTER',
               168: 'GWHEN_COINC',
               169: 'AMON_ICECUBE_EHE',
               170: 'AMON_ANTARES_FERMILAT_COINC',
               171: 'HAWC_BURST_MONITOR',
               172: 'AMON_GAMMA_NU_COINC',
               173: 'ICECUBE_ASTROTRACK_GOLD',
               174: 'ICECUBE_ASTROTRACK_BRONZE'}


@gcn.handlers.include_notice_types(
    gcn.notice_types.LVC_PRELIMINARY,
    gcn.notice_types.LVC_INITIAL,
    gcn.notice_types.LVC_UPDATE,
    gcn.notice_types.LVC_RETRACTION,)
def process_gcn(payload, root):
    """Handler-функция для gcn.listen
    На вход принимает
    payload = open(file, 'rb').read()
    root = lxml.etree.fromstring(payload)
    Отдаёт кучу всего в stdout и отправляет сообщение в дискорд-канал по API ключу
    """
    # Переключение тестовых алертов и реальных
    # if root.attrib['role'] != 'observation':
    #    return
    if root.attrib['role'] == 'test':
        return

    params = {elem.attrib['name']:
              elem.attrib['value']
              for elem in root.iterfind('.//Param')}

    print("NEW MESSAGE TYPE={type}".format(type=params['Packet_Type']), flush=True)
    # Print all parameters.
    for key, value in params.items():
        print(key, '=', value, flush=True)
    trigtime_object = datetime.datetime.strptime(root.find('.//{*}ISOTime').text.strip(), "%Y-%m-%dT%H:%M:%S.%f")
    print("trig_time=", trigtime_object.strftime("%Y-%m-%d %H:%M:%S"))
    noticetime_object = datetime.datetime.now()
    print("notice_time=", noticetime_object.strftime("%Y-%m-%d %H:%M:%S"))
    if 'skymap_fits' not in params:
        try:
            pos2d = root.find('.//{*}Position2D')
            ra = float(pos2d.find('.//{*}C1').text)
            print("RA=", ra, flush=True)
            dec = float(pos2d.find('.//{*}C2').text)
            print("DEC=", dec, flush=True)
            err = float(pos2d.find('.//{*}Error2Radius').text)
            print("errorbox=", err, flush=True)
            has_coords = True
        except AttributeError:
            has_coords = False
    else:
        has_coords = False
    print("===END===", flush=True)
    webhook = DiscordWebhook(url=discord_key)
    embed = DiscordEmbed(title=socket_name[int(params['Packet_Type'])] + '({})'.format(params['Packet_Type']), description='seq=' + params['Pkt_Ser_Num'], color=242424)
    embed.set_timestamp(timestamp=datetime.datetime.now().isoformat())
    if 'GraceID' in params:
        embed.add_embed_field(name='GraceID', value=params['GraceID'])
    if 'Instruments' in params:
        embed.add_embed_field(name='Instruments', value=params['Instruments'])
    if ('GraceID' in params):
        image_data = re.search('^.*/(\w+)\.fits\.gz(,\d)\s*$', params['skymap_fits'], flags=re.I + re.M)
        embed.set_image(url='https://gracedb.ligo.org/api/superevents/{graceid}/files/{pipeline}.png{seq}'.format(
            graceid=params['GraceID'], pipeline=image_data.group(1), seq=image_data.group(2)))
    if 'AlertType' in params:
        embed.add_embed_field(name='Alert Type', value=params['AlertType'])
    if 'TrigID' in params:
        embed.add_embed_field(name='TrigID', value=params['TrigID'])
    if 'EventPage' in params:
        embed.add_embed_field(name='Event Page', value=params['EventPage'])
    if 'BNS' in params:
        embed.add_embed_field(name='BNS  NSBH BBH  GAP  Terr', value="{:2.2f} {:2.2f} {:2.2f} {:2.2f} {:2.2f}".format(
            float(params['BNS']), float(params['NSBH']), float(params['BBH']), float(params['MassGap']), float(params['Terrestrial']),), inline=False)
    if has_coords:
        embed.add_embed_field(name='Localisation', value="{ra} d {dec} d {eb}".format(ra=ra, dec=dec, eb=err))
    embed.add_embed_field(name='Trigger time', value=trigtime_object.strftime("%Y-%m-%d %H:%M:%S"))
    embed.add_embed_field(name='Notice time', value=noticetime_object.strftime("%Y-%m-%d %H:%M:%S"))
    webhook.add_embed(embed)
    response = webhook.execute()
    if response.ok is False:
        print(response.status_code, response.text)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        file = sys.argv[1]
        payload = open(file, 'rb').read()
        root = lxml.etree.fromstring(payload)
        process_gcn(payload, root)
    else:
        print("###Starting listen daemon now!", flush=True)
        gcn.listen(handler=process_gcn)
