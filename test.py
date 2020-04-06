# j = '111, 555, 222, 5532'
#
# print(j.split(','))


# j = 'project_6delete'
# j = j[len('project_'):]
#
# print(j[:-len('delete')])

# l = '223, saf'
# user_list = l.split(',')
# for data in user_list:
#     if data.isdigit():
#         print('ok')
# import sys
# ADD_TEMPLATE = {}
# ADD_TEMPLATE[1111111] = {}
# ADD_TEMPLATE[1111111]['id'] = 1111111
# ADD_TEMPLATE[1111111]['weekdays'] = ['']
# ADD_TEMPLATE[1111111]['status_weekdays'] = []
# ADD_TEMPLATE[1111111]['time'] = []
# ADD_TEMPLATE[1111111]['time_to_answer'] = []
# ADD_TEMPLATE[1111111]['text'] = []
# ADD_TEMPLATE[1111111]['project'] = []
# ADD_TEMPLATE[1111111]['inline_temp'] = []
# ADD_TEMPLATE[1111111]['change_project'] = []
#
#
# print(sys.getsizeof(ADD_TEMPLATE))


data = 'confirm_markup_6_yes__template'
print(data[len('confirm_markup_'):data.find('_yes_')])