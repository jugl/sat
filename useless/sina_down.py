#!/usr/bin/env python3  
# -*- coding:utf-8 -*-  
   
import mysql.connector
import sys, os
 
user = 'root'
pwd  = '654321'
host = '127.0.0.1'
db   = 'mytest'
id   = 2
stockcode = '000002.SZ'
stockname = '万科A'
mydate = '2014-11-30'

 

data_file = 'mysql-test.dat'

""" 
create_table_sql = "CREATE TABLE IF NOT EXISTS mytable ( \
                    id int(10) AUTO_INCREMENT PRIMARY KEY, \
		    name varchar(20), age int(4) ) \
		    CHARACTER SET utf8"
"""

insert_sql = "INSERT INTO t_stock_code(code, name, indate) VALUES ('000002.SZ', '万科A', '2014-11-30')"
select_sql = "SELECT id, code, name FROM t_stock_code"
 
cnx = mysql.connector.connect(user=user, password=pwd, host=host, database=db)
cursor = cnx.cursor()

""" 
try:
    #cursor.execute(create_table_sql)
except mysql.connector.Error as err:
    print("create table 'mytable' failed.")
    print("Error: {}".format(err.msg))
    sys.exit()
"""
 
try:
    cursor.execute(insert_sql)
except mysql.connector.Error as err:
    print("insert table 't_stock_code' failed.")
    print("Error: {}".format(err.msg))
    sys.exit()
 
if os.path.exists(data_file):
    myfile = open(data_file)
    lines = myfile.readlines()
    myfile.close()
 
    for line in lines:
        myset = line.split()
        sql = "INSERT INTO t_stock_code (id, code, name) VALUES ('{}', {}, {})".format(myset[0], myset[1], myset[2])
        try:
            cursor.execute(sql)
        except mysql.connector.Error as err:
            print("insert table 't_stock_code' from file 'mysql-test.dat' -- failed.")
            print("Error: {}".format(err.msg))
            sys.exit()
 
try:
    cursor.execute(select_sql)
    for (id, code, name) in cursor:
        print("id:{}  code:{}  name:{}".format(id, code, name))
except mysql.connector.Error as err:
    print("query table 't_stock_code' failed.")
    print("Error: {}".format(err.msg))
    sys.exit()
 
cnx.commit()
cursor.close()
cnx.close()

"""
download data from qq. 
"""
   
import urllib  
import urllib.request
      
#debug=True  
debug=0  
      
class Utility:  
    def ToGB(str):  
        if(debug): print(str)  
        return str.decode('gb2312')  
      
class StockInfo:  
    """ 
    0: 未知 
    1: 名字 
    2: 代码 
    3: 当前价格 
    4: 涨跌 
    5: 涨跌% 
    6: 成交量（手） 
    7: 成交额（万） 
    8: 
    9: 总市值"""  
    
    def GetStockStrByNum(num):  
        f= urllib.request.urlopen('http://qt.gtimg.cn/q=s_'+ str(num))  
        if(debug): print(f.geturl())  
        if(debug): print(f.info())  
        #return like: v_s_sz000858="51~五 粮 液~000858~18.10~0.01~0.06~94583~17065~~687.07";  
        return f.readline()  
        f.close()  
    
    def ParseResultStr(resultstr):  
        if(debug): print(resultstr)  
        slist=resultstr[14:-3]  
        if(debug): print(slist)  
        slist=slist.split('~')  
    
        if(debug) : print(slist)  
        
        #print('*******************************')  
        print('  股票名称:', slist[1])  
        print('  股票代码:', slist[2])  
        
        print('  当前价格:', slist[3])  
        print('  涨    跌:', slist[4])  
        print('  涨   跌%:', slist[5],'%')  
        print('成交量(手):', slist[6])  
        print('成交额(万):', slist[7])  
        #print('date and time is :', dateandtime)  
        print('*******************************')  
    
    def GetStockInfo(num):  
        str=StockInfo.GetStockStrByNum(num)  
        strGB=Utility.ToGB(str)  
        StockInfo.ParseResultStr(strGB)  
            

if __name__ == '__main__':  

    stocks = ['sh601398','sh601818']  

    for stock in stocks:  
        StockInfo.GetStockInfo(stock)  
