import file_handler, logging
from os.path import join
from re import sub

logger = logging.getLogger('ccl_data')


r'''
ccl_loads -> loads from selected method (ccl, csv)
    automatic get type
        load all values


'''


template = {
    "templates" : {
        "Info" : {
                "FileType" : "CCL100 Marking Layout File", 
                "Version" : "1.0"
            }
        ,
        "Count" : {
                "Number" : 9
            }
        ,
        "FileParams" : {
            "rotation" : 0.00000, 
            "xoffset" : 0.00000, 
            "yoffset" : 0.00000, 
            "mirrored" : 0, 
            "flipped" : 0
            }
        ,
        "CircleL" : {
            "char" : 0, 
            "enabled" : 0, 
            "font" : 20, 
            "pen" : 1, 
            "height" : 1.500000, 
            "width" : 1.500000, 
            "x" : 17.00000, 
            "y" : 0.00000, 
            "rotation" : 0.00000, 
            "orientation" : 5, 
            "flipping" : 0, 
            "decimalsign" : 1, 
            "digits" : 2, 
            "type" : 6, 
            "name" : "CircleL"
            }
        ,
        "CircleR" : {
            "char" : 0,
            "enabled" : 0, 
            "font" : 20, 
            "pen" : 1, 
            "height" : 1.500000, 
            "width" : 1.500000, 
            "x" : 17.00000, 
            "y" : 0.00000, 
            "rotation" : 0.00000, 
            "orientation" : 5, 
            "flipping" : 0, 
            "decimalsign" : 1, 
            "digits" : 2, 
            "type" : 6, 
            "name" : "CircleR"
            }
        ,
        "Logo" : {
            "char" : 0, 
            "enabled" : 0, 
            "font" : 32, 
            "pen" : 2, 
            "height" : 2.00000, 
            "width" : 2.500000, 
            "x" : 17.00000, 
            "y" : -6.00000, 
            "rotation" : 0.00000, 
            "orientation" : 5, 
            "mirrorin" : 1, 
            "flipping" : 0, 
            "decimalsign" : 1, 
            "digits" : 2, 
            "type" : 6, 
            "name" : "Logo"
            }
        
    },
    "Text" : {
        "text" : "",
        "enabled" : 0,
        "font" : 10,
        "pen" : 3,
        "height" : 1.500000,
        "width" : 1.500000,
        "x" : 0.000000,
        "y" : 0.000000,
        "rotation" : 0.000000,
        "orientation" : 5,
        "mirroring" : 0,
        "flipping" : 0,
        "decimalsign" : 0,
        "digits" : 2,
        "type" : 6,
        "name" : ""
    }
}


def dict_compare_filler(dict_base, dict_compare):
    temp_dict = {}
    counter = 0
    for key in dict_base.keys():
        if key not in dict_compare.keys():
            temp_dict[key] = dict_base[key]
            counter = counter +1
        else:
            temp_dict[key] = dict_compare[key]
    if counter:
        return temp_dict


def ccl_organizer(ccl_file_contents):
    ccl_organized = {}
    counter = 0
    values_group = {}
    for line in ccl_file_contents:
        line = line.replace('\n', '')
        if line.startswith('[') and line.endswith(']'):
            if not counter == 0:
                counter = 0
                ccl_organized[header] = values_group
                values_group = {}
            header = line.replace('[', '').replace(']', '')
        else:
            values_splitted = line.split('=')
            values_group[values_splitted[0]] = values_splitted[1]
            counter = counter + 1
    ccl_organized[header] = values_group
    return ccl_organized


def ccl_filler(ccl_organized, templates):
    for key in templates['templates'].keys():
        if key not in ccl_organized.keys():
            ccl_organized[key] = templates['templates'][key]
        else:
            temp_dict = dict_compare_filler(templates['templates'][key], ccl_organized[key])
            if temp_dict:
                ccl_organized[key] = temp_dict
    for key_name in ccl_organized.keys():
        if 'Text' in key_name:
            last_digit = int(key_name.replace('Text', ''))
            temp_dict = dict_compare_filler(templates['Text'], ccl_organized[key_name])
            if temp_dict:
                ccl_organized[key_name] = temp_dict
            counter = last_digit + 1
    while counter <= 12:
        field_values_filler = {}
        for key_value in templates['Text']:
            if key_value == 'name':
                field_values_filler['name'] = f'text{counter}'
            else:
                field_values_filler[key_value] = templates['Text'][key_value]
        ccl_organized[f'Text{counter}'] = field_values_filler
        counter = counter + 1
    return ccl_organized


def ccl_loads(path: str, extension: str, template: dict=template):
    try:
        file_list = file_handler.file_list(path, extension)
        ccl_marking_files = {}
        list_side_R = {}
        list_side_L = {}     
        list_no_side = {}
        if len(file_list) > 0:
            for file in file_list:
                full_path = join(path, file)     
                file_contents = file_handler.file_reader(full_path)
                ccl_contents = ccl_organizer(file_contents)
                ccl_contents_filled = ccl_filler(ccl_contents, template)
                file_name = file.replace('.ccl', '')
                ccl_dict = {}
                ccl_dict['File_Name'] = file_name
                ccl_dict.update(ccl_contents_filled)
                name_no_side = sub('R$|_R$|L$|_L$', '', file_name)
                marking_file = ccl_marking_files.get(name_no_side, '')
                if marking_file:






                file_side = file.replace('.ccl', '')[-1]
                match file_side:
                    case 'R':
                        list_side_R[file_name] = ccl_dict
                    case 'L':
                        list_side_L[file_name] = ccl_dict
                    case _:
                        list_no_side[file_name] = ccl_dict
            name_list = __create_dict_ccl(list_side_R, list_side_L, list_no_side)
            ccl_values = {}
            for name in name_list:
                temp_dict = {}
                if f'{name}_R' in list_side_R:
                    temp_dict[f'{name}_R'] = list_side_R[f'{name}_R']
                if f'{name}_L' in list_side_L:
                    temp_dict[f'{name}_L'] = list_side_L[f'{name}_L']
                if name in list_no_side:
                    temp_dict['No_Side'] = list_no_side[name]
                ccl_values[name] = temp_dict
            return ccl_values
    except Exception as error:
        logger.error(error)


def __create_dict_ccl(list_side_R: dict, list_side_L: dict, list_no_side: dict) -> dict:
    list_R = [sub('R$|_R$', '', file_name) for file_name in list_side_R.keys()]
    list_L = [sub('L$|_L$', '', file_name) for file_name in list_side_L.keys()]
    list_N = [file_name for file_name in list_no_side.keys()]
    return set(list_R + list_L + list_N)


if __name__ == '__main__':
    path = r'C:\Users\fausto.akio\Desktop\MarkingFiles'
    extension = 'ccl'

    ccl_loads(path, extension)