import requests
import os

# scan_type_options = ['ProfilometerScanInTrackLine',
#                      'ProfilometerScanCrossTrackLine',
#                      'ProfilometerScanCrossCylinderLine',
#                      ]

scan_type_options = {'itl': 'ProfilometerScanInTrackLine',
                     'ctl': 'ProfilometerScanCrossTrackLine',
                     'ccl': 'ProfilometerScanCrossCylinderLine',
                     }

db_url = r'http://131.246.251.61:3000/profilometer_scans'
upload2db_path = r'E:\KF_Tribologie\_frt_backup\upload_to_db'

def log(file_path, success):
    folder_path, file_name = os.path.split(file_path)
    file_name = file_name[:file_name.rfind('.zip')]
    if success:
        file_name += "_upload_successful.log"
        with open(os.path.join(os.path.split(upload2db_path)[0] , 'log',file_name), 'w+'):
            pass
    else:
        file_name+= "_upload_FAILED.log"
        with open(os.path.join(os.path.split(upload2db_path)[0] ,'log',file_name), 'w+'):
            pass

def to_DB(file_path, scan_type):
    # if scan_type == 'ctl':
    #     option_idx = 1
    # elif scan_type == 'itl':
    #     option_idx = 0
    # elif scan_type == 'ccl':
    #     option_idx = 2

    if not scan_type in scan_type_options.keys():
        print('Fehler im Scantyp')

    #with open('{}/{}'.format(upload2db_path, filename), 'rb') as f:
    with open('{}'.format(file_path), 'rb') as f:
        try:
            r = requests.post(db_url,
                              data={'profilometer_id': 1, 'scan_type': scan_type_options[scan_type]},
                              files={'file_to_upload': f},
                              timeout=5,
                              )
            is_file_sent = True
        except requests.Timeout:
            is_file_sent = False

        if is_file_sent:
            r_str = str(r)
            if '201' in r_str:
                print('{}: Upload erfolgreich, Scan neu angelegt [201]'.format(file_path))
                log(file_path, success=True)
            elif '204' in r_str:
                print('{}: Upload erfolgreich, Scan aktualisiert [204]'.format(file_path))
                log(file_path, success=True)
            elif '500' in r_str:
                print('{}: Hochladen fehlgeschlagen [500]'.format(file_path))
                log(file_path, success=False)
            else:
                print('{}: Response: {}'.format(file_path, r))
                log(file_path, success=False)
        else:
            print('Verbindung mit dem Server fehlgeschlagen!')
    return r_str


if __name__ == '__main__':
    import os

    filenames = os.listdir(upload2db_path)
    if len(filenames) == 0:
        print('Keine Dateien gefunden! Bitte prüfen')
    else:
        for filename in filenames:
            scan_type = filename.split('.')
            temp = to_DB(file_path="{}".format(os.path.join(upload2db_path,filename)),
                  # upload2db_path=upload2db_path,
                  scan_type=scan_type[3],
                  # db_url=db_url,
                  )
    input('Irgendeine Taste drücken zum beenden ')
