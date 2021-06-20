import datetime
import os
import re
import logging
from string import Template


def create_sl(text, str_check):
    sl_tmp = {}
    for i in text:
        if str_check in i and '//' not in i:
            if 'FAST|' in i:
                sl_tmp[i[:i.find(' ')]] = int(i[i.rfind('[') + 1:i.rfind(']')])
            else:
                sl_tmp[i[:i.find('(')]] = int(i[i.rfind('(') + 1:i.rfind(')')])

    sl_tmp = {key: value for key, value in sl_tmp.items() if f'FAST|{key}' not in sl_tmp}
    '''В словаре sl_tmp лежит индекс массива: алг имя (в том числе FAST|+)'''
    sl_tmp = {value: key for key, value in sl_tmp.items()}
    return sl_tmp


def create_sl_im(text):
    sl_tmp = {}
    for i in text:
        if 'IM|' in i and '//' not in i and '[' in i:
            a = i.split(':=')[0].strip()
            sl_tmp[int(i[i.rfind('[') + 1:i.rfind(']')])] = a[a.find('|')+1:a.rfind('_')]
    '''В словаре sl_tmp лежит индекс массива: алг имя'''
    return sl_tmp


def create_group_par(sl_global_par, sl_local_par, sl_global_fast, template_arc_index, template_no_arc_index,
                     pref_par, source):
    sl_data_cat = {
        'R': 'Analog',
        'I': 'Analog',
        'B': 'Discrete'
    }
    sl_type = {
        'R': 'Analog',
        'I': 'Analog',
        'B': 'Bool'
    }
    s_out = ''
    for key, value in sl_global_par.items():
        tmp_i = int(key[key.find('[')+1:key.find(']')])
        tmp_sub_name = key[:key.find('[')]
        if tmp_i not in sl_local_par:
            continue
        if 'FAST|' in sl_local_par[tmp_i] and re.fullmatch(r'Value', key[:key.find('[')]):
            value[0] = sl_global_fast[sl_local_par[tmp_i]]
            a = sl_local_par[tmp_i][sl_local_par[tmp_i].find('|')+1:]
            temp = template_arc_index
            pref_arc = 'Arc'
        else:
            a = sl_local_par[tmp_i][sl_local_par[tmp_i].find('|')+1:]
            temp = template_no_arc_index
            pref_arc = f'NoArc{sl_data_cat[value[1]]}'
        s_out += Template(temp).substitute(name_signal=f'{pref_par}.{a}.{tmp_sub_name}', type_signal=sl_type[value[1]],
                                           index=value[0], data_category=f'DataCategory_{source}_{pref_arc}')
    return s_out


def create_group_im(sl_global_im, sl_local_im, sl_global_fast, template_arc_index, template_no_arc_index, source):
    sl_data_cat = {
        'R': 'Analog',
        'I': 'Analog',
        'B': 'Discrete'
    }
    sl_type = {
        'R': 'Analog',
        'I': 'Analog',
        'B': 'Bool'
    }
    s_out = ''
    for key, value in sl_global_im.items():
        tmp_i = int(key[key.find('[') + 1:key.find(']')])
        tmp_sub_name = key[:key.find('[')]
        if tmp_i not in sl_local_im:
            continue
        if f'FAST|IM_{sl_local_im[tmp_i]}_{tmp_sub_name}' in sl_global_fast:
            value[0] = sl_global_fast[f'FAST|IM_{sl_local_im[tmp_i]}_{tmp_sub_name}']
            a = sl_local_im[tmp_i]
            temp = template_arc_index
            pref_arc = 'Arc'
        else:
            a = sl_local_im[tmp_i]
            temp = template_no_arc_index
            pref_arc = f'NoArc{sl_data_cat[value[1]]}'
        s_out += Template(temp).substitute(name_signal=f'IM.{a}.{tmp_sub_name}', type_signal=sl_type[value[1]],
                                           index=value[0], data_category=f'DataCategory_{source}_{pref_arc}')
    return s_out


def create_index():
    # Считываем шаблоны для карты
    with open(os.path.join(os.path.dirname(__file__), 'Template', 'Temp_map_index_Arc'), 'r', encoding='UTF-8') as f:
        tmp_ind_arc = f.read()
    with open(os.path.join(os.path.dirname(__file__), 'Template', 'Temp_map_index_noArc'), 'r', encoding='UTF-8') as f:
        tmp_ind_no_arc = f.read()

    lst_ai = (
        'coSim', 'coRepair', 'coUpdRepair', 'Message.msg_fBreak', 'Message.msg_qbiValue', 'Value', 'fValue', 'iValue',
        'qbiValue', 'sChlType', 'sEnRepair', 'TRepair', 'Value100', 'aH', 'aL', 'fParam', 'fOverlow', 'fOverhigh',
        'fHighspeed', 'Repair', 'Sim', 'wH', 'wL', 'sEnaH', 'sBndaH', 'sEnaL', 'sBndaL', 'sEnwH', 'sBndwH', 'sEnwL',
        'sBndwL', 'sEnRate', 'sBndRate', 'sHighLim', 'sHys', 'sLowLim', 'sSimValue', 'sTaH', 'sTaL', 'sTRepair', 'sTwH',
        'sTwL', 'sHighiValue', 'sLowiValue'
    )
    lst_ae = (
        'coSim', 'coRepair', 'coUpdRepair', 'Message.msg_fBreak', 'Message.msg_qbiValue', 'Value', 'fValue', 'iValue',
        'qbiValue', 'sChlType', 'sEnRepair', 'TRepair', 'Value100', 'aH', 'aL', 'fParam', 'fOverlow', 'fOverhigh',
        'fHighspeed', 'Repair', 'Sim', 'wH', 'wL', 'sEnaH', 'sBndaH', 'sEnaL', 'sBndaL', 'sEnwH', 'sBndwH', 'sEnwL',
        'sBndwL', 'sEnRate', 'sBndRate', 'sHighLim', 'sHys', 'sLowLim', 'sSimValue', 'sTaH', 'sTaL', 'sTRepair', 'sTwH',
        'sTwL'
    )
    lst_di = (
        'coSim', 'brk', 'kz', 'coRepair', 'coUpdRepair', 'fParam', 'Value', 'fValue', 'Message.msg_brk',
        'Message.msg_qbiValue', 'Message.msg_kz', 'qbiValue', 'Repair', 'sBlkPar', 'Sim', 'sSimValue', 'TRepair',
        'sTRepair'
    )
    lst_im1x0 = (
        'coOn', 'coOff', 'Message.msg_fwcOn', 'Message.msg_fwsDu', 'Message.msg_qbiDu', 'Message.msg_qboOn', 'oOff',
        'oOn', 'fFlt', 'fwcOn', 'pcoMan', 'pcoOff', 'pcoOn', 'pMan', 'qbiDu', 'qboOn', 'Repair', 'fwsDu', 'wbcaOff',
        'wbcaOn', 'wMU', 'wRU', 'TRepair', 'coRepair', 'sTRepair', 'coUpdRepair', 'coMan'
    )

    with open('Source_list', 'r') as f:
        while 8:
            line_source = f.readline().strip().split(',')
            if line_source == ['']:
                break
            sl_global_ai, sl_tmp_ai = {}, {}
            sl_global_ae, sl_tmp_ae = {}, {}
            sl_global_di, sl_tmp_di = {}, {}
            sl_global_im1x0, sl_tmp_im1x0 = {}, {}
            sl_global_fast = {}
            s_all = ''
            '''Если есть файл аналогов'''
            if os.path.isfile(os.path.join(line_source[1], '0_par_A.st')):
                with open(os.path.join(line_source[1], '0_par_A.st')) as f_par_a:
                    text = f_par_a.read().split('\n')
                sl_tmp_ai = create_sl(text, 'AI_')

            '''Если есть файл расчётных'''
            if os.path.isfile(os.path.join(line_source[1], '0_par_Evl.st')):
                with open(os.path.join(line_source[1], '0_par_Evl.st')) as f_par_evl:
                    text = f_par_evl.read().split('\n')
                sl_tmp_ae = create_sl(text, 'AE_')

            '''Если есть файл дискретных'''
            if os.path.isfile(os.path.join(line_source[1], '0_par_D.st')):
                with open(os.path.join(line_source[1], '0_par_D.st')) as f_par_d:
                    text = f_par_d.read().split('\n')
                sl_tmp_di = create_sl(text, 'DI_')

            '''Если есть файл ИМ_1x0'''
            if os.path.isfile(os.path.join(line_source[1], '0_IM_1x0.st')):
                with open(os.path.join(line_source[1], '0_IM_1x0.st')) as f_im:
                    text = f_im.read().split('\n')
                sl_tmp_im1x0 = create_sl_im(text)

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
                                sl_global_ai[line[0][line[0].find('|')+1:]] = [max(int(line[9]), int(line[10])),
                                                                               line[1]]
                            else:
                                sl_global_ai['Message.' + line[0][line[0].find('|') + 1:]] = [max(int(line[9]),
                                                                                                  int(line[10])),
                                                                                              line[1]]

                        elif 'A_EVL|' in line and len(line.split(',')) >= 10:
                            line = line.split(',')
                            if 'msg' not in line[0]:
                                sl_global_ae[line[0][line[0].find('|')+1:]] = [max(int(line[9]), int(line[10])),
                                                                               line[1]]
                            else:
                                sl_global_ae['Message.' + line[0][line[0].find('|') + 1:]] = [max(int(line[9]),
                                                                                                  int(line[10])),
                                                                                              line[1]]
                        elif 'D_INP|' in line and len(line.split(',')) >= 10:
                            line = line.split(',')
                            if 'msg' not in line[0]:
                                sl_global_di[line[0][line[0].find('|')+1:]] = [max(int(line[9]), int(line[10])),
                                                                               line[1]]
                            else:
                                sl_global_di['Message.' + line[0][line[0].find('|') + 1:]] = [max(int(line[9]),
                                                                                                  int(line[10])),
                                                                                              line[1]]
                        elif 'IM_1x0|' in line and len(line.split(',')) >= 10:
                            line = line.split(',')
                            if 'msg' not in line[0]:
                                sl_global_im1x0[line[0][line[0].find('|')+1:]] = [max(int(line[9]), int(line[10])),
                                                                                  line[1]]
                            else:
                                sl_global_im1x0['Message.' + line[0][line[0].find('|') + 1:]] = [max(int(line[9]),
                                                                                                     int(line[10])),
                                                                                                 line[1]]

                        if 'FAST|' in line:
                            line = line.split(',')
                            '''В словаре sl_global_fast лежит  алг имя(FAST|): индекс переменной'''
                            sl_global_fast[line[0][1:]] = max(int(line[9]), int(line[10]))
            '''В словаре sl_global_ai лежит подимя[индекс массива]: [индекс переменной, тип переменной(I, B, R)]'''
            sl_global_ai = {key: value for key, value in sl_global_ai.items() if key[:key.find('[')] in lst_ai}
            sl_global_ae = {key: value for key, value in sl_global_ae.items() if key[:key.find('[')] in lst_ae}
            sl_global_di = {key: value for key, value in sl_global_di.items() if key[:key.find('[')] in lst_di}
            sl_global_im1x0 = {key: value for key, value in sl_global_im1x0.items() if key[:key.find('[')] in lst_im1x0}

            '''Обработка и запись в карту аналогов'''

            if sl_global_ai and sl_tmp_ai:
                s_all += create_group_par(sl_global_ai, sl_tmp_ai, sl_global_fast, tmp_ind_arc, tmp_ind_no_arc,
                                          'AI', line_source[0])

            '''Обработка и запись в карту расчётных'''

            if sl_global_ae and sl_tmp_ae:
                s_all += create_group_par(sl_global_ae, sl_tmp_ae, sl_global_fast, tmp_ind_arc, tmp_ind_no_arc,
                                          'AE', line_source[0])

            '''Обработка и запись в карту дискретных'''
            if sl_global_di and sl_tmp_di:
                s_all += create_group_par(sl_global_di, sl_tmp_di, sl_global_fast, tmp_ind_arc, tmp_ind_no_arc,
                                          'DI', line_source[0])

            '''Обработка и запись в карту ИМ1x0'''
            if sl_global_im1x0 and sl_tmp_im1x0:
                s_all += create_group_im(sl_global_im1x0, sl_tmp_im1x0, sl_global_fast, tmp_ind_arc, tmp_ind_no_arc,
                                         line_source[0])

            with open(f'trei_map_{line_source[0]}.xml', 'w') as f_out:
                f_out.write('<root format-version=\"0\">\n' + s_all.rstrip() + '\n</root>')


try:
    print(datetime.datetime.now())
    create_index()
except (BaseException, KeyError):
    logging.basicConfig(filename='app.log', filemode='a', datefmt='%d.%m.%y %H:%M:%S',
                        format='%(levelname)s - %(message)s - %(asctime)s')
    logging.exception("Ошибка выполнения")

print(datetime.datetime.now())
'''
for key, value in sl_tmp_ae.items():
    print(key, value)
'''
