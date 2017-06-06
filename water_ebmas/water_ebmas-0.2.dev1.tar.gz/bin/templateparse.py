# -*- coding: UTF-8 -*-
from lxml import etree
from lxml import objectify
import MySQLdb
import  pandas as pd
from pandas import DataFrame
import datetime
from datetime import datetime
import sys

def get_arg_dic():
    conn = MySQLdb.connect(host='192.168.10.150', port=3306, db='dm_metabase', user='dmer', passwd='dmer',charset='utf8')
    cursor = conn.cursor()
    # sql = 'select * from dm_user_info'
    # sql = 'show tables'
    sql = 'select * from dm_arg_spark_dic'
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        dic_arg = {}
        for row in results:
            id = row[0]
            name = row[1]
            dic_arg[name] = id
        return dic_arg
        # conn.commit()
    except:
        conn.rollback()
        # conn.close()

def get_desc_dic():
    conn = MySQLdb.connect(host='192.168.10.150', port=3306, db='dm_metabase', user='dmer', passwd='dmer',charset='utf8')
    cursor = conn.cursor()
    # sql = 'select * from dm_user_info'
    # sql = 'show tables'
    sql = 'select * from dm_desc_spark_dic'
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        dic_arg = {}
        for row in results:
            id = row[0]
            name = row[1]
            dic_arg[name] = id
        return dic_arg
        # conn.commit()
    except:
        conn.rollback()
        # conn.close()

def get_interp_type_dic():
    conn = MySQLdb.connect(host='192.168.10.150', port=3306, db='dm_metabase', user='dmer', passwd='dmer',charset='utf8')
    cursor = conn.cursor()
    # sql = 'select * from dm_user_info'
    # sql = 'show tables'
    sql = 'select * from dm_var_interp_type'
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        dic_interp_type = {}
        for row in results:
            id = row[0]
            name = row[1]
            dic_interp_type[name] = id
        return dic_interp_type
        # conn.commit()
    except:
        conn.rollback()
        # conn.close()

def get_var_method_dic():
    conn = MySQLdb.connect(host='192.168.10.150', port=3306, db='dm_metabase', user='dmer', passwd='dmer',charset='utf8')
    cursor = conn.cursor()
    # sql = 'select * from dm_user_info'
    # sql = 'show tables'
    sql = 'select * from dm_var_method'
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        dic_var_method = {}
        for row in results:
            id = row[0]
            name = row[1]
            dic_var_method[name] = id
        return dic_var_method
        # conn.commit()
    except:
        conn.rollback()
        # conn.close()


def get_colum_dic(proj_id):
    conn = MySQLdb.connect(host='192.168.10.150', port=3306, db='dm_metabase', user='dmer', passwd='dmer',charset='utf8')
    cursor = conn.cursor()
    # sql = 'select * from dm_user_info'
    # sql = 'show tables'
    sql = """select col_name,id from dm_data_source where pro_id =%d""" % (int(proj_id))
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        dic_colum = {}
        for row in results:
            colname = row[0]
            id = row[1]
            dic_colum[colname] = id
        return dic_colum
        # conn.commit()
    except:
        conn.rollback()
        # conn.close()

def insert_busi(sql):
    conn = MySQLdb.connect(host='192.168.10.150', port=3306, db='dm_metabase', user='dmer', passwd='dmer',charset='utf8')
    cursor = conn.cursor()
    # sql = 'select * from dm_user_info'
    # sql = 'show tables'
    # sql = """insert into dm_busi(id,busi_id,algo_id,dic_type, dic_id, value, time) values (,1,4002,0,5,'gini',)"""
    try:
        cursor.execute(sql)
        print "*********************"
        results = cursor.fetchall()
        conn.commit()
    except:
        conn.rollback()
        # conn.close()

def parse_xml(path):
    # path = "D:\\work\\busi_template\\classification_rf_test2.xml"
    # path = '/opt/LYB/template/junk_message_gbtsregression.xml'
    parsed = objectify.parse(open(path))
    root = parsed.getroot()
    busi_id = root.find("busi_id").text
    algo_id = root.find("algo_id").text
    version = root.find("version").text
    framework = root.find("framework").text
    instance_id = root.find("instance_id").text
    model_path = root.find("model_path").text
    if model_path is None:
        model_path_str = '"''"'
    else:
        model_path_str = '"' + model_path + '"'

    conn = MySQLdb.connect(host='192.168.10.150', port=3306, db='dm_metabase', user='dmer', passwd='dmer',charset='utf8')
    conn.set_character_set('utf8')
    cursor = conn.cursor()
    sql = """select proj_id from dm_busi_core where id = %d""" % (int(busi_id))
    cursor.execute(sql)
    results = cursor.fetchall()
    conn.commit()
    proj_id = results[0][0]
    colum_dic = get_colum_dic(proj_id)
    # print root.tag
    # print etree.tostring(root)
    reload(sys)
    sys.setdefaultencoding('utf-8')
    for child in root.getchildren():
        # print child.tag
        # print int(busi_id)
        # if(cmp(child.tag,"parm") & cmp(child.tag,"desc") & cmp(child.tag, "variables")):
            # print child.tag,child.pyval
            # print '-----------------------------'
        if (cmp(child.tag, "classification") == 0):
            classification = root.find("classification").text
            time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sql = ("insert into dm_busi_recode(busi_id,algo_id,dic_type,dic_id,val,time) "
                                  "values(%d,%d,%d,%d,\'%s\',\"%s\")"
                                  % (int(busi_id), int(algo_id), 0, 29, classification, time))
            try:
                cursor.execute(sql)
                results = cursor.fetchall()
                conn.commit()
                print sql
                # print int(cursor.lastrowid)
                # print results
            except:
                conn.rollback()
                # conn.close()

        if (cmp(child.tag, "variables") == 0):
            print '--------------variables  start--------------'
            variables = root.find('variables')
            interp_type_dic = get_interp_type_dic()
            var_method_dic = get_var_method_dic()
            # print interp_type_dic
            # print  variables.tag
            for variables_elt in variables:
                for variables_elt_child  in variables_elt.getchildren():
                    if (cmp(variables_elt_child.tag, "independent_variable") == 0):
                        # print variables_elt_child.tag
                        for independent_variable in variables_elt_child.getchildren():
                            # print independent_variable.tag
                            if (cmp(independent_variable.tag, "original") == 0):
                                # list_len = len(independent_variable.getchildren())
                                # print independent_variable.tag,list_len
                                if independent_variable.find('var') is not None:
                                    for vars in independent_variable.find('var'):
                                        var_name = vars.get("name")
                                        col_name = vars.get("colname")
                                        col_id = colum_dic[col_name]
                                        mode = vars.find('mode').get("name")
                                        mode_id = var_method_dic[mode]
                                        interpolation = vars.find('interpolation')
                                        var_mapping = vars.find('var_mapping')
                                        var_order = vars.get("var_order")
                                        if var_mapping is None:
                                            var_mapping = ""
                                        if interpolation is None:
                                            sql = ("insert into dm_var(var_name,busi_id,col_id,var_type,var_method,var_mapping,var_order) "
                                            "values (\"%s\",%d,%d,%d,%d,\"%s\",%d)" % (
                                            var_name, int(busi_id), int(col_id), 1, int(mode_id), var_mapping, int(var_order)))
                                        else:
                                            # print interpolation.text
                                            var_interp_type = interp_type_dic[interpolation.text]
                                            # print var_name,busi_id,col_id, interpolation,var_interp_type,mode
                                            sql = ("insert into dm_var(var_name,busi_id,col_id,var_type,var_interp_type,var_method,var_mapping,var_order) "
                                               "values (\"%s\",%d,%d,%d,%d,%d,\"%s\",%d)"%(var_name, int(busi_id), int(col_id), 1, int(var_interp_type), int(mode_id), var_mapping, int(var_order)) )
                                        try:
                                            print sql
                                            cursor.execute(sql)
                                            results = cursor.fetchall()
                                            conn.commit()

                                            # print int(cursor.lastrowid)
                                            # print results
                                        except:
                                            conn.rollback()
                                            # conn.close()
                                        var_id = int(cursor.lastrowid)
                                        # print var_id
                                        mode =vars.find('mode')
                                        print mode.find('value')
                                        if(mode.find('value') != None):
                                            for values in mode.find('value'):
                                                var_lable = values.get("name")
                                                label_code = values.get("label_code")
                                                var_formula_str = values.text
                                                # print var_lable,var_formula_str
                                                print "------------------------"
                                                sql = ("insert into dm_var_formula(var_id,var_label,var_formula_str,label_code)"
                                                       "values (%d,\'%s\',\'%s\',%d)" % (var_id, var_lable, var_formula_str, int(label_code)))
                                                try:
                                                    cursor.execute(sql)
                                                    results = cursor.fetchall()
                                                    conn.commit()
                                                    print sql
                                                    # print int(cursor.lastrowid)
                                                    # print results
                                                except:
                                                    conn.rollback()
                                                    # conn.close()

                            if (cmp(independent_variable.tag, "customized") == 0):
                                if independent_variable.find('var') is not None:
                                    for vars in independent_variable.find('var'):
                                        var_name = vars.get("name")
                                        var_order = vars.get("var_order")
                                        # print var_name

                                        sql = ("insert into dm_var(var_name,busi_id,var_type,var_method,var_order)"
                                               "values (\"%s\",%d,%d,%d,%d)" % (var_name, int(busi_id), 1, 4, int(var_order)) )
                                        try:
                                            cursor.execute(sql)
                                            results = cursor.fetchall()
                                            conn.commit()
                                            print sql
                                            # print int(cursor.lastrowid)
                                            # print results
                                        except:
                                            conn.rollback()
                                            # conn.close()
                                        var_id = int(cursor.lastrowid)
                                        # print var_id
                                        # if(vars.find('mode') == None):
                                        #     break
                                        cust_var = vars.find('value')
                                        # print cust_var
                                        print "+++++++++++++++++++++"
                                        if(cust_var != None):
                                            for values in cust_var:
                                                var_lable = values.get("name")
                                                label_code = values.get("label_code")
                                                var_formula_str = values.text
                                                # print var_lable,var_formula_str
                                                sql = ("insert into dm_var_formula(var_id,var_label,var_formula_str,label_code)"
                                                "values (%d,\'%s\',\'%s\',%d)" % (var_id, var_lable, var_formula_str, int(label_code)))
                                                try:
                                                    cursor.execute(sql)
                                                    results = cursor.fetchall()
                                                    conn.commit()
                                                    print sql
                                                    # print int(cursor.lastrowid)
                                                    # print results
                                                except:
                                                    conn.rollback()
                                                    # conn.close()
                                                # print sql
                                                # print results

                    if (cmp(variables_elt_child.tag, "dependent_variable") == 0):
                        for dependent_variable in variables_elt_child.getchildren():
                            if (cmp(dependent_variable.tag, "original") == 0):
                                if dependent_variable.find('var') is not None:
                                    for vars in dependent_variable.find('var'):
                                        var_name = vars.get("name")
                                        col_name = vars.get("colname")
                                        col_id = colum_dic[col_name]
                                        mode = vars.find('mode').get("name")
                                        mode_id = var_method_dic[mode]
                                        interpolation = vars.find('interpolation')
                                        var_mapping = vars.find('var_mapping')
                                        var_order = vars.get("var_order")
                                        if var_mapping is None:
                                            var_mapping = ""
                                        if interpolation is None:
                                            sql = ("insert into dm_var(var_name,busi_id,col_id,var_type,var_method,var_mapping) "
                                            "values (\"%s\",%d,%d,%d,%d,\"%s\")" % (
                                            var_name, int(busi_id), int(col_id), 0, int(mode_id), var_mapping))
                                        else:
                                            var_interp_type = interp_type_dic[interpolation.text]
                                            # print busi_id, var_name, col_id, interpolation, var_interp_type, mode
                                            sql = ("insert into dm_var(var_name, busi_id, col_id, var_type, var_interp_type, var_method, var_mapping) "
                                               "values (\"%s\",%d,%d,%d,%d,%d,\'%s\')"
                                               % (var_name, int(busi_id), int(col_id), 0, int(var_interp_type), int(mode_id), var_mapping))
                                        # print sql
                                        try:
                                            cursor.execute(sql)
                                            results = cursor.fetchall()
                                            conn.commit()
                                            print sql
                                            # print int(cursor.lastrowid)
                                            # print results
                                        except:
                                            conn.rollback()
                                            # conn.close()
                                        # print results
                            if (cmp(dependent_variable.tag, "customized") == 0):
                                if dependent_variable.find('var') is not None:
                                    for vars in dependent_variable.find('var'):
                                        var_name = vars.get("name")
                                        mode = vars.find('mode').get("name")
                                        mode_id = var_method_dic[mode]
                                        interpolation = vars.find('interpolation').text
                                        var_interp_type = interp_type_dic[interpolation]

                                        sql = ("insert into dm_var(var_name,busi_id,var_type,var_interp_type,var_method)" \
                                              "values (\"%s\",%d,%d,%d,%d)" % (var_name, int(busi_id),1, int(var_interp_type), int(mode_id)) )
                                        cursor.execute(sql)
                                        results = cursor.fetchall()
                                        conn.commit()
                                        var_id = int(cursor.lastrowid)
                                        # print var_name
                                        for values in vars.find("value"):
                                            var_lable = values.get("name")
                                            label_code = values.get("label_code")
                                            var_formula_str = values.text
                                            # print var_lable, var_formula_str
                                            sql = (
                                            "insert into dm_var_formula(var_id,var_label,var_formula_str,label_code)"
                                            "values (%d,\"%s\",\"%s\",%d)" % (
                                            var_id, var_lable, var_formula_str, int(label_code)))
                                            try:
                                                cursor.execute(sql)
                                                results = cursor.fetchall()
                                                conn.commit()
                                                print sql
                                                # print int(cursor.lastrowid)
                                                # print results
                                            except:
                                                conn.rollback()
                                                # conn.close()

                    if (cmp(variables_elt_child.tag, "marking_variable") == 0):
                        if variables_elt_child.find('var') is not None:
                            for vars in variables_elt_child.find('var'):
                                var_name = vars.get("name")
                                col_name = vars.get("colname")
                                col_id = colum_dic[col_name]
                                # interpolation = vars.find('interpolation').text
                                # var_interp_type = interp_type_dic[interpolation]
                                # mode = vars.find('mode').get("name")
                                # mode_id = var_method_dic[mode]
                                print var_name, busi_id, col_id
                                sql = ("insert into dm_var(var_name,busi_id,col_id,var_type)"
                                       "values (\"%s\",%d,%d,%d)" % (var_name, int(busi_id), int(col_id), 2))
                                # print sql
                                try:
                                    cursor.execute(sql)
                                    results = cursor.fetchall()
                                    conn.commit()
                                    print sql
                                    # print int(cursor.lastrowid)
                                    # print results
                                except:
                                    conn.rollback()
                                    # conn.close()
                                # print results

            print '--------------variables  end--------------'

        if (cmp(child.tag, "parms")==0):
            print '--------------parm start------------------'
            # insert_busi()
            dict = get_arg_dic()
            # print dict
            parms = root.find('parms')
            type = 0
            if parms.find('parm') is not None:
                print len(parms.find('parm'))
                for parm in parms.find('parm'):
                    # print parm.get("name"),parm.text
                    name = parm.get("name")
                    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    sql = ("insert into dm_busi_recode(busi_id,algo_id,dic_type,dic_id,val,time) "
                           "values(%d,%d,%d,%d,\'%s\',\"%s\")"
                           % (int(busi_id), int(algo_id), type, int(dict[name]), parm.text, time))
                    print sql
                    try:
                        cursor.execute(sql)
                        results = cursor.fetchall()
                        conn.commit()
                        # print int(cursor.lastrowid)
                        # print results
                    except:
                        conn.rollback()
                        # conn.close()
                print '--------------parm end------------------'

        if(cmp(child.tag,"descs")==0):
            print '--------------desc start------------------'
            dict = get_desc_dic()
            descs = root.find('descs')
            type = 1
            if descs.find('desc') is not None:
                print len(descs.find('desc'))
                for desc in descs.find('desc'):
                    # print desc.get("name"),desc.text
                    name = desc.get("name")
                    print name
                    if(cmp(name,"rule")==0):
                        val_path = desc.text
                        val_text = open(val_path).read()
                        # print val_text
                    else:
                        val_text = desc.text
                    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    sql = ("insert into dm_busi_recode(busi_id,algo_id,dic_type,dic_id,val,time) "
                           "values(%d,%d,%d,%d,\"%s\",\"%s\")"
                           % (int(busi_id), int(algo_id), type, int(dict[name]), val_text, time))
                    print sql
                    try:
                        cursor.execute(sql)
                        results = cursor.fetchall()
                        conn.commit()
                        # print int(cursor.lastrowid)
                        # print results
                    except:
                        conn.rollback()
                        # conn.close()
                print '--------------desc end-------------------'

    # print algo_id, model_path_str
    if instance_id is None:
        sql = """update dm_busi_core set busi_status = 1, algo_code = %d,
            algo_store_path = %s  where id = %d""" % (int(algo_id), model_path_str, int(busi_id))
        print sql
    else:
        sql = """update dm_busi_core set busi_status = 1, algo_code = %d ,algo_inst_id = %d,
          algo_store_path = %s  where id = %d""" % (int(algo_id), int(instance_id), model_path_str, int(busi_id))
        print sql
    cursor.execute(sql)
    results = cursor.fetchall()
    conn.commit()
    conn.close()

if __name__ == '__main__':
    args = sys.argv
    if args.__len__() == 2:
        path = args[1]
        parse_xml(path)
    else:
        print('print input path of the template file ')

