DEBUG = True
import os
import shutil
import datetime
import frt_zip as frt_zip
import frt_send2DB as db_post

if not DEBUG:
    import frt_motor as frt


def generate_line_wsf(fn, start_x, end_x, start_y, end_y, points, set_autofocus, measurement_rate):
    f = open("measurement.wsf".format(fn), 'w+')

    f.write("<job>\n")
    f.write('<?job debug="true"?>\n')
    f.write('<script language="VBScript" src="LIB_IniAccess.wsf" />\n')
    f.write('<script language="VBScript" src="LIB_Acquire.wsf" />\n')
    f.write('<script language="VBScript" src="LIB_AcquireError.wsf" />\n')
    f.write('<script language="VBScript">\n')
    f.write('Option Explicit\n')
    f.write('IniAccess_Initialize\n')
    f.write('dim Acquire\n')
    f.write('dim AcquireError\n')
    f.write('dim filename\n')
    f.write('dim filenamesave\n')
    f.write('Set Acquire = new AcquireClass\n')
    f.write('Set AcquireError = new AcquireErrorClass\n')
    f.write('dim state, ok\n')
    f.write('Acquire.Init\n')
    f.write('StartProgram ("C:ProgrammeAcquireAcquire.exe")\n')
    f.write('Acquire.SetParam "CreateSet", "Actual"\n')
    f.write('Acquire.SetParam "AutoApproach","{}"\n'.format(str(bool(set_autofocus)).upper()))
    f.write('Acquire.SetParam "MeasRate", ' + str(measurement_rate) + "\n")
    f.write('Acquire.SetParam "AutoRetract","FALSE"\n')
    f.write('Acquire.SetParam "ScanMode", "2D"\n')
    f.write('Acquire.SetParam "DisplayStartBox","FALSE"\n')
    f.write('Acquire.SetParam "PointsPerLine", ' + str(points))
    f.write('\n')

    f.write('Acquire.SetParam "StartX", ' + str(start_x) + "\n")
    f.write('Acquire.SetParam "StartY", ' + str(start_y) + "\n")
    f.write('Acquire.SetParam "EndX", ' + str(end_x) + "\n")
    f.write('Acquire.SetParam "EndY", ' + str(end_y) + "\n")

    f.write('Acquire.SetParam "UseSet", Empty\n')
    f.write('Acquire.StartScan\n')
    f.write('Acquire.WaitForScanFinished\n')
    # f.write('Acquire.SaveData "' + fn + '", "FRT"\n')
    f.write('filename = "' + fn + '"\n')
    f.write('filename = Replace(filename, "/", "\\")\n')
    f.write('filenamesave = filename & ".txt"\n')
    f.write('Acquire.SaveData filenamesave, "ASCII"\n')
    f.write('filenamesave = filename & ".frt"\n')
    f.write('Acquire.SaveData filenamesave, "FRT"\n')

    f.write('</script>\n')
    f.write('</job>\n')
    f.close()

    return


def input_params(params):
    # params = {}

    params['sample_geometry'] = input("Probengeometrie? (Ring, Scheibe): ")
    params['sensor_type'] = input("Sensor? (1 = 0,3 mm, 2 = 3 mm): ")
    params['test_id'] = input("Probenname (WearTestID, SpecimenID)?: ")
    params['segment_no'] = input('Segmentnr.: ')
    params['sample_condition'] = input('1: pre, 2: post, 3: post-clean: ')
    params['measurement_mode'] = input('measurement mode (1: ctl, 2: itl): ')
    params['measurement_rate'] = input('measurement rate [Hz], e.g. 1000, 300 or 100 ): ')
    params['position_start'] = input("Spuranfang [mm]: ")
    params['rim_surplus'] = input('Spurüberstand [mm]: ')
    params['measurement_length'] = input("Spurbreite [mm]: ")
    params['n_measurements'] = input('Anzahl Messungen?: ')
    params['pixel_distance'] = input('Pixelabstand [um] ?: ')
    params['send_to_db'] = input('An DB senden? 0 = Nein, 1 = Ja ')
    params['set_autofocus'] = input('Autofokus? 0 = Aus, 1 = An ')
    check_input_params(params)
    return params


def check_input_params(params):
    if params['sample_geometry'] not in ['Scheibe', 'Ring']:
        print('Error_geometry')

    try:
        params['test_id'] = int(params['test_id'])
        params['n_measurements'] = int(params['n_measurements'])
        params['segment_no'] = int(params['segment_no'])
        params['sample_condition'] = int(params['sample_condition'])
        params['pixel_distance'] = int(params['pixel_distance'])
        params['position_start'] = float(params['position_start'].replace(',', '.'))
        params['measurement_length'] = float(params['measurement_length'].replace(',', '.'))
        params['sensor_type'] = int(params['sensor_type'])
        params['measurement_mode'] = int(params['measurement_mode'])
        params['send_to_db'] = int(params['send_to_db'])
        params['rim_surplus'] = float(params['rim_surplus'].replace(',', '.'))
        params['set_autofocus'] = int(params['set_autofocus'])
        params['measurement_rate'] = int(params['measurement_rate'])
        print('Inputs OK')
    except:
        print('Error with numbers, Redo your input')
        input_params(params)

    return


def get_step_transmission(n_measurements, gear_transmission):
    step_size = pow(2, 8) * 200 * gear_transmission / n_measurements
    print(step_size)
    for i in range(9):
        if step_size / pow(2, i) <= 200:
            res = 8 - i
            break
        else:
            res = 8 - i
    return res


def compute_additional_params(params):
    if params['sensor_type'] == 1 or params['sensor_type'] == '0.3 mm':
        params['x_ref'] = params['hardware_config']['x_pos_fine_sensor']
    elif params['sensor_type'] == 2 or params['sensor_type'] == '3.0 mm':
        params['x_ref'] = params['hardware_config']['x_pos_regular_sensor']

    if params['sample_condition'] == 1:
        params['sample_condition'] = 'pre'
    elif params['sample_condition'] == 2:
        params['sample_condition'] = 'post'
    elif params['sample_condition'] == 3:
        params['sample_condition'] = 'post-clean'

    if params['measurement_mode'] == 1:
        params['measurement_mode'] = 'ctl'
    elif params['measurement_mode'] == 2:
        params['measurement_mode'] = 'itl'

    params['x_start'] = params['x_end'] = params['x_ref']
    if params['sample_geometry'] == 'Ring':
        params['gear_transmission'] = 1.0
        # params['step_transmission'] = 1
        params['step_transmission'] = get_step_transmission(params['n_measurements'], params['gear_transmission'])
        print('step_transmission_final', params['step_transmission'])
        params['motor_current'] = 150
        params['motor_speed'] = 60
        params['y_start'] = params['hardware_config']['y_ref_ring'] + params['position_start'] - params[
            'rim_surplus']  # new
        params['y_end'] = params['y_start'] + params['measurement_length'] + 2 * params['rim_surplus']  # new
        params['steps_full_rot'] = 200

    elif params['sample_geometry'] == 'Scheibe':
        params['gear_transmission'] = 1.8
        # params['step_transmission'] = 1
        params['step_transmission'] = get_step_transmission(params['n_measurements'], params['gear_transmission'])
        params['motor_current'] = 150
        params['motor_speed'] = 60
        params['y_start'] = params['hardware_config']['y_ref_disk'] + params['position_start'] / 2 - params[
            'rim_surplus']  # new
        params['y_end'] = params['y_start'] + params['measurement_length'] + params['rim_surplus']  # new
        params['steps_full_rot'] = 360

    params['steps'] = int(
        (pow(2, params['step_transmission']) * (200 * params['gear_transmission'])) / params['n_measurements'])
    params['pixel_distance'] = round(
        abs(params['y_end'] - params['y_start']) * 1000 / params['pixel_distance'])
    params['filename'] = '{:08.0f}.{:04.0f}.{}.{}'.format(
        params['test_id'],
        params['segment_no'],
        params['sample_condition'],
        params['measurement_mode'],
    )
    params['recorded_at'] = frt_zip.get_timestamp()
    if DEBUG:
        print(params)
        # print(params_setup)
    return params


def to_yaml(params):
    import yaml

    yaml_file = {':{}'.format(k): v for (k, v) in params.items()}
    yaml_file[':hardware_config'] = {':{}'.format(k): v for (k, v) in params['hardware_config'].items()}

    with open('{url}/{fn}/{fn}.header.yaml'.format(url=params['backup_url'], fn=params['filename']), 'w+') as f:
        f.write(yaml.safe_dump(yaml_file))
    return


def process_measurement(params):
    ### Ordner erstellen ###
    file_path = os.path.join(params['backup_url'], params['filename'])
    params['path'] = params['backup_url']

    if not os.path.isdir(file_path):
        os.mkdir(file_path)

    ### Berechnung Daten für Messvorgang
    # Errechne Winkel pro Vollschritt
    deg_per_fstep = 1.8 / params['gear_transmission']
    deg_per_step = deg_per_fstep / pow(2, params['step_transmission']) * params['steps']

    # Errechne Iterationszahl für vollständige Messung
    # params['n_measurements'] = pow(2, params['step_transmission']) * sample.steps_full_rot
    # Ausgabe Informationen
    print("Winkel pro Schritt", deg_per_step)
    print("Anzahl Iterationen", params['n_measurements'], "\n")

    ### Setup Motor Initialization
    if not DEBUG:
        motor.configure(params['step_transmission'], params['motor_current'], params['motor_speed'])

    ##### Variablen für Messvorgang Main-Schleife
    # timestamp1 = 0  # Zeitstempel
    timestamp2 = 0
    print()
    for i in range(params['n_measurements']):
        ### Informationsausgabe (Iterationen, Winkel, Vorr. Endzeitpunkt als Uhrzeit)
        cur_deg = round(i * deg_per_step, 2)
        print("Iteration: ", i + 1, " von ", params['n_measurements'])
        print("Aktueller Winkel: ", cur_deg)
        timestamp1 = timestamp2
        timestamp2 = datetime.datetime.now()
        if i > 0:
            time_diff = timestamp2 - timestamp1
            time_finish = datetime.datetime.now() + time_diff * (params['n_measurements'] - i + 1)
            time_finish = time_finish.strftime("%d.%m.%Y, %H:%M:%S")
            print("Voraussichtlicher Endzeitpunkt: ", time_finish)

        # Generiere Messprotokoll
        print("generating wsf... ", end="")

        # define filename
        filename = '{}.a{:03.0f}-{:02.0f}'.format(os.path.join(file_path, params['filename']),
                                                  int(cur_deg), cur_deg * 100 % 100)
        generate_line_wsf(
            fn=filename,
            start_x=params['x_start'],
            end_x=params['x_end'],
            start_y=params['y_start'],
            end_y=params['y_end'],
            points=params['pixel_distance'],
            set_autofocus=bool(params['set_autofocus']),
            measurement_rate=params['measurement_rate'],
        )

        print("OK")

        # Ausführen des Messprotokolls
        print("executing wsf... ", end='')
        if not DEBUG:
            os.system("measurement.wsf")

        os.remove("measurement.wsf")
        print("OK")
        print()

        # Motorbewegung
        if not DEBUG and params['n_measurements'] > 1:
            motor.mov_abs(params['steps'])

    else:
        print()
        print('Seems to work. Congrats!')

        to_yaml(params)

    if not DEBUG:
        frt_zip.zip_files(url=params['backup_url'], fn=params['filename'])
        send2db(params)
    return


def motor_disconnect():
    # Serienschnittstelle schließen
    if not DEBUG:
        motor.disconnect()
    return


def debug_defaults():
    params['sample_geometry'] = 'Ring'
    params['sensor_type'] = '1'
    params['test_id'] = "00000000"
    params['segment_no'] = '0'
    params['sample_condition'] = '1'
    params['measurement_mode'] = '1'
    params['position_start'] = '2'
    params['rim_surplus'] = '2'
    params['measurement_length'] = '1'
    params['n_measurements'] = '1'
    params['pixel_distance'] = '10'
    params['send_to_db'] = '1'
    params['set_autofocus'] = '0'
    check_input_params(params)


def send2db(params):
    if params['send_to_db']:
        # db_post.to_DB(filename='{}.zip'.format(params['filename']),
        res_str = db_post.to_DB(file_path='{}.zip'.format(os.path.join(params['backup_url'], params['filename'])),
                      # upload2db_path=params['path'],
                      scan_type=params['measurement_mode'],
                      # db_url=params['db_url'],
                      )
        if '201' in res_str or '204' in res_str:
                shutil.rmtree(os.path.join(params['backup_url'], params['filename']))
        # shutil.rmtree('{url}/{fn}'.format(url=params['path'], fn=params['filename']))
        # mv_orig = '{}/{}.zip'.format(params['path'], params['filename'])
        # mv_dst = 'E:/KF_Tribologie/_frt_backup/{}.zip'.format(params['filename'])
        # mv_dst = '{}/{}.zip'.format(params['backup_url'], params['filename'])
        # shutil.copyfile(mv_orig, mv_dst)
        # if os.path.isfile(mv_dst):
        #     os.remove(mv_orig)


### Konfigurationsvariablen
params = {}
params['hardware_config'] = {}
params['hardware_config']['x_pos_fine_sensor'] = 50  # X-Position 0.300 mm Sensor ()
params['hardware_config']['x_pos_regular_sensor'] = 51  # X-Positon 3.00 mm Sensor

params['hardware_config']['y_ref_ring'] = 67.4  # Y-Position Referenz bei Ringen ()
params['hardware_config']['y_ref_disk'] = 0  # Y-Position Referenz bei Scheiben

# params['rim'] = 0  # Kantenlänge

if not DEBUG:
    params['backup_url'] = r'E:/KF_Tribologie/_frt_backup'
else:
    params['backup_url'] = r'C:\frt_backup'
params['db_url'] = r'http://131.246.251.61:3000/profilometer_scans'

# Motorinitialisierung
if not DEBUG:
    motor = frt.single_axis_motor()
    motor.connect()

if __name__ == '__main__':
    if DEBUG:
        debug_defaults()
        pass
    else:
        params = input_params(params)
    params = compute_additional_params(params)
    process_measurement(params)
    motor_disconnect()
