#!/usr/bin/python3
import pymysql

class CMysql():

    def __init__(self, host, port, user, pw, database):
        self.host = host or '127.0.0.1'
        self.port = port or 3306
        self.user = user or 'root'
        self.pw = pw or ''
        self.database = database or ''

        self.conn = ''
        self.cur = ''

    def Connect(self):
        try:
            self.conn = pymysql.Connect(self.host, self.user, self.pw, self.database, self.port, charset='utf8')
            self.cur = self.conn.cursor()
        except  Exception as e:
            print(e)

    def Fetch(self, sql):
        try:
            self.cur.execute(sql)
            rows = self.cur.fetchall()
            #for row in rows:
                #print('row', row)
            return rows
        except Exception as e:
            print(e)

    def CreateTiebaTable(self, name):
        try:
            self.cur.execute('CREATE TABLE IF NOT EXISTS ' + name + '  LIKE tieba_template')
            self.conn.commit()
        except Exception as e:
            print(e)


    def Execute(self, sql):
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(e)

    #UpdateUserInfo(user_name, user_url, '', user_level)
    def UpdateUserInfo(self, user_name, user_url, user_star, user_level):
        try:
            user_id = 0
            self.cur.execute("select * from tieba_user where user_name = '" + user_name + "'")
            ret_row = self.cur.fetchall()
            if len(ret_row) == 0:
                #insert
                datas = self.Fetch('select * from tieba_coef where name_type = 1')
                for row in datas:
                    user_id = row[2]
                self.Execute('update tieba_coef set cur_index = ' + str(user_id +1) + ' where name_type = 1')

                tmp_sql = "insert into tieba_user(userid, user_name, `level`, url, user_star, create_time) value({0}, '{1}', {2}, '{3}', '{4}', now())".format(user_id, user_name, user_level, user_url, user_star)
                self.Execute(tmp_sql)
            else:
                for row in ret_row:
                    user_id = row[0]
            print('user_id', user_id)
            return user_id
        except Exception as e:
            print('error',e)
        return 0

    def Close(self):
        try:
            self.cur.close()
            self.conn.close()
        except Exception as e:
            print(e)


