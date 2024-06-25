import os
import sqlite3
import datetime

DBFILE = 'sts.db' # sqlite3数据库，全局变量
def get_create_db(db_filename):
    """打开本地数据库文件db_filename，并返回数据库连接con
    如果本地数据库文件db_filename，在创建数据库和UserInfo表"""
    if os.path.exists(db_filename):
        con = sqlite3.connect(db_filename)
    else:
        con = sqlite3.connect(db_filename)
        # 在该数据库下创建Course表
        sql_create_Course = '''CREATE TABLE Course (
    COURSEID     VARCHAR (20)  PRIMARY KEY,
    COURSENAME   VARCHAR (20)  NOT NULL,
    CREDIT       INT,
    DESCRIPTION  VARCHAR (100),
    PUBLISHER_ID VARCHAR (20)  REFERENCES UserInfo (USERID),
    RECEIVER_ID  VARVAHR (20),
    STATE        VARCHAR (20),
    KEY          VARCHAR (20) );'''
        con.execute(sql_create_Course)

        # 在该数据库下创建USERINFO表
        sql_create_userinfo = '''CREATE TABLE UserInfo (
    USERID   VARCHAR (20) PRIMARY KEY,
    USERNAME VARCHAR (20) NOT NULL,
    POINT    INTEGER (6),
    PHONE    VARCHAR (20),
    USERTYPE VARCHAR (4),
    PASSWORD VARCHAR (20) NOT NULL
);
'''
        con.execute(sql_create_userinfo)


        sql_insert_UserInfo = '''INSERT INTO UserInfo VALUES 
                              ('admin','管理员','88888','13912345678','管理','admin');'''
        con.execute(sql_insert_UserInfo)
        con.commit()

        # 在该数据库下创建Items表
        sql_create_ITEMS = '''CREATE TABLE Items (
    ITEMID    VARCHAR (20) PRIMARY KEY,
    ITEMNAME  VARCHAR (20),
    ITEMPOINT INT          NOT NULL,
    INVENTORY INT          NOT NULL
);
'''
        con.execute(sql_create_ITEMS)
        # 在该数据库下创建Items表
        sql_create_GET = '''CREATE TABLE GET (
    ITEMID  VARCHAR (20) REFERENCES Items (ITEMID),
    USERID  VARCHAR (20) REFERENCES UserInfo (USERID),
    GETDATE VARCHAR (50) NOT NULL
);
'''
        con.execute(sql_create_GET)

    return con  # 返回数据库连接

# ——————————————————————————————————————————user
def check_usertype(userid):
    """检查用户类型"""
    con = get_create_db(DBFILE)
    try:
        sql_pattern = '''SELECT USERTYPE FROM UserInfo WHERE USERID="{0}" '''
        sql = sql_pattern.format(userid)
        cur = con.execute(sql)
        row = cur.fetchone()
        if row:
            r = tuple(row)
            return r[0]
        else:
            return False
    finally:
        con.close()

def check_login(userid, password, usertype):
    """检查用户登录信息是否正确"""
    con = get_create_db(DBFILE)
    try:
        sql_pattern = '''SELECT USERNAME FROM UserInfo WHERE USERID="{0}" 
                                    AND PASSWORD="{1}" AND USERTYPE="{2}"'''
        sql = sql_pattern.format(userid, password, usertype)
        cur = con.execute(sql)
        row = cur.fetchone()
        if row:
            r = tuple(row)
            return r[0]
        else:
            return False
    finally:
        con.close()

def change_password(userid, password):
    """修改用户密码"""
    con = get_create_db(DBFILE)
    try:
        sql_pattern = '''UPDATE UserInfo SET PASSWORD="{1}" 
                                 WHERE USERID="{0}"'''
        sql = sql_pattern.format(userid, password)
        con.execute(sql)
        con.commit()
    finally:
        con.close()

def check_point(userid):
    """检查UserInfo中的积分"""
    con = get_create_db(DBFILE)
    try:
        sql_pattern = '''SELECT POINT FROM UserInfo WHERE USERID="{0}"'''
        sql = sql_pattern.format(userid)
        cur = con.execute(sql)
        row = cur.fetchone()
        if row:
            return row[0]  #返回积分
        else:
            return False
    finally:
        con.close()


def check_user_id(userid):
    """检查UserInfo中是否存在userid"""
    con = get_create_db(DBFILE)
    try:
        sql_pattern = '''SELECT USERID, USERNAME FROM UserInfo WHERE USERID="{0}"'''
        sql = sql_pattern.format(userid)
        cur = con.execute(sql)
        row = cur.fetchone()
        if row:
            return row[1]  #返回用户名
        else:
            return False
    finally:
        con.close()

def get_user_list(user_type):
    """查找数据库UserInfo表，获取类型为user_type的用户信息列表"""
    con = get_create_db(DBFILE)
    try:
        sql_pattern = '''SELECT USERID, USERNAME, POINT, PHONE,USERTYPE,PASSWORD
                                      FROM UserInfo 
                                     WHERE USERTYPE="{0}"'''
        sql = sql_pattern.format(user_type)
        results = con.execute(sql)
        users = results.fetchall()
        user_list = []
        for user in users:
            user_list.append(user)
        return user_list
    finally:
        con.close()
# ——————————————————————————————————————————item
def check_item_id(itemid):
    """检查Items中是否存在itemid"""
    con = get_create_db(DBFILE)
    try:
        sql_pattern = '''SELECT ITEMID, ITEMNAME FROM Items WHERE ITEMID="{0}"'''
        sql = sql_pattern.format(itemid)
        cur = con.execute(sql)
        row = cur.fetchone()
        if row:
            return row[0] 
        else:
            return False
    finally:
        con.close()

def get_item_list():
    """查找数据库Items表，获取类用户信息列表"""
    con = get_create_db(DBFILE)
    try:
        sql = '''SELECT ITEMID, ITEMNAME, ITEMPOINT, INVENTORY
                                      FROM Items '''
        results = con.execute(sql)
        items = results.fetchall()
        items_list = []
        for item in items:
            items_list.append(item)
        return items_list
    finally:
        con.close()


def insert_item(itemid, itemname, point, inventory):
    """插入一条记录到Items表"""
    con = get_create_db(DBFILE)
    try:
        sql = '''INSERT INTO Items(ITEMID, ITEMNAME, ITEMPOINT, INVENTORY)
                                      VALUES (?,?,?,?)'''
        con.execute(sql, (itemid, itemname, point, inventory))
        con.commit()
    finally:
        con.close()


def update_item(itemid, itemname, point, inventory):
    """更新一条记录到Items表"""
    con = get_create_db(DBFILE)
    try:
        sql = '''UPDATE Items
                    SET ITEMNAME = ?
                        ,ITEMPOINT = ?
                        ,INVENTORY = ?
                    WHERE ITEMID = ?'''
        con.execute(sql, (itemname, point, inventory,itemid))
        con.commit()
    finally:
        con.close()

def delete_item(itemid):
    """从Items表中删除一条记录"""
    con = get_create_db(DBFILE)
    try:
        sql = '''DELETE FROM Items
                    WHERE ITEMID = ?'''
        con.execute(sql, (itemid, ))
        con.commit()
    finally:
        con.close()

def get_get_list_all():
    """查找数据库GET表，获取类用户信息列表"""
    con = get_create_db(DBFILE)
    try:
        sql = '''SELECT ITEMID, USERID, GETDATE
                                      FROM GET '''
        results = con.execute(sql)
        gets = results.fetchall()
        get_list = []
        for get in gets:
            get_list.append(get)
        return get_list
    finally:
        con.close()

def get_get_list_one(userid):
    """查找数据库GET表，获取类用户信息列表"""
    con = get_create_db(DBFILE)
    try:
        sql = '''SELECT ITEMID, USERID, GETDATE
                                      FROM GET 
                                      WHERE USERID="{0}"'''
        sql=sql.format(userid)
        results = con.execute(sql)
        gets = results.fetchall()
        get_list = []
        for get in gets:
            get_list.append(get)
        return get_list
    finally:
        con.close()

def get_item(itemid, userid,new_point,new_inventory):
    """插入一条记录到GET、 ITEM表"""
    con = get_create_db(DBFILE)
    try:
        sql1 = '''INSERT INTO GET(ITEMID,USERID,GETDATE) VALUES (?,?,?)'''
        sql2 = '''UPDATE UserInfo
                    SET POINT = ?
                    WHERE USERID = ?'''
        sql3 = '''UPDATE Items
                    SET INVENTORY = ?
                    WHERE ITEMID = ?'''
        con.execute(sql1, (itemid, userid, str(datetime.datetime.now())))
        con.execute(sql2, (new_point,userid))
        con.execute(sql3, (new_inventory,itemid))
        con.commit()
    finally:
        con.close()

def inventory_check(itemid):
    """检查item中inventory是否存在>=1"""
    con = get_create_db(DBFILE)
    try:
        sql_pattern = '''SELECT INVENTORY FROM Items WHERE ITEMID="{0}"'''
        sql = sql_pattern.format(itemid)
        cur = con.execute(sql)
        row=cur.fetchone()
        if row:
            return row[0]  #返回库存数
        else:
            return False
    finally:
        con.close()
# ——————————————————————————————————————————user管理
def register(usertype,userid, username, phone,password):
    """插入一条记录到UserInfo表"""
    con = get_create_db(DBFILE)
    try:
        sql = '''INSERT INTO UserInfo(USERID, USERNAME, POINT, PHONE, USERTYPE, PASSWORD)
                                      VALUES (?,?,?,?,?,?)'''
        con.execute(sql, (userid, username, 50, phone, usertype, password))
        con.commit()
    finally:
        con.close()

def insert_info(userid, username, point, phone, usertype, password):
    """插入一条记录到UserInfo表"""
    con = get_create_db(DBFILE)
    try:
        sql = '''INSERT INTO UserInfo(USERID, USERNAME, POINT, PHONE, USERTYPE, PASSWORD)
                                      VALUES (?,?,?,?,?,?)'''
        con.execute(sql, (userid, username, point, phone, usertype, password))
        con.commit()
    finally:
        con.close()


def update_user(userid, username, point, phone,usertype,password):
    """更新一条记录到UserInfo表"""
    con = get_create_db(DBFILE)
    try:
        sql = '''UPDATE UserInfo
                    SET USERNAME = ?
                        ,POINT = ?
                        ,PHONE = ?
                        ,USERTYPE = ?
                        ,PASSWORD = ?
                    WHERE USERID = ?'''
        con.execute(sql, (username, point, phone, usertype, password,userid))
        con.commit()
    finally:
        con.close()

def delete_user(userid):
    """从UserInfo表中删除一条记录"""
    con = get_create_db(DBFILE)
    try:
        sql = '''DELETE FROM UserInfo
                    WHERE USERID = ?'''
        con.execute(sql, (userid, ))
        con.commit()
    finally:
        con.close()

def update_user_point(userid,point):
    """在UserInfo表中更新一个用户的积分"""
    con = get_create_db(DBFILE)
    try:
        sql = '''UPDATE UserInfo
                    SET POINT = {0}
                    WHERE USERID = {1}'''
        sql=sql.format(point,userid)
        con.execute(sql)
        con.commit()
    finally:
        con.close()


############course表管理#########################################################################
def check_course_id(courseid):
    """检查Course表中是否存在courseid"""
    con = get_create_db(DBFILE)
    try:
        sql_pattern = '''SELECT COURSEID, COURSENAME FROM COURSE WHERE COURSEID="{0}"'''
        sql = sql_pattern.format(courseid)
        cur = con.execute(sql)
        row = cur.fetchone()
        if row:
            return row[1] #返回课程名称
        else:
            return False
    finally:
        con.close()

def get_course_list_one():
    """查找数据库Course表，获取任务信息列表"""
    con = get_create_db(DBFILE)
    try:
        sql = '''SELECT COURSEID, COURSENAME, CREDIT, DESCRIPTION,PUBLISHER_ID,RECEIVER_ID,STATE,KEY
                                      FROM Course
                                      WHERE STATE="待接取"'''
        results = con.execute(sql)
        courses = results.fetchall()
        course_list = []
        for course in courses:
            course_list.append(course)
        return course_list
    finally:
        con.close()

def get_course_list_all():
    """查找数据库Course表，获取任务信息列表"""
    con = get_create_db(DBFILE)
    try:
        sql = '''SELECT COURSEID, COURSENAME, CREDIT, DESCRIPTION,PUBLISHER_ID,RECEIVER_ID,STATE,KEY
                                      FROM Course'''
        results = con.execute(sql)
        courses = results.fetchall()
        course_list = []
        for course in courses:
            course_list.append(course)
        return course_list
    finally:
        con.close()

def cancel_course(courseid):
    """完成任务，改变Course表中对应id的状态，同时扣除receiverid对应的积分"""
    con = get_create_db(DBFILE)
    try:
        sql = '''UPDATE COURSE
                 SET STATE = '待接取'
                 WHERE COURSEID = ?; '''
        con.execute(sql,courseid)
        con.commit()
    finally:
        con.close()

def get_courseList_forCanceling(userid):
    """查找数据库Course表和UserInfo表，获取所有自己进行中的任务信息以及发布者的联系方式"""
    con = get_create_db(DBFILE)
    try:
        sql = '''SELECT Course.COURSEID,Course.PUBLISHER_ID, Course.CREDIT, Course.STATE, Course.COURSENAME, Course.DESCRIPTION,UserInfo.PHONE
                                      FROM Course INNER JOIN UserInfo  
                                      ON Course.PUBLISHER_ID=UserInfo.USERID
                                      WHERE Course.STATE ="进行中" and Course.RECEIVER_ID="{0}"'''
        sql=sql.format(userid)
        results = con.execute(sql)
        courses = results.fetchall()
        course_list = []
        for course in courses:
            course_list.append(course)
        return course_list
    finally:
        con.close()


def get_published_course_list(userid):
    """查找数据库Course表，获取某个用户已发布的任务信息列表"""
    con = get_create_db(DBFILE)
    try:
        sql = '''SELECT COURSEID, COURSENAME, CREDIT, DESCRIPTION,PUBLISHER_ID,RECEIVER_ID,STATE,KEY
                                      FROM Course
                                      WHERE PUBLISHER_ID="{0}"'''
        sql=sql.format(userid)
        results = con.execute(sql)
        courses = results.fetchall()
        course_list = []
        for course in courses:
            course_list.append(course)
        return course_list
    finally:
        con.close()

def get_courseList_forTaking(userid):
    """查找数据库Course表和UserInfo表，获取除自己发布的所有待接取的任务信息"""
    con = get_create_db(DBFILE)
    try:
        sql = '''SELECT COURSEID, PUBLISHER_ID, CREDIT, STATE, COURSENAME, DESCRIPTION
                                      FROM Course
                                      WHERE STATE="待接取" and PUBLISHER_ID!={0}'''
        sql=sql.format(userid)
        results = con.execute(sql)
        courses = results.fetchall()
        course_list = []
        for course in courses:
            course_list.append(course)
        return course_list
    finally:
        con.close()

def get_courseList_forCompleting(userid):
    """查找数据库Course表和UserInfo表，获取所有自己进行中的任务信息以及发布者的联系方式"""
    con = get_create_db(DBFILE)
    try:
        sql = '''SELECT Course.COURSEID,Course.PUBLISHER_ID, Course.CREDIT, Course.STATE, Course.COURSENAME, Course.DESCRIPTION,UserInfo.PHONE
                                      FROM Course INNER JOIN UserInfo  
                                      ON Course.PUBLISHER_ID=UserInfo.USERID
                                      WHERE Course.STATE in ("进行中","已完成") and Course.RECEIVER_ID="{0}"'''
        sql=sql.format(userid)
        results = con.execute(sql)
        courses = results.fetchall()
        course_list = []
        for course in courses:
            course_list.append(course)
        return course_list
    finally:
        con.close()

def insert_course(courseid, coursename, credit, description,publisher_id,receiver_id,state, key):
    """插入一条记录到Course表"""
    con = get_create_db(DBFILE)
    try:
        sql = '''INSERT INTO COURSE(COURSEID, COURSENAME, CREDIT,DESCRIPTION,PUBLISHER_ID,RECEIVER_ID,STATE,KEY)
                                      VALUES (?,?,?,?,?,?,?,?)'''
        con.execute(sql, (courseid, coursename, credit, description,publisher_id,receiver_id,state,key))
        con.commit()
    finally:
        con.close()

def update_course(courseid, coursename, credit, description,key):
    """更新一条记录到COURSE表"""
    con = get_create_db(DBFILE)
    try:
        sql = '''UPDATE COURSE
                    SET COURSENAME = ?
                        ,CREDIT = ?
                        ,DESCRIPTION = ?
                        ,KEY= ?
                    WHERE COURSEID = ?'''
        con.execute(sql, (coursename, credit, description, key, courseid))
        con.commit()
    finally:
        con.close()

def delete_course(courseid):
    """从COURSE表中删除一条记录"""
    con = get_create_db(DBFILE)
    try:
        sql = '''DELETE FROM COURSE
                    WHERE COURSEID = ?'''
        con.execute(sql, (courseid, ))
        con.commit()
    finally:
        con.close()

def kill_point(userid,point):
    """发布花费积分"""
    con = get_create_db(DBFILE)
    try:
        sql = '''UPDATE UserInfo
                    SET POINT = ?
                    WHERE USERID = ?'''
        con.execute(sql, (point,userid))
        con.commit()
    finally:
        con.close()

def take_course(courseid, receiver_id):
    """接取任务，改变Course表中对应ID状态、同时将receiver设置成接取者用户ID"""
    con = get_create_db(DBFILE)
    try:
        sql = '''UPDATE COURSE
                    SET STATE = '进行中'
                    ,RECEIVER_ID= ?
                    WHERE COURSEID = ?'''
        con.execute(sql, (receiver_id,courseid))
        con.commit()
    finally:
        con.close()

def complete_course(courseid):
    """完成任务，改变Course表中对应id的状态，同时增加receiverid对应的积分"""
    con = get_create_db(DBFILE)
    try:
        sql = '''UPDATE COURSE
                    SET STATE = '已完成'
                    WHERE COURSEID = {0}; 
                '''
        sql=sql.format(courseid)
        con.execute(sql)
        con.commit()
    finally:
        con.close()

def get_course_key(courseid):
    con = get_create_db(DBFILE)
    try:
        sql = '''SELECT KEY FROM Course
                    WHERE COURSEID = {0}'''
        sql=sql.format(courseid)
        cur=con.execute(sql)
        row=cur.fetchone()
        if row:
            return row[0]
        else:
            return
    finally:
        con.close()

def get_course_state(courseid):
    con = get_create_db(DBFILE)
    try:
        sql = '''SELECT STATE FROM Course
                    WHERE COURSEID = {0}'''
        sql=sql.format(courseid)
        cur=con.execute(sql)
        row=cur.fetchone()
        if row:
            return row[0]
        else:
            return
    finally:
        con.close()
