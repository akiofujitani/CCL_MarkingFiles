from ntpath import join
from time import sleep
import FileHandler, DataOrganizer, config, os


def convert_to_csv(ccl_templates=dict, path=str, path_output=str) :
    
    file_list = FileHandler.fileList(path, 'ccl')
    list_side_R = []
    list_side_L = []
    list_no_side = []
    
    for file in file_list:
        full_path = join(path, file)
        file_contents = FileHandler.file_reader(full_path)
        ccl_contents = DataOrganizer.ccl_organizer(file_contents)
        ccl_contents_filled = DataOrganizer.ccl_filler(ccl_contents, ccl_templates)
        plain_dict = {}
        plain_dict['File_Name'] = file.replace('.ccl', '')
        plain_dict.update(DataOrganizer.ccl_organized_to_plain_dict(ccl_contents_filled))
        file_side = file.replace('.ccl', '')[-1]
        match file_side:
            case 'R':
                list_side_R.append(plain_dict)
            case 'L':
                list_side_L.append(plain_dict)
            case _:
                list_no_side.append(plain_dict)

    FileHandler.listToCSV(DataOrganizer.plain_dict_float_format(list_side_R), join(path_output, 'ccl_side_R.csv'))
    FileHandler.listToCSV(DataOrganizer.plain_dict_float_format(list_side_L), join(path_output, 'ccl_side_L.csv'))
    if len(list_no_side) > 0:
        FileHandler.listToCSV(DataOrganizer.plain_dict_float_format(list_no_side), join(path_output, 'ccl_no_side.csv'))


def convert_to_ccl(csv_path=str, ccl_path=str):
    csv_list = FileHandler.fileList(csv_path, 'csv')

    for csv_file in csv_list:
        file_data = FileHandler.CSVtoList(join(csv_path, csv_file), False, ',')
        for file in file_data:
            ccl_organized = DataOrganizer.simple_dict_to_ccl_organized(file)
            ccl_organized.pop('File')
            print('done')
            ccl_in_string  = DataOrganizer.ccl_organized_to_string(ccl_organized)
            FileHandler.file_writer(join(ccl_path, f'{file["File_Name"]}.ccl'), ccl_in_string)    
        print('done')


def path_input_validation(message=str):
    print(message)
    path = ''
    while not path:
        path = input()
        if not os.path.exists(path):
            print('Path not valid, try again.')
            path = ''
    return path



if __name__ == '__main__':
    ccl_templates = config.load_json_config()
    while True:
        print('Press [1] to convert ccl files to csv')
        print('Press [2] to convert csv files to ccl')
        print('Press [3] to exit')
        print('and press "Enter" to confirm.')
        print('Enter value ', end='')
        value = input()
        if value == '1' or value == '2' or value == '3':
            break
        else:
            print('Invalid input, try again...')

    match value:
        case '1':
            path = path_input_validation('Insert marking files path:')
            print('')
            path_output = path_input_validation('Insert csv files output path')
            convert_to_csv(ccl_templates, path, path_output)
            print('')
            print('Done')
            sleep(3)
        case '2':
            csv_path = path_input_validation('Insert csv files path:')
            print('')
            ccl_path = path_input_validation('Insert ccl output files path:')
            convert_to_ccl(csv_path, ccl_path)
            print('')
            print('Done')
        case '3':
            print('Script ended.')
            exit()
