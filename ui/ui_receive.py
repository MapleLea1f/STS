'''接取任务，更改Course表中STATE状态为进行中,修改Course表中RECEIVER_ID为接取者id'''
'''完成任务，填入任务ID、key，调用Course表中的任务ID和key进行验证，验证成功则更改CourseING表中STATE状态为已完成，并给予receiverID用户相应积分'''
from data import data
import wx
from . import ui_main
useridcheck=0
class ReceiveWindow(wx.Frame):
    def __init__(self, parent, title, userid, username,usertype):
        wx.Frame.__init__(self, parent, title=title, size=(800, 600))
        panel = wx.Panel(self, wx.ID_ANY)
        self.CreateStatusBar()  # 创建状态栏
        self.userid = userid
        self.username = username
        self.usertype=usertype
        point=data.check_point(userid)
        self.point=point
        lblListAction = ['接取任务', '完成任务']
        self.rboxAction = wx.RadioBox(panel, label='操作', choices=lblListAction)
        labeltips=wx.StaticText(panel,wx.ID_ANY,'注:发布任务请到主菜单，查看联系方式请划到列表最右方。')
        labeltips.SetForegroundColour(wx.RED)

        self.listCourse = wx.ListCtrl(panel, wx.ID_ANY, size=(630, 400), style=wx.LC_REPORT)
        self.listCourse.InsertColumn(0, '任务ID', width=50)
        self.listCourse.InsertColumn(1, '发布用户', width=80)
        self.listCourse.InsertColumn(2, '积分', width=50)
        self.listCourse.InsertColumn(3, '任务状态',  width=100)
        self.listCourse.InsertColumn(4, '任务名称',  width=200)
        self.listCourse.InsertColumn(5, '要求说明', width=250)
        self.listCourse.InsertColumn(6, '联系方式',  width=150)

        labelCourseID = wx.StaticText(panel, wx.ID_ANY, '任务ＩＤ:')
        self.inputTextCourseID = wx.TextCtrl(panel, wx.ID_ANY, '')
        labelCredit = wx.StaticText(panel, wx.ID_ANY, '任务积分:')
        self.inputTextCredit = wx.TextCtrl(panel, wx.ID_ANY, '',size=(50,-1))
        labelCourseName = wx.StaticText(panel, wx.ID_ANY, '任务名称:')
        self.inputTextCourseName = wx.TextCtrl(panel, wx.ID_ANY, '',size=(250,-1))
        labelDescription = wx.StaticText(panel, wx.ID_ANY, '要求说明:')
        self.inputTextDescription = wx.TextCtrl(panel, wx.ID_ANY, '',size=(250,-1))
        labelKey = wx.StaticText(panel, wx.ID_ANY, '完成密钥:')
        self.inputTextKey = wx.TextCtrl(panel, wx.ID_ANY, '',size=(100,-1))

        self.takeBtn = wx.Button(panel, wx.ID_ANY, '接取')
        self.completeBtn = wx.Button(panel, wx.ID_ANY, '完成')
        self.completeBtn.Disable()
        self.inputTextCourseID.Enable()
        self.inputTextCredit.Disable()
        self.inputTextCourseName.Disable()
        self.inputTextDescription.Disable()
        self.takeBtn.Enable()
        self.inputTextKey.Disable()
        exitBtn = wx.Button(panel, wx.ID_ANY, '返回')

        topSizer = wx.BoxSizer(wx.VERTICAL)
        optionSizer = wx.BoxSizer(wx.HORIZONTAL)
        contentSizer = wx.BoxSizer(wx.HORIZONTAL)
        listSizer = wx.BoxSizer(wx.HORIZONTAL)
        editSizer = wx.BoxSizer(wx.VERTICAL)
        courseidSizer = wx.BoxSizer(wx.HORIZONTAL)
        coursenameSizer = wx.BoxSizer(wx.HORIZONTAL)
        creditSizer = wx.BoxSizer(wx.HORIZONTAL)
        descriptionSizer = wx.BoxSizer(wx.HORIZONTAL)
        keySizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)

        optionSizer.Add(self.rboxAction, 0, wx.ALL, 5)

        listSizer.Add(self.listCourse, 0, wx.ALL, 5)

        optionSizer.Add(labeltips, 0, wx.ALL, 5)
        courseidSizer.Add(labelCourseID, 0, wx.ALL, 5)
        courseidSizer.Add(self.inputTextCourseID, 0, wx.ALL, 5)
        coursenameSizer.Add(labelCourseName, 0, wx.ALL, 5)
        coursenameSizer.Add(self.inputTextCourseName, 0, wx.ALL, 5)
        creditSizer.Add(labelCredit, 0, wx.ALL, 5)
        creditSizer.Add(self.inputTextCredit, 0, wx.ALL, 5)
        descriptionSizer.Add(labelDescription, 0, wx.ALL, 5)
        descriptionSizer.Add(self.inputTextDescription, 0, wx.ALL, 5)
        keySizer.Add(labelKey, 0, wx.ALL, 5)
        keySizer.Add(self.inputTextKey, 0, wx.ALL, 5)
        btnSizer.Add(self.takeBtn, 0, wx.ALL, 5)
        btnSizer.Add(self.completeBtn, 0, wx.ALL, 5)
        btnSizer.Add(exitBtn, 0, wx.ALL, 5)

        editSizer.Add(courseidSizer, 0, wx.ALL, 5)
        editSizer.Add(creditSizer, 0, wx.ALL, 5)
        editSizer.Add(coursenameSizer, 0, wx.ALL, 5)
        editSizer.Add(descriptionSizer, 0, wx.ALL, 5)
        editSizer.Add(keySizer, 0, wx.ALL, 5)
        editSizer.Add(btnSizer, 0, wx.ALL, 5)

        contentSizer.Add(listSizer, 0, wx.ALL, 5)
        contentSizer.Add(editSizer, 0, wx.ALL, 5)

        topSizer.Add(optionSizer, 0, wx.ALL | wx.CENTER, 5)
        topSizer.Add(contentSizer, 0, wx.ALL | wx.CENTER, 5)

        panel.SetSizer(topSizer)
        topSizer.Fit(self)
        
        #绑定事件.
        self.Bind(wx.EVT_RADIOBOX, self.onAction, self.rboxAction)
        self.Bind(wx.EVT_LIST_ITEM_FOCUSED, self.onAction, self.listCourse)
        self.Bind(wx.EVT_LIST_ITEM_FOCUSED, self.onCourseList, self.listCourse)
        self.Bind(wx.EVT_BUTTON, self.onTake, self.takeBtn)
        self.Bind(wx.EVT_BUTTON, self.onComplete, self.completeBtn)
        self.Bind(wx.EVT_BUTTON, self.OnPoint, exitBtn)
        self.populate_courseList_forTaking()

    def OnPoint(self, e):
        self.Close(True)
        title = "大学生校内悬赏任务大厅(登录： {0} / {1} / {2} / 当前积分为：{3} )".format(self.userid, self.username, self.usertype,data.check_point(self.userid))
        mainFrame = ui_main.MainWindow(None, title, self.userid, self.username, self.usertype)
        mainFrame.Show() #显示主窗口
        mainFrame.Center()  #窗口居中

#——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————原main，下面加入ui_teacher部分
    def populate_courseList_forTaking(self):
        """查询待接取任务的信息并显示"""
        course_list = data.get_courseList_forTaking(self.userid)
        self.listCourse.DeleteAllItems()
        index = 0
        for course in course_list:
            self.listCourse.InsertItem(index, course[0])
            self.listCourse.SetItem(index, 1, course[1])
            self.listCourse.SetItem(index, 2, str(course[2]))
            self.listCourse.SetItem(index, 3, course[3])
            self.listCourse.SetItem(index, 4, course[4])
            self.listCourse.SetItem(index, 5, course[5])
            self.listCourse.SetItem(index, 6, "已隐藏")
            index += 1

    def populate_courseList_forCompleting(self):
        """查询待完成任务的信息并显示"""
        course_list = data.get_courseList_forCompleting(self.userid)
        self.listCourse.DeleteAllItems()
        index = 0
        for course in course_list:
            self.listCourse.InsertItem(index, course[0])
            self.listCourse.SetItem(index, 1, course[1])
            self.listCourse.SetItem(index, 2, str(course[2]))
            self.listCourse.SetItem(index, 3, course[3])
            self.listCourse.SetItem(index, 4, course[4])
            self.listCourse.SetItem(index, 5, course[5])
            self.listCourse.SetItem(index, 6, course[6])
            index += 1

    def onAction(self, e):
        """事情处理函数：根据操作类型（接取任务、完成任务）设置不同控件的状态"""
        action = self.rboxAction.GetStringSelection()
        if action == "接取任务":
            
            self.inputTextCourseID.Enable()
            self.inputTextCredit.Disable()
            self.inputTextCourseName.Disable()
            self.inputTextDescription.Disable()
            self.takeBtn.Enable()
            self.inputTextKey.Disable()
            self.completeBtn.Disable()
            self.populate_courseList_forTaking()


        elif action == "完成任务":
            
            self.inputTextCourseID.Enable()
            self.inputTextCredit.Disable()
            self.inputTextCourseName.Disable()
            self.inputTextDescription.Disable()
            self.inputTextKey.Enable()
            self.takeBtn.Disable()
            self.completeBtn.Enable()         
            self.rboxAction.SetSelection(1)
            self.populate_courseList_forCompleting()
    

        

    def onCourseList(self,e):
        """事件处理函数：在列表中选择任务，内容显示在右侧"""
        global useridcheck
        index = e.GetIndex() #获得被激活表项的索引号
        self.inputTextCourseID.SetValue(self.listCourse.GetItem(index, 0).GetText())
        self.inputTextCourseName.SetValue(self.listCourse.GetItem(index, 4).GetText())
        self.inputTextCredit.SetValue(self.listCourse.GetItem(index, 2).GetText())
        self.inputTextDescription.SetValue(self.listCourse.GetItem(index, 5).GetText())
        useridcheck=self.listCourse.GetItem(index, 1).GetText()
        return useridcheck


    def onTake(self,e):
        """事件处理函数：接取任务"""
        courseid = self.inputTextCourseID.GetValue()
        if len(courseid.strip()) == 0:
            wx.MessageBox('请选中您要接取的任务！')

        if bool(data.check_course_id(courseid)) and data.get_course_state(courseid)=='待接取':
            data.take_course(courseid,receiver_id=self.userid)
            wx.MessageBox('任务接取成功！请到完成任务页面查看联系方式。')
            
        #初始化界面
        self.refresh_screen()
        self.populate_courseList_forTaking()


    def refresh_screen(self):
        self.inputTextCourseID.SetValue('')
        self.inputTextCourseName.SetValue('')
        self.inputTextCredit.SetValue('')
        self.inputTextDescription.SetValue('')
        self.Close(True)  # 关闭窗口
        self.OnPoint(None)
        

    def onComplete(self, e):
        """事件处理函数：完成任务"""
        courseid = self.inputTextCourseID.GetValue()
        credit = int(self.inputTextCredit.GetValue())
        key=self.inputTextKey.GetValue()
        if len(courseid.strip()) == 0:
            wx.MessageBox('请输入任务ID！')
            self.inputTextCourseID.SetFocus()
            return None
        
        if len(key.strip()) == 0:
            wx.MessageBox('请输入密钥确认完成任务！')
            self.inputTextKey.SetFocus()
            return None
        #更新记录
        if key==data.get_course_key(courseid) and data.get_course_state(courseid)=="进行中":
            data.complete_course(courseid)
            data.update_user_point(self.userid,int(self.point)+credit)
            wx.MessageBox('您的任务已完成！积分增加{0}，现在的积分数为{1}。'.format(credit,int(self.point)+credit))
        else:
            wx.MessageBox('任务ID或密钥输入错误！')
            
        #初始化界面
        self.refresh_screen()
        self.populate_courseList_forCompleting()

