# coding=utf-8
#######################################################
# filename:test_xlrd.py
# author:defias
# date:xxxx-xx-xx
# function：读excel文件中的数据
#######################################################
import os, sys, subprocess, time
import re,shutil
#import xlrd
#import xlutils.copy
import  re,  datetime, string

reload(sys)
sys.setdefaultencoding('utf8')


class excel_object(object):
    csvfilename = ''
    num_rows = 0
    num_cols = 0
    workbook = ''
    worksheets = ''
    worksheet1 = ''
    wb = ''
    ws = ''
    non_distrubance_phone_dict = {}
    non_distrubance_phone_dict_label = {}

    X_distrubance_count_dict = {}
    Y_distrubance_count_dict = {}
    Z_distrubance_count_dict = {}

    def __init__(self, excel_file_name):
        # 打开一个workbook
        self.csvfilename = excel_file_name
        if False:
            self.workbook = xlrd.open_workbook(excel_file_name)
            self.wb = xlutils.copy.copy(self.workbook)
            self.ws = self.wb.get_sheet(0)

            # 抓取所有sheet页的名称
            self.worksheets = self.workbook.sheet_names()
            print('worksheets is %s' % self.worksheets)

            self.workbook = xlrd.open_workbook(excel_file_name)
            # 再次定位到sheet1
            self.worksheet1 = self.workbook.sheet_by_name(self.worksheets[0])
            self.num_rows = self.worksheet1.nrows
            self.num_cols = self.worksheet1.ncols

            print 'num_rows is %d' % self.num_rows

    '''
    def get_non_distrubance_phone_info(self):
        for rown in range(self.num_rows):
            try:
                str_non_distrubance_phone_list = self.worksheet1.cell_value(rown, 0)
                #re.sub(" +", " ", non_distrubance_phone_list)

                str_non_distrubance_phone_list = ' '.join(str_non_distrubance_phone_list.split())

                if not '.wav'in str_non_distrubance_phone_list:
                    continue

                filename = str_non_distrubance_phone_list.split()[0].split('/')[-1]
                label = str_non_distrubance_phone_list.split()[3]

                if label not in '非骚扰电话':
                    continue

                print self.num_rows
                #print filename, label

                if not self.non_distrubance_phone_dict.has_key(filename):
                    #print 'HERE: phone dict---- label: %s, filename %s' %(label, filename)
                    self.non_distrubance_phone_dict[filename] = [label]
                    print 'HERE: phone dict---- filename %s, value %s' %(filename, self.non_distrubance_phone_dict[filename])
                else:
                    self.non_distrubance_phone_dict[filename].append(label)

                if not self.non_distrubance_phone_dict_label.has_key(unicode(label,"utf8")):
                    #print 'HERE: label dict---- label: %s, filename %s' % (label, filename)
                    self.non_distrubance_phone_dict_label[unicode(label, "utf8")] = [filename]
                    self.non_distrubance_phone_dict_label[unicode(label, "utf8")].append(filename)

            except Exception as err:
                print 'ERRPOR! %s, rown %d '%(err, rown)
    '''

    def get_non_distrubance_phone_info_via_csv(self):
        try:
            with open(self.csvfilename) as f:
                for line in f:
                    str_non_distrubance_phone_list =  ' '.join(line.split())
                    if not '.wav' in str_non_distrubance_phone_list:
                        continue
                    if len(str_non_distrubance_phone_list.split()) < 6:
                        continue
                    filename = str_non_distrubance_phone_list.split()[0].split('/')[-1]
                    label = str_non_distrubance_phone_list.split()[3]
                    sub_label = str_non_distrubance_phone_list.split()[-1]

                    #print label

                    if label not in '非骚扰电话':
                        continue

                    # print filename, label

                    if not self.non_distrubance_phone_dict.has_key(filename):
                        # print 'HERE: phone dict---- label: %s, filename %s' %(label, filename)
                        self.non_distrubance_phone_dict[filename] = [sub_label]
                    else:
                        self.non_distrubance_phone_dict[filename].append(sub_label)

                    if not self.non_distrubance_phone_dict_label.has_key(sub_label):
                        # print 'HERE: label dict---- label: %s, filename %s' % (label, filename)
                        self.non_distrubance_phone_dict_label[sub_label] = [filename]
                        self.non_distrubance_phone_dict_label[sub_label].append(filename)

            f.close()

        except Exception as err:
            print 'ERRPOR! %s, line  %s'%(err, line)

    def _count_label_statistics(self, dict_Name, dict_distrubance_count_dict):
        i = 0
        for filenamekey in dict_Name:
            #print filenamekey
            if self.non_distrubance_phone_dict.has_key(filenamekey):
                #print 'HERE!! filenamekey %s!' %filenamekey
                sub_label = self.non_distrubance_phone_dict[filenamekey][0]
                #print label
                if not dict_distrubance_count_dict.has_key(sub_label):
                    dict_distrubance_count_dict[sub_label] = 1
                else:
                    dict_distrubance_count_dict[sub_label] = dict_distrubance_count_dict[sub_label] + 1
            else:
                #print '###%s### not in self.non_distrubance_phone_dict!' %filenamekey
                #print len(self.non_distrubance_phone_dict)

                if not filenamekey.find('15676548990_11_0_20160811092441666')>= 0:
                    continue
                #if i < 100:
                fileout = file('why_no_match.txt', 'a')
                fileout.writelines('###%s### not in non_distrubance_phone_dict\n' %filenamekey)
                fileout.close()
                i = i + 1
        for filekey in self.non_distrubance_phone_dict:
            if not filekey.find('15676548990_11_0_20160811092441666')>= 0:
                continue
            fileout2 = file('non_distrubance_phone_dict.txt', 'a')
            fileout2.writelines('filekey: %s, label: %s\n' %(filekey, self.non_distrubance_phone_dict[filekey]))
            fileout2.close()

    def get_statistics_of_non_distrubance_X_Y_Z(self, dict_X, dict_Y, dict_Z):
        self._count_label_statistics(dict_X, self.X_distrubance_count_dict)
        self._count_label_statistics(dict_Y, self.Y_distrubance_count_dict)
        self._count_label_statistics(dict_Z, self.Z_distrubance_count_dict)

    def prompt_counting_result(self):
        X_total = 0
        Y_total = 0
        Z_total = 0
        print '\nprompt_counting_result!\n'
        for labelkey in self.X_distrubance_count_dict:
            X_total = X_total + self.X_distrubance_count_dict[labelkey]
            print 'X: labelkey: %s, number: %d' %(labelkey, self.X_distrubance_count_dict[labelkey])

        print '\nX non_distrubance_count total number is %d\n' %X_total

        for labelkey in self.Y_distrubance_count_dict:
            Y_total = Y_total + self.Y_distrubance_count_dict[labelkey]
            print 'Y: labelkey: %s, number: %d' %(labelkey, self.Y_distrubance_count_dict[labelkey])

        print '\nY non_distrubance_count total number is %d\n' %Y_total
        for labelkey in self.Z_distrubance_count_dict:
            Z_total = Z_total + self.Z_distrubance_count_dict[labelkey]
            print 'Z: labelkey: %s, number: %d' %(labelkey, self.Z_distrubance_count_dict[labelkey])
        print '\nZ non_distrubance_count total number is %d\n' %Z_total
        print '\nY + Z non_distrubance_count total number is %d\n' % (Y_total + Z_total)

filename_for_classify = []
model_file_and_flassify_dict = {}
dict_template_result = {}

def verify_for_flags(result_file, local_black_non_black_flag, local_file_classify_flag, file_item_in_result_file, model_file):
    file_item_in_template = ''
    '''
    with open(model_file) as f:
        for line in f:
            if line is '\n' or line is '' or len(line) < 5:
                continue

            line = unicode(line, "utf8")
            line = line.replace('      ', '****')

            filename, file_classify, black_non_black = line.split('****')[0], line.split('****')[1], line.split('****')[2]
            model_file_and_flassify_dict[filename] = [black_non_black, file_classify]

    f.close()
    
    with open(result_file) as f:
        for line in f:
            template_file_name, result_file_item = line.split(',')[0].split('/')[1], line.split(',')[1]

            if file_item_in_result_file is result_file_item:
                file_item_in_template = template_file_name
                break
        f.close()
    '''
    if dict_template_result.has_key(file_item_in_result_file):
        file_item_in_template = dict_template_result[file_item_in_result_file]


    if file_item_in_template != '' and  model_file_and_flassify_dict.has_key(file_item_in_template):
        print 'file_item_in_template is : ' +  file_item_in_template
        if model_file_and_flassify_dict[file_item_in_template][0] != local_black_non_black_flag:
            print 'set false! file %s, local_black_non_black_flag is %s!!, model_file_and_flassify_dict[file_item_in_template][0] is %s!!' \
                  %(file_item_in_template, local_black_non_black_flag, model_file_and_flassify_dict[file_item_in_template][0])
            is_Y_black_non_black_verify_passed = 0
        else:
            is_Y_black_non_black_verify_passed = 1

        if model_file_and_flassify_dict[file_item_in_template][1] != local_file_classify_flag:
            is_Y_file_classify_verify_passed = 0
        else:
            is_Y_file_classify_verify_passed = 1
    else:
        fileremove = file(r'file_need_remove.txt', 'a')
        fileremove.write(file_item_in_template+'\n')
        fileremove.close()
        print 'file_item_in_template is empty?: ' + file_item_in_template
        is_Y_black_non_black_verify_passed = -1
        is_Y_file_classify_verify_passed   = -1

    return is_Y_black_non_black_verify_passed, is_Y_file_classify_verify_passed

def main(filepath_filename_standard_answer, filepath_filename_test_file, is_original_standard_file):
    #print 'START'
    dicXnew = {}
    dicYnew = {}

    dicYUniqChk = {}

    dicYfilename_inX = {}

    dicMismatchZ = {}

    ipath = filepath_filename_standard_answer
    uipath = ipath
    if is_original_standard_file:
        uipath = unicode(ipath, "utf8")

    #print 'STEP -1 DONE'
    msg_classify = {}
    total_cnts = 0
    line_count_no = 1
    if os.path.exists('X_DUPLICATE.TXT'):
        os.remove('X_DUPLICATE.TXT')
    file_dup = file('X_DUPLICATE.TXT', 'a')
    with open(uipath) as f:
        for line in f:
            total_cnts = total_cnts + 1
            line = unicode(line, "utf8")
            line = line.replace('      ', 'xxxxx')
            filename = line.split('xxxxx')[0]
            msg_key = line.split('xxxxx')[1]
            #msg_key = unicode(msg_key, "utf8")
            if msg_classify.has_key(msg_key):
                msg_classify[msg_key].append( (line.split('xxxxx')[0], line.split('xxxxx')[1], line.split('xxxxx')[2]) )
            else:
                msg_classify[msg_key] = [ ( line.split('xxxxx')[0],  line.split('xxxxx')[1], line.split('xxxxx')[2]) ]
                #print len(msg_classify[msg_key])
                #print (msg_classify[msg_key])
                #print unicode(msg_classify[msg_key][0][1], "utf8")
            value_black_nonblack = line.split('xxxxx')[2].strip()
            value_classify = line.split('xxxxx')[1].strip()

            if dicXnew.has_key(filename):
                file_dup.write('duplicate line found! line: %d, filename: %s\n' %(line_count_no, filename))

            dicXnew[filename] = [filename, value_black_nonblack, value_classify]
            line_count_no = line_count_no + 1

            #print '!!!!!dicXnew: %s %s'%(filename, unicode(value_black_nonblack, "utf8"))
            # print i, filename, value_black_nonblack,"-->", DicXXall[i], DicXXall[i][1] == "非黑"
        f.close()
        file_dup.close()

        for key in msg_classify:
            filename = "file_classify_%s" %key
            filename_for_classify.append(filename)
            _file = file(filename, "w+")
            _file.close()

        for key in msg_classify:
            filename = "file_classify_%s" % key
            _file = file(filename, "a+")
            for i in range(len(msg_classify[key])):
                _file.writelines(msg_classify[key][i][0] + '      ' + msg_classify[key][i][1] + '      '+ msg_classify[key][i][2])
            _file.close()


    #print '!!!!!dicXnew count is %d' % (len(dicXnew))
    #print 'STEP 0 DONE'

    j = 0
    ipath = filepath_filename_test_file
    uipath = unicode(ipath, "utf8")

    if os.path.exists('Result_Unique.txt'):
        os.remove('Result_Unique.txt')
    fileUniqResult = file('Result_Unique.txt', 'a')
    with open(uipath) as f:
        for line in f:
            if (not line.startswith('testdata')) and (not line.startswith('modeldata')):
                continue

            filename = line.split(',')[1].split('/')[1]

            if dicYUniqChk.has_key(filename):
                continue

            dicYUniqChk[filename] = filename

            dicYnew[filename] = [filename, 'UNKNOWN']

            fileUniqResult.write(line)

        f.close()
    fileUniqResult.close()

    #print 'STEP 1 DONE, Y count is %d ' %len(dicYnew)

    Y_B   = 0
    Y_NOB = 0
    X_B   = 0
    X_NOB = 0
    Z_B   = 0
    Z_NOB = 0
    Mismatch_records = 0

    model_file = 'model.txt'
    with open(model_file) as f:
        for line in f:
            if line is '\n' or line is '' or len(line) < 5:
                continue

            line = unicode(line, "utf8")
            line = line.replace('      ', '****')

            filename, file_classify, black_non_black = line.split('****')[0], line.split('****')[1], line.split('****')[
                2].split('\n')[0]
            model_file_and_flassify_dict[filename] = [black_non_black, file_classify]

    f.close()

    ipath = filepath_filename_test_file
    result_uipath = unicode(ipath, "utf8")

    with open(result_uipath) as f:
        for line in f:
            template_file_name, result_file_item = line.split(',')[0].split('/')[1], line.split(',')[1].split('/')[1]

            if not dict_template_result.has_key(result_file_item):
                dict_template_result[result_file_item] = template_file_name

        f.close()


    for filenames in dicYnew:
        if dicXnew.has_key(filenames):
            ipath = filepath_filename_test_file
            result_uipath = unicode(ipath, "utf8")

            model_file = 'model.txt'

            check_B_NOB, check_classify = verify_for_flags(result_uipath, dicXnew[filenames][1], dicXnew[filenames][2], filenames, model_file)

            #print 'add verify info done! check_B_NOB: %d, check_classify %d' %(check_B_NOB, check_classify)
            dicYfilename_inX[filenames] = [ filenames, dicXnew[filenames][1], dicXnew[filenames][2], check_B_NOB, check_classify ] #black or nonblack
        #else:
        #    Mismatch_records = Mismatch_records + 1
        #    print 'MISMATCH FILE: ' + filenames

    #print 'dicYfilename_inX count is %d ' %(len(dicYfilename_inX))

    #while True:
    #   time.sleep(1000)
    match_file = file('match_files.txt', 'w')
    mismatch_file = file('mismatch_files.txt', 'w')

    match_file.close()
    mismatch_file.close()

    match_file = file('match_files.txt', 'a+')
    mismatch_file = file('mismatch_files.txt', 'a+')

    for filenames in dicXnew:
        if not dicYfilename_inX.has_key(filenames):
            Mismatch_records = Mismatch_records + 1
            print 'MISMATCH FILE: ' + filenames

            dicMismatchZ[filenames] = filenames

            if mismatch_file:
                mismatch_file.writelines(filenames)
                mismatch_file.writelines('\n')
        else:
            if match_file:
                match_file.writelines(filenames)
                match_file.writelines('\n')

    match_file.close()
    mismatch_file.close()
    #print 'STEP 2 DONE'

    key_dict_x_b_key = {}
    key_dict_x_non_b_key = {}
    key_dict_y_b_key_in_x = {}
    key_dict_y_none_b_key_in_x = {}
    key_dict_z_b = {}
    key_dict_z_none_b = {}
    key_dict_y_classify_special_B = {}
    key_dict_y_classify_special_D = {}

    if os.path.exists('feisaorao.txt'):
        os.remove('feisaorao.txt')
    if os.path.exists('feizhapian.txt'):
        os.remove('feizhapian.txt')
    if os.path.exists('shehei.txt'):
        os.remove('shehei.txt')

    file111 = file('feisaorao.txt', 'a+')
    file222 = file('feizhapian.txt', 'a+')
    file333 = file('shehei.txt', 'a+')
    for filenames in dicXnew:
        #print 'dicXnew: %s: %d'  %(dicXnew[filenames],dicXnew[filenames][1] == unicode("非黑", "utf8"))
        if dicXnew[filenames][1] == unicode("黑", "utf8"):
            X_B = X_B + 1
        elif dicXnew[filenames][1] == unicode("非黑", "utf8"):
            X_NOB = X_NOB + 1

        for key in msg_classify:

            #test = unicode('诈骗电话', "utf8")
            test = unicode('非骚扰电话', "utf8")
            test2 = unicode('非诈骗电话', "utf8")
            test3 = unicode('涉黑信息', "utf8")
            non_key = unicode("非", "utf8") + key
            #print key, non_key
            if dicXnew[filenames][2] == key:
                if not key_dict_x_b_key.has_key(key):
                    key_dict_x_b_key[key] = 1
                    #print '!!!'
                    if key == test3:
                        file333.write('涉黑电话: %s\n' % dicXnew[filenames])
                    elif key == test:
                        file111.write('非骚扰电话: %s\n'  %dicXnew[filenames])

                        #print '非骚扰电话: %s '  %dicXnew[filenames]
                        #print '%s %s %d' %(key, key_dict_x_b_key, key_dict_x_b_key[key])
                    elif key == test2:
                        file222.write('非诈骗电话: %s\n' % dicXnew[filenames])

                        #print '非诈骗电话: %s ' % dicXnew[filenames]
                else:
                    key_dict_x_b_key[key] = key_dict_x_b_key[key] + 1
                    if key == test3:
                        file333.write('涉黑电话: %s\n' % dicXnew[filenames])
                    elif key == test:
                        file111.write('非骚扰电话: %s\n' % dicXnew[filenames])

                        #print '非骚扰电话: %s '  %dicXnew[filenames]
                        #print '%s %s %d' %(key, key_dict_x_b_key, key_dict_x_b_key[key])
                    elif key == test2:
                        file222.write('非诈骗电话: %s\n' % dicXnew[filenames])
                        #print '非诈骗电话: %s ' % dicXnew[filenames]

            else:
                if not key_dict_x_non_b_key.has_key(key):
                    key_dict_x_non_b_key[key] = 1
                else:
                    key_dict_x_non_b_key[key] = key_dict_x_non_b_key[key] + 1

    file111.close()
    file222.close()
    file333.close()
    # fake begin


    #while True:
    #    time.sleep(1000)
    # fake end




    #print 'STEP 3 DONE'
    B = 0
    D = 0
    special_cnt1 = 0
    special_cnt2 = 0
    special_cnt3 = 0
    special_cnt4 = 0
    for filenames in dicYfilename_inX:

        if dicYfilename_inX[filenames][1] == unicode("黑", "utf8"):
            if dicYfilename_inX[filenames][3] == -1:
                special_cnt1 = special_cnt1 + 1
            elif dicYfilename_inX[filenames][3] == 0:
                D = D + 1
            else:
                Y_B = Y_B + 1
            #print 'Y_B is %d ' % Y_B
        elif dicYfilename_inX[filenames][1] == unicode("非黑", "utf8"):
            if dicYfilename_inX[filenames][3] == -1:
                special_cnt2 = special_cnt2 + 1
            elif dicYfilename_inX[filenames][3] == 0:
                B = B + 1
            else:
                Y_NOB = Y_NOB + 1
            #print 'Y_NOB is %d ' % Y_NOB
        else:
            print 'ABNORMAL: FILENAME: %s, RECORD IS NOT IN BLACK AND NON-BLACK!' %filenames

        for key in msg_classify:
            # print "key is %s " %key
            non_key = unicode("非", "utf8") + key

            if dicYfilename_inX[filenames][2] == key:
                if dicYfilename_inX[filenames][4] == -1:
                    special_cnt3 = special_cnt3 + 1
                elif dicYfilename_inX[filenames][4] == 0:
                    if not key_dict_y_classify_special_D.has_key(key):
                        key_dict_y_classify_special_D[key] = 1
                    else:
                        key_dict_y_classify_special_D[key] = key_dict_y_classify_special_D[key] + 1

                else:
                    if not key_dict_y_b_key_in_x.has_key(key):
                        key_dict_y_b_key_in_x[key] = 1
                    else:
                        key_dict_y_b_key_in_x[key] = key_dict_y_b_key_in_x[key] + 1
            else:
                if dicYfilename_inX[filenames][4] == -1:
                    special_cnt4 = special_cnt4 + 1
                elif dicYfilename_inX[filenames][4] == 0 and dicXnew[filenames][2] == key:

                    if not key_dict_y_classify_special_B.has_key(key):
                        key_dict_y_classify_special_B[key] = 1
                    else:
                         key_dict_y_classify_special_B[key] = key_dict_y_classify_special_B[key] + 1

                else:
                    if not key_dict_y_none_b_key_in_x.has_key(key):
                        key_dict_y_none_b_key_in_x[key] = 1
                    else:
                        key_dict_y_none_b_key_in_x[key] = key_dict_y_none_b_key_in_x[key] + 1

    #print 'STEP 4 DONE'

    for filenames in dicXnew:
        if not dicYnew.has_key(filenames):
            if dicXnew[filenames][1] == unicode("黑", "utf8"):
                Z_B = Z_B + 1
            elif dicXnew[filenames][1] == unicode("非黑", "utf8"):
                Z_NOB = Z_NOB + 1

        for key in msg_classify:
            non_key = unicode("非", "utf8") + key

            if not dicYnew.has_key(filenames):
                if dicXnew[filenames][2] == key:
                    if not key_dict_z_b.has_key(key):
                        key_dict_z_b[key] = 1
                    else:
                        key_dict_z_b[key] = key_dict_z_b[key] + 1

                else:
                    if not key_dict_z_none_b.has_key(key):
                        key_dict_z_none_b[key] = 1
                    else:
                        key_dict_z_none_b[key] = key_dict_z_none_b[key] + 1



    A = Y_B
    #B = 0
    C = Z_B  # Z #Mismatch_records
    #D = 0  # min_XnonB_YB
    E = Y_NOB  # min_nonblack
    F = Z_NOB  # Z #Mismatch_records


    d_value = D
    b_value = B

    D = b_value
    B = d_value

    if is_original_standard_file:
        CHARACTER_BLACK = unicode("黑", "utf8")
        CHARACTER_NON_BLACK = unicode("非黑", "utf8")
        CHARACTER_MISMATCH = unicode("未匹配", "utf8")
        print '===========================TOTAL TABLE COUNTING START ==============================='
        print '------------------------------------------------------------------------------------------------------------'
        print '               Y%s               Y %s               Z %s   ' %(CHARACTER_BLACK, CHARACTER_NON_BLACK, CHARACTER_MISMATCH)
        print ' X %s          %f        %f              %d     ' % (CHARACTER_BLACK, A, B, C)
        print ' X %s         %f        %f          %d     ' % (CHARACTER_NON_BLACK, D, E, F)
        print '------------------------------------------------------------------------------------------------------------'

        if float(A + D) != 0:
            print '===>Precision_1 = %f ' % float(A / float(A + D))
        else:
            print '===>Precision_1 cannot be calculated due to A + D is zero'
        if float(E + B) != 0:
            print '===>Precision_2 = %f ' % float(E / float(E + B))
        else:
            print '===>Precision_2 cannot be calculated due to E + B is zero'
        if float(A + B + C) != 0:
            print '===>Recall_1 = %f ' % float(A / float(A + B + C))
        else:
            print '===>Recall_1 cannot be calculated due to A + B + C is zero'
        if float(E + F) != 0:
            print '===>Recall_2 = %f ' % float(E / float(E + F))
        else:
            print '===>Recall_2 cannot be calculated due to E + F is zero'

        print '------>X black : %d, X nonblack: %d ' % (X_B, X_NOB)
        print '------>Y black : %d, Y nonblack: %d ' % (Y_B, Y_NOB)
        print '------> Z black %d, Z non black %d' %(Z_B, Z_NOB)

    print 'SPECIAL COUNT FOR MISMATCH MODEL: %d %d %d %d' %(special_cnt1, special_cnt2, special_cnt3,special_cnt4)

    print '##################### CLASSIFY TABLES ########################################################'

    for key in msg_classify:
        # print "key is %s " %key
        non_key = unicode("非", "utf8") + key

        X_B = 0
        X_NOB = 0
        Y_B = 0
        Y_NOB = 0
        Z_B =0
        Z_NOB = 0

        if key_dict_x_b_key.has_key(key):
            X_B = key_dict_x_b_key[key]
        if key_dict_x_non_b_key.has_key(key):
            X_NOB = key_dict_x_non_b_key[key]
        if key_dict_y_b_key_in_x.has_key(key):
            Y_B = key_dict_y_b_key_in_x[key]
        if key_dict_y_none_b_key_in_x.has_key(key):
            Y_NOB = key_dict_y_none_b_key_in_x[key]
        if key_dict_z_b.has_key(key):
            Z_B = key_dict_z_b[key]
        if key_dict_z_none_b.has_key(key):
            Z_NOB = key_dict_z_none_b[key]

        if key_dict_y_b_key_in_x.has_key(key):
            A = key_dict_y_b_key_in_x[key]
        else:
            A = 0
        B = 0
        if key_dict_y_classify_special_B.has_key(key):
            B = key_dict_y_classify_special_B[key]
        if key_dict_z_b.has_key(key):
            C = key_dict_z_b[key]  # Z #Mismatch_records
        else:
            C = 0
        D = 0
        if key_dict_y_classify_special_D.has_key(key):
            D = key_dict_y_classify_special_D[key]  # min_XnonB_YB

        if key_dict_y_none_b_key_in_x.has_key(key):
            E = key_dict_y_none_b_key_in_x[key]  # min_nonblack
        else:
            E = 0

        if key_dict_z_none_b.has_key(key):
            F = key_dict_z_none_b[key] # Z #Mismatch_records
        else:
            F = 0

        CHARACTER_BLACK = key
        CHARACTER_NON_BLACK = non_key
        CHARACTER_MISMATCH = unicode("未匹配", "utf8")

        d_value = D
        b_value = B

        D = b_value
        B = d_value

        print '------------------------------------------------------------------------------------------------------------'
        print '               Y%s               Y %s               Z %s   ' % (
        CHARACTER_BLACK, CHARACTER_NON_BLACK, CHARACTER_MISMATCH)
        print ' X %s          %f        %f              %d     ' % (CHARACTER_BLACK, A, B, C)
        print ' X %s         %f        %f          %d     ' % (CHARACTER_NON_BLACK, D, E, F)
        print '------------------------------------------------------------------------------------------------------------'

        if float(A + D) != 0:
            print '===>Precision_1 = %f ' % float(A / float(A + D))
        else:
            print '===>Precision_1 cannot be calculated due to A + D is zero'
        if float(E + B) != 0:
            print '===>Precision_2 = %f ' % float(E / float(E + B))
        else:
            print '===>Precision_2 cannot be calculated due to E + B is zero'
        if float(A + B + C) != 0:
            print '===>Recall_1 = %f ' % float(A / float(A + B + C))
        else:
            print '===>Recall_1 cannot be calculated due to A + B + C is zero'
        if float(E + F) != 0:
            print '===>Recall_2 = %f ' % float(E / float(E + F))
        else:
            print '===>Recall_2 cannot be calculated due to E + F is zero'


        #print '------>X %s : %d, X %s: %d ' % (key, A+B+C, non_key, D+E+F)
        #print '------>Y %s : %d, Y %s: %d ' % (key, Y_B, non_key, Y_NOB)
        #print '------>Z %s : %d, Z %s: %d' %(key, Z_B, non_key, Z_NOB)

        print '------>X %s : %d, X %s: %d ' % (key, X_B -D, non_key, X_NOB-B)
        print '------>Y %s : %d, Y %s: %d ' % (key, Y_B, non_key, Y_NOB)
        print '------>Z %s : %d, Z %s: %d' %(key, Z_B, non_key, Z_NOB)


    xlsfile = sys.argv[3]
    EXCEL_OBJECT = excel_object(xlsfile)
    EXCEL_OBJECT.get_non_distrubance_phone_info_via_csv()
    EXCEL_OBJECT.get_statistics_of_non_distrubance_X_Y_Z(dicXnew, dicYfilename_inX, dicMismatchZ)
    EXCEL_OBJECT.prompt_counting_result()

    #else:
    #    return
    #while True:
        #time.sleep(1000)

'''
#############################################################################################

    DictinfoX = {}
    Match_records = 0
    Mismatch_records = 0
    black_recordsX = 0
    nonblack_recordsX = 0
    black_recordsY = 0
    nonblack_recordsY = 0

    DicXblack = {}
    DicXnonblack = {}
    DicYblack = {}
    DicYnonblack = {}
    DicZXblack = {}
    DicZXnonblack = {}
    DicYall = {}


    DicXXblack = {}
    DicXXnonblack = {}
    DicYYblack = {}
    DicYYnonblack = {}
    DicZZXblack = {}
    DicZZXnonblack = {}
    DicXXall = {}
    DicYYall = {}

    DicYYKeyUnical = {}

    ipath = filepath_filename_standard_answer
    uipath = unicode(ipath, "utf8")

    i = 0
    with open(uipath) as f:
        for line in f:
            line = line.replace('      ', 'xxxxx')
            filename = line.split('xxxxx')[0]
            value_black_nonblack = line.split('xxxxx')[2].strip()

            DicXXall[i] = [filename, value_black_nonblack]
            #print i, filename, value_black_nonblack,"-->", DicXXall[i], DicXXall[i][1] == "非黑"
            i = i + 1
        f.close()

    #print 'DONE PART 1'

    j = 0
    ipath = filepath_filename_test_file
    uipath = unicode(ipath, "utf8")

    with open(uipath) as f:
        for line in f:
            if (not line.startswith('testdata')) and (not line.startswith('modeldata')):
                continue

            filename = line.split(',')[1].split('/')[1]

            if DicYYKeyUnical.has_key(filename):
                continue

            DicYYKeyUnical[filename] = filename

            value_black_nonblack = 'UNKNOWN'
            #print 'DOING IN PART 2, len DicXXall is %d ' % len(DicXXall)
            for loop in DicXXall:
                if filename == DicXXall[loop][0]:
                    value_black_nonblack = DicXXall[loop][1]
                    break

            DicYYall[j] = [ filename, value_black_nonblack ]
            j = j + 1
        f.close()

    #print 'DONE PART 2'

    XB = 0
    YB = 0
    XNOB = 0
    YNOB = 0
    XB_YB = 0
    XB_YNOB = 0
    XNOB_YB = 0
    XNOB_YNOB = 0
    ZZZ = 0

    AAA = 0
    BBB = 0
    CCC = 0
    DDD = 0
    EEE = 0
    FFF = 0

    for j in DicYYall:
        Yblack_or_nonblack = DicYYall[j][1]

        if (Yblack_or_nonblack == "黑"):
            YB = YB + 1

        if (Yblack_or_nonblack == "非黑"):
            YNOB = YNOB + 1

    #print 'DONE PART 3'

    for i in DicXXall:
        #print 'DONE IN PART 4'
        X_filename = DicXXall[i][0]
        Xblack_or_nonblack = DicXXall[i][1]

        if (Xblack_or_nonblack == "黑"):
            XB = XB + 1

        if (Xblack_or_nonblack == "非黑"):
            XNOB = XNOB + 1

        is_exist = 0
        for j in DicYYall:

            if DicYYall[j][0] == X_filename:
                is_exist = 1

        if not is_exist:
            ZZZ = ZZZ+1
            print 'MISMATCH FILE: ' + X_filename

    AAA = min(XB, YB)
    BBB = min(XB, YNOB)
    DDD = min(XNOB, YB)
    EEE = min(XNOB, YNOB)
    CCC = ZZZ

    A = AAA  # min_black
    B = BBB  # min_XB_YnonB
    C = CCC  # Z #Mismatch_records
    D = DDD  # min_XnonB_YB
    E = EEE  # min_nonblack
    F = CCC  # Z #Mismatch_records

    #print black_recordsX, nonblack_recordsX, black_recordsY, nonblack_recordsY

    print '------------------------------------------------------------------------------------------------------------'
    print '               Y黑               Y 非黑               Z 未匹配   '
    print ' X 黑          %f        %f              %d     ' % (A, B, C)
    print ' X非黑         %f         %f              %d     ' % (D, E, F)
    print '------------------------------------------------------------------------------------------------------------'

    if float(A + D) != 0:
        print '===>Precision_1 = %f ' % float(A / float(A + D))
    else:
        print '===>Precision_1 cannot be calculated due to A + D is zero'
    if float(E + B) != 0:
        print '===>Precision_2 = %f ' % float(E / float(E + B))
    else:
        print '===>Precision_2 cannot be calculated due to E + B is zero'
    if float(A + B + C) != 0:
        print '===>Recall_1 = %f ' % float(A / float(A + B + C))
    else:
        print '===>Recall_1 cannot be calculated due to A + B + C is zero'
    if float(E + F) != 0:
        print '===>Recall_2 = %f ' % float(E / float(E + F))
    else:
        print '===>Recall_2 cannot be calculated due to E + F is zero'

    print '------>X black : %d, X nonblack: %d ' % (XB, XNOB)
    print '------>Y black : %d, Y nonblack: %d ' % (YB, YNOB)
    print '------> Z %d' % ZZZ

    while 1:
        time.sleep(1000);

    #ipath = 'G:\\tmpdata\\stand_answer.txt'
    ipath=filepath_filename_standard_answer
    uipath = unicode(ipath, "utf8")
    with open(uipath) as f:
        for line in f:
            line = line.replace('      ', 'xxxxx')
            keyword = line.split('xxxxx')[0]
            value_black_nonblack = line.split('xxxxx')[2].strip()

            DictinfoX[keyword] = value_black_nonblack

            if value_black_nonblack == "黑":
                black_recordsX = black_recordsX + 1
                DicXblack[keyword] = value_black_nonblack
            if value_black_nonblack == "非黑":
                nonblack_recordsX = nonblack_recordsX + 1
                DicXnonblack[keyword] = value_black_nonblack
        f.close()

    for i in sorted(DictinfoX.iteritems(), key=lambda x: x[0]):
        print i[0], i[1], black_recordsX, nonblack_recordsX

    #ipath = 'G:\\tmpdata\\涉黑.rst'
    ipath = filepath_filename_test_file
    uipath = unicode(ipath, "utf8")

    with open(uipath) as f:
        DictinfoY = {}
        for line in f:
            if (not line.startswith('testdata')) and (not line.startswith('modeldata')):
                continue
            print '!!!!!!!!!!!!!!!!!!!!!'
            print line
            print '------------------------'
            print line.split(',')[0]
            keyword = line.split(',')[0].split('/')[1]
            value_black_nonblack = line.split(',')[2].strip()

            DicYall[keyword] = value_black_nonblack

            if value_black_nonblack == "黑":
                DicYblack[keyword] = value_black_nonblack
            if value_black_nonblack == "非黑":
                DicYnonblack[keyword] = value_black_nonblack

            # found if Y in X

            if ( DictinfoX.has_key(keyword)) and ( not DictinfoY.has_key(keyword) ):
                DictinfoY[keyword] = DictinfoX[keyword]
                Match_records = Match_records + 1
                if DictinfoX[keyword] == "黑":
                    black_recordsY = black_recordsY + 1
                if DictinfoX[keyword] == "非黑":
                    nonblack_recordsY = nonblack_recordsY + 1
                #print  DictinfoX[keyword]
            else:
                DictinfoY[keyword] = 'UNKNOWN'
                #Mismatch_records = Mismatch_records + 1

                # time, size = line.strip().split()
                # time = time.replace('xxxxx', ' ')
                # record[time] = record.get(time, 0) + int(size)

        f.close()
            #time, size = line.strip().split()
            #time = time.replace('xxxxx', ' ')
            #record[time] = record.get(time, 0) + int(size)

    ipath = filepath_filename_standard_answer
    uipath = unicode(ipath, "utf8")

    Z = 0

    with open(uipath) as f:
        for line in f:
            line = line.replace('      ', 'xxxxx')
            keyword = line.split('xxxxx')[0]

            if not DictinfoY.has_key(keyword) :
                Z = Z + 1

        f.close()


    for i in sorted(DictinfoY.iteritems(),  key=lambda x: x[0]):
        print i[0], i[1]

    AA = 0
    BB = 0
    CC = 0
    DD = 0
    EE = 0
    FF = 0
    ZZ = 0
    for key in DicXblack:
        if  DicYblack.has_key(DicXblack[key]):
            AA = AA + 1

    for key in DicXblack:
        if  DicYnonblack.has_key(DicXblack[key]):
            BB = BB + 1

    for key in DicXblack:
        if (not DicYblack.has_key(DicXblack[key])) and (not DicYnonblack.has_key(DicXblack[key])):
            CC = CC + 1

    for key in DicXnonblack:
        if  DicYblack.has_key(DicXnonblack[key]):
            DD = DD + 1

    for key in DicXnonblack:
        if  DicYnonblack.has_key(DicXnonblack[key]):
            EE = EE + 1

    for key in DicXnonblack:
        if (not DicYblack.has_key(DicXnonblack[key])) and (not DicYnonblack.has_key(DicXnonblack[key])):
            FF = FF + 1

    for key in DictinfoX:
        if not DicYall.has_key(key):
            ZZ = ZZ + 1

    print 'match records %d, mismatch records(Z) %d， black_recordsX %d, nonblack_recordsX %d, ' \
          'black_recordsY %d, nonblack_recordsY %d, Z %d' \
          %(Match_records, Mismatch_records, black_recordsX, nonblack_recordsX, black_recordsY, nonblack_recordsY, Z)

    min_black    = min(black_recordsX, black_recordsY)

    min_nonblack = min(nonblack_recordsX, nonblack_recordsY)

    min_XB_YnonB = min(black_recordsX, nonblack_recordsY)
    min_XnonB_YB = min(nonblack_recordsX, black_recordsY)

    A = AA #min_black
    B = BB #min_XB_YnonB
    C = CC #Z #Mismatch_records
    D = DD #min_XnonB_YB
    E = EE #min_nonblack
    F = FF #Z #Mismatch_records

    print black_recordsX, nonblack_recordsX, black_recordsY, nonblack_recordsY

    print '------------------------------------------------------------------------------------------------------------'
    print '               Y黑               Y 非黑               Z 未匹配   '
    print ' X 黑          %f        %f              %d     ' %(A, B, C)
    print ' X非黑         %f         %f              %d     ' %(D, E, F)
    print '------------------------------------------------------------------------------------------------------------'

    if float(A + D) != 0:
        print '===>Precision_1 = %f ' % float(A / float(A + D))
    else:
        print '===>Precision_1 cannot be calculated due to A + D is zero'
    if float(E + B) != 0:
        print '===>Precision_2 = %f ' % float(E / float(E + B))
    else:
        print '===>Precision_2 cannot be calculated due to E + B is zero'
    if float(A + B + C) != 0:
        print '===>Recall_1 = %f ' % float(A / float(A + B + C))
    else:
        print '===>Recall_1 cannot be calculated due to A + B + C is zero'
    if float(E + F) != 0:
        print '===>Recall_2 = %f ' % float(E / float(E + F))
    else:
        print '===>Recall_2 cannot be calculated due to E + F is zero'

    print '------>X black : %d, X nonblack: %d ' %( len(DicXblack), len(DicXnonblack))
    print '------>Y black : %d, Y nonblack: %d ' % (len(DicYblack), len(DicYnonblack))
    print '------> Z %d' % ZZ

    #while 1:
    #    time.sleep(1000);
'''

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print 'Please input your standard file and test file and XLS file , names are like <filepath>/<filename>!'
        exit(-1);
    if os.path.exists('file_need_remove.txt'):
        os.remove('file_need_remove.txt')
    print 'Your standard filenmae is %s, test file is %s ' % (sys.argv[1], sys.argv[2])
    filepath_filename_standard_answer, filepath_filename_test_file = sys.argv[1], sys.argv[2]
    print '=====================HANDLE FILE: STANDARD==========================================\n'
    main(filepath_filename_standard_answer, filepath_filename_test_file, True)

    exit(0)

    while 1:
        time.sleep(1000);



    print '=====================HANDLE FILE: STANDARD DONE, len(filename_for_classify) is %d=======================\n' %len(filename_for_classify)

    filename_for_classify2 = filename_for_classify[:]

    for value in filename_for_classify2:
        _filename = "temp%s" %value
        shutil.copy(value, _filename)

        print '=====================HANDLE FILE: %s==========================================\n' %value
        main(_filename, filepath_filename_test_file, False)
        os.remove(_filename)

    while 1:
        time.sleep(1000);