import pymysql
import xlrd

def GetDataFromExcel():
    vlist = {}
    sqllist = []
    data = xlrd.open_workbook("D:\Desktop\file.xls")  # 从 excel 文件读取数据
    table = data.sheets()[0]
    nrows = table.nrows

    for i in range(1,nrows):   # 遍历行
        for n in range(0,7):    # 遍历列
            value = table.cell(i,n).value
            if value != str(value):
                value = str(int(value))

            print(n, value)
            vlist[n] = value

        sql = "insert into commonaddressbook (department,user,position,roomNo,officeLandine,phoneNo,extend1) values ('%s','%s','%s','%s','%s','%s','%s')" % \
               (vlist[0],vlist[1],vlist[2],vlist[3],vlist[4],vlist[5],vlist[6])
        print("-----------------------")
        sqllist.append(sql)

    # 返回 sql 语句的 list
    return  sqllist


def WriteDataToDB(list):
    connect = pymysql.connect(
        host='172.17.143.230', port=3306, user='msg', passwd='123456', db='msg', charset='utf8'
    )
    cursor = connect.cursor()

    # 遍历 list 执行
    for sql in list:
        cursor.execute(sql)
        connect.commit()
    cursor.close()
    connect.close()



def main():
    list = GetDataFromExcel()
    WriteDataToDB(list)



if __name__ == "__main__":
    main()


