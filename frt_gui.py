version = '2020-11-16'
git_log = 'tbn'

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import frt_script as script
import numpy as np
import os
import db_request


def error_message(msg, wear_test_id=None):
    if msg == 'no_measurement_type_selected':
        res = r'No measurement type selected!'
    elif msg == 'wrong_number_type':
        res = r'Wrong numbers. Please check!'
    elif msg == 'identical_test_ids':
        res = r'Identical test IDs found. Please Check!'
    elif msg == 'no_sample_condition':
        res = r'Sample statte not selected. Please Check!'
    elif msg == 'test_id_does_not_exist':
        res = r'Wear test id "{:08d}" does not exist. Please check or create ID'.format(wear_test_id)
        return res

def callback_continue(wear_test_id):
    res = messagebox.askyesno('Verify',
                              r'Messung {} wurde schon mal durchgegeführt. Wollen Sie die Messung wiederholen?'.format(
                                  wear_test_id))
    return res

def define_style():
    offset_level1 = 9
    offset_level2 = 16

    style = {}
    style['bd'] = 1
    style['relief'] = 'flat'
    style['width_entry_level1'] = 22
    style['width_entry_level2'] = 22 - 3
    style['width_cbox_level1'] = style['width_entry_level1'] - 3
    style['width_cbox_level2'] = style['width_entry_level1'] - 3 - 3
    style['height'] = 1
    style['anchor'] = 'e'
    style['padx_level0'] = 0
    style['padx_level1'] = style['padx_level0'] + offset_level1
    style['padx_level2'] = style['padx_level1'] + offset_level2
    style['justify'] = tk.RIGHT
    return style


def edit_state(list_of_settings):
    """
    Turn widgets on and off
    :param list_of_settings: [(var, widget)]
    :return:
    """
    for i in range(len(list_of_settings)):
        if list_of_settings[i][0].get():
            if list_of_settings[i][2] == 'cbox':
                list_of_settings[i][1]['state'] = 'readonly'
            else:
                list_of_settings[i][1]['state'] = 'normal'
        else:
            list_of_settings[i][1]['state'] = 'disabled'
    return


class Line_menu():
    def __init__(self, root, offset):
        self.root = root
        self.offset = offset
        self.init_line_menu()

    def change_label_color(self, var):
        if var.get():
            self.line_label['fg'] = 'black'
        else:
            self.line_label['fg'] = 'red'

    def init_line_menu(self):
        # column label
        self.line_label = self.line_label(row=40, column=2)

        # widgets
        self.is_conduct_line_measurement = self.widget_is_conduct_line_measurement(row=40, column=2)
        self.test_id_text = self.widget_text_id(row=50, column=2)
        self.is_intermitted_test = self.widget_is_intermitted_test(row=60, column=2)
        self.segment_no = self.widget_segment_no(row=70, column=2)
        self.sample_condition = self.widget_sample_condition(row=80, column=2)
        self.starting_position = self.widget_starting_position(row=81, column=2)
        self.measurement_distance = self.widget_measurement_distance(row=82, column=2)

        # self.is_itl = self.widget_is_itl(row=83, column=2)
        # self.rim_surplus_itl = self.widget_rim_surplus_itl(row=84, column=2)
        # self.n_measurement_itl = self.widget_n_measurement_itl(row=85, column=2)
        # self.pixel_distance_itl = self.widget_pixel_distance_itl(row=87, column=2)
        # self.measurement_rate_itl = self.widget_measurement_rate_itl(row=88, column=2)

        self.is_ctl = self.widget_is_ctl(row=89, column=2)
        self.rim_surplus_ctl = self.widget_rim_surplus_ctl(row=90, column=2)
        self.n_measurement_ctl = self.widget_n_measurement_ctl(row=92, column=2)
        self.pixel_distance_ctl = self.widget_pixel_distance_ctl(row=93, column=2)
        self.measurement_rate_ctl = self.widget_measurement_rate_ctl(row=94, column=2)

    def line_label(self, row, column):
        line_label = tk.Label(self.root, text="Track {}".format(self.offset + 1, fg='red'), font=("Times", 12))
        line_label.grid(row=row, column=column + self.offset)
        return line_label

    def widget_is_conduct_line_measurement(self, row, column):
        is_conduct_line_measurement_var = tk.BooleanVar(value=1)
        is_conduct_line_measurement = tk.Checkbutton(self.root, variable=is_conduct_line_measurement_var,
                                                     command=lambda: self.change_label_color(
                                                         is_conduct_line_measurement_var))
        if self.offset == 0:
            is_conduct_line_measurement['state'] = 'disabled'
        is_conduct_line_measurement.grid(row=row, column=column + self.offset, sticky=tk.W, padx=33)

        return is_conduct_line_measurement_var

    def widget_rim_surplus_ctl(self, row, column):
        rim_surplus_text = tk.StringVar()
        rim_surplus = tk.Entry(self.root, textvariable=rim_surplus_text, width=style['width_entry_level2'],
                               # state='disabled',
                               )
        rim_surplus_text.set("1.0")
        rim_surplus.grid(row=row, column=column + self.offset, sticky=tk.W, padx=style['padx_level2'])
        return rim_surplus

    def widget_rim_surplus_itl(self, row, column):
        rim_surplus_text = tk.StringVar()
        rim_surplus = tk.Entry(self.root, textvariable=rim_surplus_text, width=style['width_entry_level2'],
                               state='normal')
        rim_surplus_text.set("0.2")
        rim_surplus.grid(row=row, column=column + self.offset, sticky=tk.W, padx=style['padx_level2'])
        rim_surplus['state'] = 'disabled'
        return rim_surplus

    def widget_pixel_distance_ctl(self, row, column):
        pixel_distance_ctl_options = ['1 \u03BCm', '2 \u03BCm', '5 \u03BCm', '10 \u03BCm']
        pixel_distance_ctl = ttk.Combobox(self.root, values=pixel_distance_ctl_options,
                                          # state="disabled",
                                          width=style['width_cbox_level2'])
        pixel_distance_ctl.set(pixel_distance_ctl_options[3])
        pixel_distance_ctl.grid(row=row, column=column + self.offset, sticky=tk.W, padx=style['padx_level2'])
        return pixel_distance_ctl

    def widget_measurement_rate_ctl(self, row, column):
        measurement_rate_ctl_options = ['1000 Hz', '300 Hz', '100 Hz']
        measurement_rate_ctl = ttk.Combobox(self.root, values=measurement_rate_ctl_options,
                                            # state="disabled",
                                            width=style['width_cbox_level2'])
        measurement_rate_ctl.set(measurement_rate_ctl_options[0])
        measurement_rate_ctl.grid(row=row, column=column + self.offset, sticky=tk.W, padx=style['padx_level2'])
        return measurement_rate_ctl

    def widget_n_measurement_ctl(self, row, column):
        n_measurement_ctl_var = tk.IntVar()
        n_measurement_ctl = tk.Entry(self.root, textvariable=n_measurement_ctl_var,
                                     width=style['width_entry_level2'],
                                     # state='disabled',
                                     )
        n_measurement_ctl_var.set("36")
        n_measurement_ctl.grid(row=row, column=column + self.offset, sticky=tk.W, padx=style['padx_level2'])
        return n_measurement_ctl

    def widget_is_ctl(self, row, column):
        is_ctl_var = tk.BooleanVar(value=1)
        is_ctl = tk.Checkbutton(self.root, variable=is_ctl_var,
                                command=lambda: edit_state([(is_ctl_var, self.rim_surplus_ctl, 'entry'),
                                                            (is_ctl_var, self.n_measurement_ctl, 'entry'),
                                                            (is_ctl_var, self.pixel_distance_ctl, 'cbox'),
                                                            (is_ctl_var, self.measurement_rate_ctl, 'cbox'),

                                                            ]))
        is_ctl.grid(row=row, column=column + self.offset, sticky=tk.W, padx=style['padx_level0'])
        is_ctl['state'] = 'disabled'
        return is_ctl_var

    def widget_is_itl(self, row, column):
        is_itl_var = tk.BooleanVar(value=0)
        is_itl = tk.Checkbutton(self.root, variable=is_itl_var,
                                command=lambda: edit_state([(is_itl_var, self.rim_surplus_itl, 'entry'),
                                                            (is_itl_var, self.n_measurement_itl, 'entry'),
                                                            (is_itl_var, self.pixel_distance_itl, 'cbox'),
                                                            (is_itl_var, self.measurement_rate_itl, 'cbox'),
                                                            ]))
        is_itl.grid(row=row, column=column + self.offset, sticky=tk.W, padx=style['padx_level0'])
        is_itl['state'] = 'disabled'
        return is_itl_var

    def widget_pixel_distance_itl(self, row, column):
        pixel_distance_itl_options = ['1 \u03BCm', '2 \u03BCm', '5 \u03BCm', '10 \u03BCm']
        pixel_distance_itl = ttk.Combobox(self.root, values=pixel_distance_itl_options, state="readonly",
                                          width=style['width_cbox_level2'])
        pixel_distance_itl.set(pixel_distance_itl_options[1])
        pixel_distance_itl.grid(row=row, column=column + self.offset, sticky=tk.W, padx=style['padx_level2'])
        pixel_distance_itl['state'] = 'disabled'
        return pixel_distance_itl

    def widget_measurement_rate_itl(self, row, column):
        pixel_distance_itl_options = ['1000 Hz', '300 Hz', '100 Hz']
        pixel_distance_itl = ttk.Combobox(self.root, values=pixel_distance_itl_options, state="readonly",
                                          width=style['width_cboxf_level2'])
        pixel_distance_itl.set(pixel_distance_itl_options[0])
        pixel_distance_itl.grid(row=row, column=column + self.offset, sticky=tk.W, padx=style['padx_level2'])
        pixel_distance_itl['state'] = 'disabled'
        return pixel_distance_itl

    def widget_n_measurement_itl(self, row, column):
        n_measurement_itl_var = tk.IntVar()
        n_measurement_itl = tk.Entry(self.root, textvariable=n_measurement_itl_var,
                                     width=style['width_entry_level2'])
        n_measurement_itl_var.set("10")
        n_measurement_itl.grid(row=row, column=column + self.offset, sticky=tk.W, padx=style['padx_level2'])
        n_measurement_itl['state'] = 'disabled'
        return n_measurement_itl

    def widget_measurement_distance(self, row, column):
        measurement_distance_text = tk.StringVar()
        measurement_distance = tk.Entry(self.root, textvariable=measurement_distance_text,
                                        width=style['width_entry_level1'])
        measurement_distance_text.set("4.0")
        measurement_distance.grid(row=row, column=column + self.offset, sticky=tk.W, padx=style['padx_level1'])
        return measurement_distance

    def widget_starting_position(self, row, column):
        starting_position_text = tk.StringVar()
        starting_position = tk.Entry(self.root, textvariable=starting_position_text,
                                     width=style['width_entry_level1'])
        starting_position_text.set("0.0")
        starting_position.grid(row=row, column=column + self.offset, sticky=tk.W, padx=style['padx_level1'])
        return starting_position

    def widget_sample_condition(self, row, column):
        self.sample_condition_options = ["pre-Test", "Post-Test", "cleaned"]
        sample_condition = ttk.Combobox(self.root, values=self.sample_condition_options, state="readonly",
                                        width=style['width_cbox_level1'])
        sample_condition.set(self.sample_condition_options[1])
        sample_condition.grid(row=row, column=column + self.offset, sticky=tk.W, padx=style['padx_level1'])
        return sample_condition

    def widget_is_intermitted_test(self, row, column):
        is_intermitted_test_var = tk.BooleanVar(value=0)
        is_intermitted_test = tk.Checkbutton(self.root, variable=is_intermitted_test_var,
                                             command=lambda: edit_state(
                                                 [(is_intermitted_test_var, self.segment_no, 'entry')]))
        is_intermitted_test.grid(row=row, column=column + self.offset, sticky=tk.W, padx=style['padx_level0'])
        return is_intermitted_test_var

    def widget_text_id(self, row, column):
        self.test_id_text = tk.StringVar()
        self.test_id = tk.Entry(self.root, textvariable=self.test_id_text, width=style['width_entry_level1'])
        self.test_id_text.set("00000000")
        self.test_id.grid(row=row, column=column + self.offset, sticky=tk.W, padx=style['padx_level1'])
        return

    def create_list_of_measurements(self, header_params):
        params = {}
        measurement_mode_keys = ['itl', 'ctl']
        params['measurement_mode'] = []
        params['n_measurements'] = []
        params['pixel_distance'] = []
        params['measurement_rate'] = []
        if self.is_ctl.get():
            params['measurement_mode'].append(measurement_mode_keys[1])
            try:
                params['n_measurements'].append(int(self.n_measurement_ctl.get()))
                params['pixel_distance'].append(
                    int(self.pixel_distance_ctl.get()[:self.pixel_distance_ctl.get().rfind('\u03BCm')]))
                params['measurement_rate'].append(int(
                    int(self.measurement_rate_ctl.get()[:self.measurement_rate_ctl.get().rfind('Hz')])))
            except TypeError:
                messagebox.showerror("Fehler", error_message('wrong_number_type'))
        # if self.is_itl.get():
        #     params['measurement_mode'].append(measurement_mode_keys[0])
        #     try:
        #         params['n_measurements'].append(int(self.n_measurement_itl.get()))
        #         params['pixel_distance'].append(
        #             int(self.pixel_distance_itl.get()[:self.pixel_distance_itl.get().rfind('\u03BCm')]))
        #         params['measurement_rate'].append(int(
        #             int(self.measurement_rate_itl.get()[:self.measurement_rate_itl.get().rfind('Hz')])))
        #     except TypeError:
        #         messagebox.showerror("Fehler", error_message('wrong_number_type'))

        list_of_tests = []
        if len(params['measurement_mode']) > 0:
            for i in range(len(params['measurement_mode'])):
                single_test_params = {}
                single_test_params['measurement_mode'] = params['measurement_mode'][i]
                single_test_params['n_measurements'] = params['n_measurements'][i]
                single_test_params['pixel_distance'] = params['pixel_distance'][i]
                single_test_params['measurement_rate'] = params['measurement_rate'][i]
                single_test_params.update(header_params)
                list_of_tests.append(self.get_params(single_test_params))

        return list_of_tests

    def get_params(self, params):
        try:
            params['test_id'] = int(self.test_id.get())

            if self.is_intermitted_test.get():
                params['segment_no'] = int(self.segment_no.get())
            else:
                params['segment_no'] = 0

            if params['measurement_mode'] == 'ctl':
                params['rim_surplus'] = float(self.rim_surplus_ctl.get().replace(',', '.'))
            elif params['measurement_mode'] == 'itl':
                params['rim_surplus'] = -float(self.rim_surplus_itl.get().replace(',', '.'))

            params['position_start'] = float(self.starting_position.get().replace(',', '.'))
            params['measurement_length'] = float(self.measurement_distance.get().replace(',', '.'))
        except:
            messagebox.showerror("Fehler", error_message('wrong_number_type'))

        params['sample_condition'] = self.sample_condition.get()
        sample_geometry_keys = ['pre', 'post', 'post-clean']
        for i, v in enumerate(self.sample_condition_options):
            if params['sample_condition'] == v:
                params['sample_condition'] = sample_geometry_keys[i]
        step_size = (1.8, 0.9, 0.45)
        if params['sample_geometry'] == 'Ring':
            params['gear_transmission'] = 1.0
            rot_steps = 200
            for i in range(len(step_size)):
                if rot_steps / params['n_measurements'] / step_size[i] <= 100:
                    params['step_transmission'] = i
                else:
                    params['step_transmission'] = i
        elif params['sample_geometry'] == 'Disk':
            params['gear_transmission'] = 1.8
            rot_steps = 360
            for i in range(len(step_size)):
                if rot_steps / params['n_measurements'] / step_size[i] <= 100:
                    params['step_transmission'] = i
                else:
                    params['step_transmission'] = i
        # print('get_params', params)
        return params

    def widget_segment_no(self, row, column):
        segment_text = tk.StringVar()
        segment_no = tk.Entry(self.root, textvariable=segment_text, width=style['width_entry_level1'],
                              state='disabled')
        segment_text.set("0000")
        segment_no.grid(row=row, column=column + self.offset, sticky=tk.W, padx=style['padx_level1'])
        return segment_no


class Application(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Begin GUI
        self.n_line_menus = 5
        self.init_general_widgets()

        self.add_labels()
        self.line_dict = []

        self.list_of_test_params = []
        for i in range(self.n_line_menus):
            self.line_dict.append(Line_menu(self.parent, i))
        self.add_control_buttons(self.n_line_menus)

    def init_general_widgets(self):
        self.sensor = self.widget_sensor(row=20, column=2)
        self.sample_geometry = self.widget_sample_geometry(row=30, column=2)

    def widget_sensor(self, row, column):
        sensor_options = ["0.3 mm", "3.0 mm"]
        sensor = ttk.Combobox(self.parent, values=sensor_options, state="readonly", width=style['width_cbox_level1'])
        sensor.set(sensor_options[0])
        sensor.grid(row=row, column=column, sticky=tk.W, padx=style['padx_level1'])
        return sensor

    def widget_sample_geometry(self, row, column):
        sample_geometry_options = ["Ring", "Disk"]
        sample_geometry = ttk.Combobox(self.parent, values=sample_geometry_options, state="readonly",
                                       width=style['width_cbox_level1'])
        sample_geometry.set(sample_geometry_options[0])
        sample_geometry.grid(row=row, column=column, sticky=tk.W, padx=style['padx_level1'])
        return sample_geometry

    def add_labels(self):
        self.parent.title("Automatic FRT-Measurement")
        authors = 'Bai Cheng Jim'

        # labels
        tk.Label(self.parent, text="FRT-Measurement", font=("Times", 24)).grid(row=0, column=0, columnspan=400)
        tk.Label(self.parent, text="Version: {}".format(version)).grid(row=10, column=0, columnspan=400)
        tk.Label(self.parent, text="Authors: {}".format(authors)).grid(row=11, column=0, columnspan=400)
        # if script.DEBUG:
        #     tk.Label(self.parent, text="DEBUG IS ON!!!", fg='darkred', font=('Courier', 40)).grid(row=15, column=1,
        #                                                                                           columnspan=3,
        #                                                                                           sticky=tk.E)
        tk.Label(self.parent, text="Sensor Type").grid(row=20, column=1, sticky=tk.E)
        tk.Label(self.parent, text="Specimen Geometry").grid(row=30, column=1, sticky=tk.E)
        tk.Label(self.parent, text="Test ID").grid(row=50, column=1, sticky=tk.E)
        tk.Label(self.parent, text="Intermittent Test?").grid(row=60, column=1, sticky=tk.E)
        tk.Label(self.parent, text="Segment No.").grid(row=70, column=1, sticky=tk.E)
        tk.Label(self.parent, text="Specimen State").grid(row=80, column=1, sticky=tk.E)
        tk.Label(self.parent, text="Track initial [mm]").grid(row=81, column=1, sticky=tk.E)
        tk.Label(self.parent, text="Track Width [mm]").grid(row=82, column=1, sticky=tk.E)

        # tk.Label(self.parent, text="Messung Rauheit", fg='blue').grid(row=83, column=1, sticky=tk.E)
        # tk.Label(self.parent, text="Toleranzabzug pro Seite [mm]", fg='blue').grid(row=84, column=1, sticky=tk.E)
        # tk.Label(self.parent, text="Anzahl Messungen", fg='blue').grid(row=85, column=1, sticky=tk.E)
        # tk.Label(self.parent, text="Pixelabstand", fg='blue').grid(row=87, column=1, sticky=tk.E)
        # tk.Label(self.parent, text="Messrate", fg='blue').grid(row=88, column=1, sticky=tk.E)

        tk.Label(self.parent, text="Scar Measurement", fg='darkred').grid(row=89, column=1, sticky=tk.E)
        tk.Label(self.parent, text="Track Excess per Side [mm]", fg='darkred').grid(row=90, column=1, sticky=tk.E)
        tk.Label(self.parent, text="# of Measurements", fg='darkred').grid(row=92, column=1, sticky=tk.E)
        tk.Label(self.parent, text="Pixel Distance", fg='darkred').grid(row=93, column=1, sticky=tk.E)
        tk.Label(self.parent, text="Measurement Rate", fg='darkred').grid(row=94, column=1, sticky=tk.E)

        tk.Label(self.parent, text="Backup Folder").grid(row=125, column=1, sticky=tk.E)
        tk.Label(self.parent, text="DB URL").grid(row=135, column=1, sticky=tk.E)
        tk.Label(self.parent, text="Send to AtlasDB").grid(row=140, column=1, sticky=tk.E)
        tk.Label(self.parent, text="Autofocus").grid(row=150, column=1, sticky=tk.E)

        # static widgets
        self.widget_backup_url(row=125, column=2)
        self.widget_db_url(row=135, column=2)

        self.is_send2atlas = self.widget_is_send2atlas(row=140, column=2)
        self.is_autofocus = self.widget_is_autofocus(row=150, column=2)

    def widget_db_url(self, row, column):
        db_url_var = tk.StringVar()
        db_url = tk.Entry(self.parent, textvariable=db_url_var,
                          width=style['width_entry_level1'] + (self.n_line_menus - 1) * style['width_entry_level1'] + (
                                  self.n_line_menus - 1) * 5, state='disabled')
        db_url_var.set(script.params['db_url'])
        db_url.grid(row=row, column=column, sticky=tk.W, padx=style['padx_level1'], columnspan=400)

    def widget_backup_url(self, row, column):
        backup_url_var = tk.StringVar()
        backup_url = tk.Entry(self.parent, textvariable=backup_url_var,
                              width=style['width_entry_level1'] + (self.n_line_menus - 1) * style[
                                  'width_entry_level1'] + (
                                            self.n_line_menus - 1) * 5, state='disabled')
        backup_url_var.set(script.params['backup_url'])
        backup_url.grid(row=row, column=column, sticky=tk.W, padx=style['padx_level1'], columnspan=400)

    def widget_is_send2atlas(self, row, column):
        is_send2atlas_var = tk.BooleanVar(value=1)
        is_send2atlas = tk.Checkbutton(self.parent, variable=is_send2atlas_var)
        is_send2atlas.grid(row=row, column=column, sticky=tk.W, padx=style['padx_level0'])
        is_send2atlas['state'] = 'disabled'
        return is_send2atlas_var

    def widget_is_autofocus(self, row, column):
        is_autofocus_var = tk.BooleanVar(value=0)
        is_autofocus = tk.Checkbutton(self.parent, variable=is_autofocus_var)
        is_autofocus.grid(row=row, column=column, sticky=tk.W, padx=style['padx_level0'])
        return is_autofocus_var

        # def widget_n_line_menus(self, row, column):
        #     n_line_menus_options = ['1', '2']
        #     n_line_menus = ttk.Combobox(self.parent, values=n_line_menus_options, state="readonly",
        #                                 width=style['width_cbox_level1'])
        #     n_line_menus.set(n_line_menus_options[0])
        #     n_line_menus.grid(row=row, column=column, sticky=tk.W, padx=style['padx_level1'])
        #     n_line_menus.bind("<<ComboboxSelected>>", self.get_n_line_menus)
        #     return n_line_menus

        pass

    def get_n_line_menus(self):
        self.n_line_menus = self.n_line_menus.get()
        pass

    def add_control_buttons(self, n_lines):
        # control buttons
        button_measure = tk.Button(self.parent, text=("Start Measurement"), command=self.start_measurement)#, bg='green')
        button_measure.grid(row=200, column=2 + n_lines - 1, pady=10)

        button_quit = tk.Button(self.parent, text=("            Quit            "), command=self.quit_application)#, bg='red')
        button_quit.grid(row=200, column=0 + n_lines, pady=10)

    def get_header_params(self):
        params = {}
        params['sample_geometry'] = self.sample_geometry.get()
        params['sensor_type'] = self.sensor.get()
        params['sample_geometry'] = self.sample_geometry.get()
        return params

    def start_measurement(self):
        header_params = self.get_header_params()

        list_of_tests = []
        test_ids = []
        counter = 0
        for i in range(self.n_line_menus):
            if self.line_dict[i].is_conduct_line_measurement.get():
                list_of_tests.extend(self.line_dict[i].create_list_of_measurements(header_params))
                test_ids.append(list_of_tests[-1]['test_id'])
                counter += 1

        if np.unique(test_ids).size == counter:
            process_list = []
            for test in list_of_tests:
                params = script.params
                # params['rim'] = test['rim_surplus']
                params['send_to_db'] = self.is_send2atlas.get()
                params['set_autofocus'] = self.is_autofocus.get()
                params['backup_url'] = script.params['backup_url']
                # test = {**test, **params}
                test.update(params)
                test = script.compute_additional_params(test)
                process_list.append(test)
        else:
            messagebox.showerror("Fehler", error_message('identical_test_ids'))
            return

        for curr_test in process_list:
            status_code_test_exist = db_request.check_test_id_exist(curr_test['test_id'])
            if not status_code_test_exist:
                messagebox.showerror("Fehler", error_message('test_id_does_not_exist', curr_test['test_id']))
                return

        for curr_test in process_list:
            filename = '{}.zip'.format(curr_test['filename'])
            status_code_file_exist = db_request.check_scan_exists(filename)
            if status_code_file_exist:
                proceed = callback_continue(curr_test['filename'])
                if not proceed:
                    return

        for curr_test in process_list:
            script.process_measurement(curr_test)

        messagebox.showinfo(title='Measurement finished', message='Measurement finished')

        list_zips = [f for f in os.listdir('.') if f.endswith('zip')]

        if script.DEBUG:
            print(list_of_tests)
            print(len(list_of_tests))
            # print(params_setup)
            pass

    def quit_application(self):
        script.motor_disconnect()
        self.parent.destroy()
        return


if __name__ == '__main__':
    style = define_style()
    root = tk.Tk()
    app = Application(root)
    app.grid()
    root.mainloop()
    print()
