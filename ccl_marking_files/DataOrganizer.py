

def filter_list_values(data_list, *values_list):
    filtered_list = []
    for data in data_list:
        filtered_dict = {}
        for value in values_list:
            value_upper = value.upper()
            if value_upper in data.keys():
                filtered_dict[value_upper] = data[value_upper]
        filtered_list.append(filtered_dict)
    return filtered_list


def filter_column_values(data_list, column_name, filter_values):
    filter_values = [values.upper() for values in filter_values]
    filtered_list = []
    for data in data_list:
        if data[column_name.upper()].upper() in filter_values:
            filtered_list.append(data)
    return filtered_list


def filter_tag(job_data, *args):
    '''
    filter tags based on tag's list
    '''
    
    filtered_data = {}
    filtered_data['JOB'] = job_data['JOB']
    for arg in args:
        if arg in job_data.keys():
            filtered_data[arg] = job_data[arg]
    return filtered_data


def checkData(tag, convertedData):
    '''
    Check number of values inside TAG
    '''

    countOne = 0
    countTwo = 0
    for line in convertedData:
        if tag in line.keys():
            match len(line[tag]):
                case 1:
                    countOne += 1
                case 2:
                    countTwo += 1
    print(f'{tag} checked')
    return 2 if countTwo > countOne else 1


def isFloat(number):
    '''
    Check if values if float compatible
    '''
    try:
        float(number)
        return True
    except ValueError:
        return False


def isInt(number):
    '''
    Check if values if float compatible
    '''
    try:
        int(number)
        return True
    except ValueError:
        return False


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



def fields_values_template():
    template = '''
text=
enabled=0
font=10
pen=3
height=1.500000
width=1.500000
x=0.000000
y=0.000000
rotation=0.000000
orientation=5
mirroring=0
flipping=0
decimalsign=0
digits=2
type=6
name=
'''
    field_values = {}
    for line in template.split('\n'):
        if len(line) > 0:
            value_splited = line.split('=')
            field_values[value_splited[0]] = value_splited[1]
    return field_values


def ccl_organized_to_plain_dict(ccl_organized):
    plain_dict = {}
    for key_name in ccl_organized.keys():
        for key in ccl_organized[key_name]:
            plain_dict[f'{key_name}_{key}'] = ccl_organized[key_name][key]
            print(f'{key_name}_{key} = {ccl_organized[key_name][key]}')
    return plain_dict


def simple_dict_to_ccl_organized(simple_dict):
    ccl_organized = {}
    fields_value = {}
    key = ''
    for key_name in simple_dict.keys():
        splited_key = key_name.split('_')
        if not key == splited_key[0] and key != '':
            ccl_organized[key] = fields_value
            fields_value = {}  
        fields_value[splited_key[1]] = simple_dict[key_name].replace(',', '.')          
        key = splited_key[0]  
        print(f'{splited_key[0]} {splited_key[1]} {simple_dict[key_name]}')
    ccl_organized[key] = fields_value
    return ccl_organized


def ccl_organized_to_string(ccl_organized):
    string_values = ''
    for key in ccl_organized.keys():
        string_values = string_values + f'[{key}]\n'
        for value_key in ccl_organized[key].keys():
            string_values = string_values + f'{value_key}={ccl_organized[key][value_key]}\n'
    return string_values


def plain_dict_float_format(plain_dict):
    float_updated_plain_dict = []    
    for line in plain_dict:
        temp_dict = {}
        for key in line.keys():
            temp_dict[key] = str(line[key]).replace('.',',') if isFloat(line[key]) else line[key]
        float_updated_plain_dict.append(temp_dict)
        print('Float values converted')
    return float_updated_plain_dict

