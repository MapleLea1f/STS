--
-- SQLiteStudio v3.4.4 生成的文件，周四 6月 13 16:00:46 2024
--
-- 所用的文本编码：System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- 表：Course
CREATE TABLE IF NOT EXISTS Course (
                                    COURSEID    VARCHAR (20)  PRIMARY KEY,
                                    COURSENAME  VARCHAR (20)  NOT NULL,
                                    CREDIT      INT,
                                    DESCRIPTION VARCHAR (100),
                                    PUBLISHER_ID    VARCHAR (20)  REFERENCES UserInfo (USERID),
                                    RECEIVER_ID     VARVAHR (20),
                                    STATE           VARCHAR (20),
                                    KEY         VARCHAR (20) );
INSERT INTO Course (COURSEID, COURSENAME, CREDIT, DESCRIPTION, PUBLISHER_ID, RECEIVER_ID, STATE, KEY) VALUES ('1', '帮我送快递1', 100, '6月13日12点', 'ad1', 1, '已完成', '111');
INSERT INTO Course (COURSEID, COURSENAME, CREDIT, DESCRIPTION, PUBLISHER_ID, RECEIVER_ID, STATE, KEY) VALUES ('2', '送你1积分', 1, 'anyone ok', '1', 2, '已完成', '111');
INSERT INTO Course (COURSEID, COURSENAME, CREDIT, DESCRIPTION, PUBLISHER_ID, RECEIVER_ID, STATE, KEY) VALUES ('111', '11', 1, '1', '1', 2, '已完成', '1');

-- 表：GET
CREATE TABLE IF NOT EXISTS GET (ITEMID VARCHAR (20) REFERENCES Items (ITEMID), USERID VARCHAR (20) REFERENCES UserInfo (USERID), GETDATE VARCHAR (50) NOT NULL);
INSERT INTO GET (ITEMID, USERID, GETDATE) VALUES ('1', '1', '2024-06-13 04:01:18.572539');
INSERT INTO GET (ITEMID, USERID, GETDATE) VALUES ('3', '2', '2024-06-13 04:01:18.572539');
INSERT INTO GET (ITEMID, USERID, GETDATE) VALUES ('2', '1', '2024-06-13 04:01:18.572539');

-- 表：Items
CREATE TABLE IF NOT EXISTS Items (ITEMID VARCHAR (20) PRIMARY KEY, ITEMNAME VARCHAR (20), ITEMPOINT INT NOT NULL, INVENTORY INT NOT NULL);
INSERT INTO Items (ITEMID, ITEMNAME, ITEMPOINT, INVENTORY) VALUES ('1', '50元现金', 500, 100);
INSERT INTO Items (ITEMID, ITEMNAME, ITEMPOINT, INVENTORY) VALUES ('2', '精美水瓶500ml', 200, 50);
INSERT INTO Items (ITEMID, ITEMNAME, ITEMPOINT, INVENTORY) VALUES ('3', 'B5笔记本', 100, 50);

-- 表：UserInfo
CREATE TABLE IF NOT EXISTS UserInfo (USERID VARCHAR (20) PRIMARY KEY, USERNAME VARCHAR (20) NOT NULL, POINT INTEGER (6), PHONE VARCHAR (20), USERTYPE VARCHAR (4), PASSWORD VARCHAR (20) NOT NULL);
INSERT INTO UserInfo (USERID, USERNAME, POINT, PHONE, USERTYPE, PASSWORD) VALUES ('admin', '管理员', 66666, '13912345678', '管理', 'admin');
INSERT INTO UserInfo (USERID, USERNAME, POINT, PHONE, USERTYPE, PASSWORD) VALUES ('1', '1号用户', 49, '13471070000', '用户', '1');
INSERT INTO UserInfo (USERID, USERNAME, POINT, PHONE, USERTYPE, PASSWORD) VALUES ('2', '2号用户', 51, '13471072222', '用户', '2');
INSERT INTO UserInfo (USERID, USERNAME, POINT, PHONE, USERTYPE, PASSWORD) VALUES ('ad1', '卢总', 66666, '13471070002', '管理', '123');
INSERT INTO UserInfo (USERID, USERNAME, POINT, PHONE, USERTYPE, PASSWORD) VALUES ('ad2', '盛总', 66666, '13471070001', '管理', '123');

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
