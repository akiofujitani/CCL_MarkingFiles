import logging, json_config
from copy import deepcopy
from dataclasses import dataclass
from os.path import normpath
from collections import namedtuple


logger = logging.getLogger()


TtkGeometry = namedtuple('TtkGeometry', 'width, height, x, y')


@dataclass
class PathDetails:
    r'''
    Path details with path, file extension, and ignore pattern
    '''
    name : str
    path: str
    extension: str
    ignore: str


    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        else:
            self_values = self.__dict__
            for key in self_values.keys():
                if not getattr(self, key) == getattr(other, key):
                    return False
            return True
    

    @classmethod
    def check_type_insertion(cls, config_values: dict):
        try:
            name = config_values['name']
            path =  normpath(config_values['path'])
            extension = config_values['extension']
            ignore = config_values['ignore']
            return cls(name, path, extension, ignore)
        except Exception as error:
            raise error


@dataclass
class ConfigurationValues:
    r'''
    Configuration 
    -------------

    '''
    ccl_path : str
    ccl_extension : str
    hpf_path: str
    hpf_extension: str
    sheets_id : str
    sheets_name : str
    sheets_pos: str
    list_geometry : list


    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        else:
            self_values = self.__dict__
            for key in self_values.keys():
                if not getattr(self, key) == getattr(other, key):
                    return False
            return True


    def to_dict(self):
        values_dict = self.__dict__
        values_dict['list_geometry'] = {name : [*value] for name, value in values_dict['list_geometry'].items()}
        return values_dict


    def get_path_details(self, name: str) -> PathDetails:
        for path_value in self.path_list:
            if path_value.name == name:
                return path_value
        return None


    def check_win_pos(self, window_name: str) -> str:
        r'''
        Receives the window name and check its geometry
        If true return the geometry values
        '''
        if window_name not in self.list_geometry.keys():
            return
        win_pos = self.list_geometry[window_name]
        if win_pos.width and win_pos.height:
            geometry_values = f'{win_pos.width}x{win_pos.height}+{win_pos.x}+{win_pos.y}'
            logger.debug(geometry_values)
            return geometry_values        


    def save_config_on_change(self):
        r'''
        Save to configuration file if it has changes
        '''
        try:
            config_value = json_config.load_json_config('config.json')
            old_config = ConfigurationValues.check_type_insertion(config_value)
            if not self.__eq__(old_config):
                temp_config = deepcopy(self)
                json_config.save_json_config('config.json', temp_config.to_dict())
        except Exception as error:
            logger.error(f'Could not save configuration values {error}')  


    def update_win_size_pos(self, geometry_str:str, window_name: str):
        r'''
        Update window size and position in config object
        '''
        temp_splited_geometry = geometry_str.split('+')
        win_size = temp_splited_geometry[0].split('x')
        win_pos = [temp_splited_geometry[1], temp_splited_geometry[2]]
        main_pos = self.list_geometry[window_name]
        if not win_size[0] == main_pos.width or not win_size[1] == main_pos.height or not win_pos[0] == main_pos.x or not win_pos[1] == main_pos.y:
            logger.debug(f'{win_size[0]} x {win_size[1]} + {win_pos[0]} + {win_pos[1]}')
            main_pos = TtkGeometry(win_size[0], win_size[1], win_pos[0], win_pos[1])
            self.list_geometry[window_name] = main_pos
        return


    @classmethod
    def check_type_insertion(cls, config_values: dict):
        try:
            ccl_path = config_values['ccl_path']
            ccl_extension = config_values['ccl_extension']
            hpf_path = config_values['hpf_path']
            hpf_extension = config_values['hpf_extension']
            sheets_id = config_values['sheets_id']
            sheets_name = config_values['sheets_name']
            sheets_pos = config_values['sheets_pos']
            list_geometry = {name : TtkGeometry(*value) for name, value in config_values['list_geometry'].items()}
            return cls(ccl_path, ccl_extension, hpf_path, hpf_extension, sheets_id, sheets_name, sheets_pos, list_geometry)
        except Exception as error:
            raise error



