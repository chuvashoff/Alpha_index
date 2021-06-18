import datetime
import os
import re
from string import Template

print(datetime.datetime.now())

'''Считываем шаблоны для карты'''
with open(os.path.join(os.path.dirname(__file__), 'Template', 'Temp_map_index_Arc'), 'r', encoding='UTF-8') as f:
    tmp_ind_Arc = f.read()
with open(os.path.join(os.path.dirname(__file__), 'Template', 'Temp_map_index_noArc'), 'r', encoding='UTF-8') as f:
    tmp_ind_noArc = f.read()


lst_ai = [
    'coSim', 'coRepair', 'coUpdRepair', 'Message.msg_fBreak', 'Message.msg_qbiValue', 'Value', 'fValue', 'iValue',
    'qbiValue', 'sChlType', 'sEnRepair', 'TRepair', 'Value100', 'aH', 'aL', 'fParam', 'fOverlow', 'fOverhigh',
    'fHighspeed', 'Repair', 'Sim', 'wH', 'wL', 'sEnaH', 'sBndaH', 'sEnaL', 'sBndaL', 'sEnwH', 'sBndwH', 'sEnwL',
    'sBndwL', 'sEnRate', 'sBndRate', 'sHighLim', 'sHys', 'sLowLim', 'sSimValue', 'sTaH', 'sTaL', 'sTRepair', 'sTwH',
    'sTwL', 'sHighiValue', 'sLowiValue'
]
sl_type = {
    'R': 'Analog',
    'I': 'Analog',
    'B': 'Bool'
}
sl_dataCat = {
    'R': 'Analog',
    'I': 'Analog',
    'B': 'Discrete'
}

with open('Source_list', 'r') as f:
    while 8:
        line_source = f.readline().strip().split(',')
        if line_source == ['']:
            break
        sl_global_ai = {}
        sl_global_fast = {}
        s_ai = ''
        '''Если есть файл аналогов'''
        if os.path.isfile(os.path.join(line_source[1], '0_par_A.st')):
            sl_tmp_ai = {}
            with open(os.path.join(line_source[1], '0_par_A.st')) as f_par_a:
                text = f_par_a.read().split('\n')
            for i in text:
                if 'AI_' in i:
                    if ' ' in i:
                        sl_tmp_ai[i[:i.find(' ')]] = int(i[i.rfind('[')+1:i.rfind(']')])
                    else:
                        sl_tmp_ai[i[:i.find('(')]] = int(i[i.rfind('(')+1:i.rfind(')')])
            sl_tmp_ai = {key: value for key, value in sl_tmp_ai.items() if f'FAST|{key}' not in sl_tmp_ai}
            '''В словаре sl_tmp_ai лежит индекс массива: алг имя (в том числе FAST|+)'''
            sl_tmp_ai = {value: key for key, value in sl_tmp_ai.items()}

        '''Если есть глобальный словарь'''
        if os.path.isfile(os.path.join(line_source[1], 'global0.var')):
            with open(os.path.join(line_source[1], 'global0.var')) as f_global:
                while 8:
                    line = f_global.readline().strip()
                    if not line:
                        break
                    if 'A_INP|' in line and len(line.split(',')) >= 10:
                        line = line.split(',')
                        if 'msg' not in line[0]:
                            sl_global_ai[line[0][line[0].find('|')+1:]] = [max(int(line[9]), int(line[10])), line[1]]
                        else:
                            sl_global_ai['Message.' + line[0][line[0].find('|') + 1:]] = [max(int(line[9]),
                                                                                              int(line[10])), line[1]]
                    if 'FAST|' in line:
                        line = line.split(',')
                        '''В словаре sl_global_fast лежит  алг имя(FAST|): индекс переменной'''
                        sl_global_fast[line[0][1:]] = max(int(line[9]), int(line[10]))
        '''В словаре sl_global_ai лежит подимя[индекс массива]: [индекс переменной, тип переменной(I, B, R)]'''
        sl_global_ai = {key: value for key, value in sl_global_ai.items() if key[:key.find('[')] in lst_ai}

        '''Обработка и запись в карту аналогов'''
        for key, value in sl_global_ai.items():
            tmp_i = int(key[key.find('[')+1:key.find(']')])
            tmp_subName = key[:key.find('[')]
            if 'FAST|' in sl_tmp_ai[tmp_i] and re.fullmatch(r'Value', key[:key.find('[')]):
                value[0] = sl_global_fast[sl_tmp_ai[tmp_i]]
                a = sl_tmp_ai[tmp_i][sl_tmp_ai[tmp_i].find('|')+1:]
                temp = tmp_ind_Arc
            else:
                a = sl_tmp_ai[tmp_i][sl_tmp_ai[tmp_i].find('|') + 1:]
                temp = tmp_ind_noArc
            s_ai += Template(temp).substitute(name_signal=f'AI.{a}.{tmp_subName}',
                                              type_signal=sl_type[value[1]], index=value[0],
                                              data_category=f'DataCategory_{line_source[0]}_NoArc{sl_dataCat[value[1]]}'
                                              )

        with open(f'trei_map_{line_source[0]}.xml', 'w') as f_out:
            f_out.write('<root format-version=\"0\">\n' + s_ai.rstrip() + '\n</root>')



'''
for key, value in sl_global_ai.items():
    print(key, value)
'''

# print(s_ai)
print(datetime.datetime.now())
