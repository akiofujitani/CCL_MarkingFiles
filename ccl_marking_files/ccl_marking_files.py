import logging, log_builder, tkinter, json_config, file_handler
from tkinter import messagebox
from gui_builder import About
from classes import ConfigurationValues
from PIL import ImageDraw, Image, ImageTk
from queue import Queue

logger = logging.getLogger('ccl_marking_files')


'''
==========================================================================================

Configuration Template

==========================================================================================
'''

config_template = '''{
    "ccl_path" : "./",
    "ccl_extension" : "ccl",
    "hpf_path" : "./",
    "hpf_extension" : "hpf",
    "sheets_id" : "",
    "sheets_name" : "",
    "sheets_pos" : "",
    "list_geometry" : {
        "main" : ["", "", 0, 0],
        "settings" : ["", "", 0, 0],
        "edit" : ["", "", 0, 0],
        "about" : ["", "", 0, 0]
    }
}
'''

'''
==========================================================================================



==========================================================================================
'''

r'''
Structure

Main_app
    |
    |____ Settings
    |
    |
    |____ About 
    |
    |
    |______GUI
            |_____ Treeview > List of all marking files
            |                       |
            |                       |____ Load from sheets, ccl files in directory or csv             
            |
            |______________CCL Vizualizer
                                |
                                |_________Load values from marking file
                                |
                                |_________Load hpf files for logo and characters
                                |
                                |_________Combine values into image (ImageDraw)
            

'''

'''
==========================================================================================

        GUI     GUI     GUI     GUI     GUI     GUI     GUI     GUI     GUI     GUI     

==========================================================================================
'''


class MainApp(tkinter.Tk):
    def __init__(self, title: str, log_queue: Queue, config: ConfigurationValues, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title(title)
        self.configuration_values = config
        self.log_queue = log_queue
        self.minsize(600, 400)
        # Get and set geometry
        win_pos = self.configuration_values.check_win_pos('main')
        if win_pos:
            self.geometry(win_pos)

        # Icon load, path hard coded but...
        try:
            self.icon_path = file_handler.resource_path('./Icon/walrus.png')
            icon = Image.open(self.icon_path)
            icon.resize((96, 96), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(icon)
            self.wm_iconphoto(True, photo)
        except Exception as error:
            logger.error(f'Could not load icon {error}')        

        # Configure grid columns weight (follow resize)
        self.grid_columnconfigure(0, weight=1, minsize=200)
        self.grid_columnconfigure(2, weight=1, minsize=100)
        self.grid_rowconfigure(0, weight=1)

        # Menu bar creation
        menu_bar = tkinter.Menu(self)
        file_menu = tkinter.Menu(menu_bar, tearoff=0)
        help_menu = tkinter.Menu(menu_bar, tearoff=0)
        edit_menu = tkinter.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label='Load   ', command=self.__load)
        file_menu.add_command(label='Exit   ', command=self.__quit_window)
        edit_menu.add_command(label='Settings ', command=self.__settings)
        help_menu.add_command(label='About     ', command=self.__about_command)
        menu_bar.add_cascade(label='File   ', menu=file_menu)
        menu_bar.add_cascade(label='Edit   ', menu=edit_menu)
        menu_bar.add_cascade(label='Help   ', menu=help_menu)
        self.config(menu=menu_bar)

        # 

    def __load(self):
        logger.debug('Load pressed')
        pass


    def __settings(self):
        logger.debug('Settings pressed')
        pass



    def __about_command(self):
        logger.info('About clicked')
        self.about = About(self, True,
            'About', '''
            Application name: Directory Monitor
            Version: 0.10.00
            Developed by: Akio Fujitani
            e-mail: akiofujitani@gmail.com
        ''', file_handler.resource_path('./Icon/Bedo.jpg'))     


    def __quit_window(self):
        if messagebox.askokcancel('Quit', 'Do you want to quit?'):
            self.configuration_values.update_win_size_pos(self.geometry(), 'main')
            self.configuration_values.save_config_on_change()
            logger.info('Closing app')
            self.after(150, self.deiconify)
            self.destroy()


if __name__ == '__main__':
    log_queue = Queue()
    logger = logging.getLogger()
    log_builder.logger_setup(log_queue)

    try:
        config_dict = json_config.load_json_config('config.json', config_template)
        config = ConfigurationValues.check_type_insertion(config_dict)
    except Exception as error:
        logger.critical(f'Configuration error {error}')
        exit()


    main_app = MainApp('CCL Marking File Viewer', log_queue, config)
    main_app.mainloop()