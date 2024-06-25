import wx
from . import ui_login
from . import ui_change_password
from . import ui_user
from . import ui_courseED
from . import ui_receive
from . import ui_cancel
from . import ui_prize
from . import ui_prizemanage
from . import ui_checkprize
from data import data

useridcheck=0

class MainWindow(wx.Frame):
    def __init__(self, parent, title, userid, username, usertype):
        wx.Frame.__init__(self, parent, title=title, size=(800, 600))
        panel = wx.Panel(self, wx.ID_ANY)
        self.CreateStatusBar()  # 创建状态栏
        self.userid = userid
        self.username = username
        self.usertype = usertype
        point=data.check_point(userid)
        self.point=point
        title = "大学生校内悬赏任务大厅(登录： {0} / {1} / {2} / 当前积分为：{3} )".format(userid, username, usertype,point)
        # 创建菜单并添加菜单项
        sysmenu = wx.Menu() #系统：登录、修改密码、退出
        a_menu = wx.Menu() #管理菜单：用户管理、兑换管理
        u_menu = wx.Menu()  # 用户菜单：接取/完成任务、已发布任务、兑换奖励
        helpmenu = wx.Menu() #帮助菜单：关于
        # wx.ID_OPEN、wx.ID_SAVE、x.ID_ABOUT、wx.ID_EXIT是标准菜单ID.
        menuPoint = sysmenu.Append(wx.ID_ANY,"刷新积分","刷新积分")
        menuLogin = sysmenu.Append(wx.ID_ANY, "重新登录", "重新登录")
        menuChangePassword = sysmenu.Append(wx.ID_ANY, "修改密码", "修改密码")
        menuExit = sysmenu.Append(wx.ID_EXIT, "退出系统", "退出")

        menuUser = a_menu.Append(wx.ID_ANY, "用户管理", "用户管理")
        menuPrizemanage = a_menu.Append(wx.ID_ANY, "兑换管理", "兑换管理")
        menuPrizecheck = a_menu.Append(wx.ID_ANY, "兑奖记录", "兑奖记录")

        menureceive = u_menu.Append(wx.ID_ANY, "接取/完成任务", "接取/完成任务")
        menucancel = u_menu.Append(wx.ID_ANY, "放弃任务", "放弃任务")
        menucourseED = u_menu.Append(wx.ID_ANY, "已发布任务", "已发布任务")
        menuprize = u_menu.Append(wx.ID_ANY, "兑换奖励", "兑换奖励")
        menuPrizecheck2 = u_menu.Append(wx.ID_ANY, "兑奖记录", "兑奖记录")

        menuAbout = helpmenu.Append(wx.ID_ABOUT, "关于", "关于")

        # 创建菜单栏，根据不同角色，显示不同菜单
        menuBar = wx.MenuBar()
        menuBar.Append(sysmenu, "系统") 
        if self.usertype == "管理":
            menuBar.Append(a_menu, "管理菜单")  
        elif self.usertype == "用户":
            menuBar.Append(u_menu, "用户菜单")  
        menuBar.Append(helpmenu, "帮助") 
        self.SetMenuBar(menuBar)  # 把菜单栏添加到顶层框架窗口

        # 绑定事件.
        self.Bind(wx.EVT_MENU, self.OnPoint, menuPoint)
        self.Bind(wx.EVT_MENU, self.OnLogin, menuLogin)
        self.Bind(wx.EVT_MENU, self.OnChangePassword , menuChangePassword )
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

        self.Bind(wx.EVT_MENU, self.OnUser, menuUser)
        self.Bind(wx.EVT_MENU, self.OnPrizemanage, menuPrizemanage)
        self.Bind(wx.EVT_MENU, self.OnPrizecheck, menuPrizecheck)
        self.Bind(wx.EVT_MENU, self.OnPrizecheck, menuPrizecheck2)

        self.Bind(wx.EVT_MENU, self.Onreceive, menureceive)
        self.Bind(wx.EVT_MENU, self.Oncancel, menucancel)
        self.Bind(wx.EVT_MENU, self.OncourseED, menucourseED)
        self.Bind(wx.EVT_MENU, self.Onprize, menuprize)

        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
#——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————原main，下面加入ui_teacher部分
        #创建控件

        lblListAction = ['发布', '修改', '删除']
        self.rboxAction = wx.RadioBox(panel, label='操作', choices=lblListAction)
        labeltips=wx.StaticText(panel,wx.ID_ANY,'注:请牢记完成密钥，接取任务请到用户菜单,\n只有管理员和本人能进行修改、删除操作,\n发布后若删除任务，且无人接取，可返还积分(修改积分不返还)')
        labeltips.SetForegroundColour(wx.RED)

        self.listCourse = wx.ListCtrl(panel, wx.ID_ANY, size=(630, 400), style=wx.LC_REPORT)
        self.listCourse.InsertColumn(0, '任务ID', width=50)
        self.listCourse.InsertColumn(1, '发布用户', width=80)
        self.listCourse.InsertColumn(2, '积分', width=50)
        self.listCourse.InsertColumn(3, '任务内容',  width=200)
        self.listCourse.InsertColumn(4, '要求说明', width=250)

        labelCourseID = wx.StaticText(panel, wx.ID_ANY, '任务ＩＤ:')
        self.inputTextCourseID = wx.TextCtrl(panel, wx.ID_ANY, '')
        labelCredit = wx.StaticText(panel, wx.ID_ANY, '任务积分:')
        self.inputTextCredit = wx.TextCtrl(panel, wx.ID_ANY, '',size=(50,-1))
        labelCourseName = wx.StaticText(panel, wx.ID_ANY, '任务名称:')
        self.inputTextCourseName = wx.TextCtrl(panel, wx.ID_ANY, '',size=(250,-1))
        labelDescription = wx.StaticText(panel, wx.ID_ANY, '要求说明:')
        self.inputTextDescription = wx.TextCtrl(panel, wx.ID_ANY, '',size=(250,-1))
        labelKey = wx.StaticText(panel, wx.ID_ANY, '完成密钥:')
        self.inputTextKey = wx.TextCtrl(panel, wx.ID_ANY, '',size=(100,-1),style=wx.TE_PASSWORD)

        self.insertBtn = wx.Button(panel, wx.ID_ANY, '发布')
        self.updateBtn = wx.Button(panel, wx.ID_ANY, '修改')
        self.updateBtn.Disable()
        self.deleteBtn = wx.Button(panel, wx.ID_ANY, '删除')
        self.deleteBtn.Disable()
        exitBtn = wx.Button(panel, wx.ID_ANY, '退出')

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
        btnSizer.Add(self.insertBtn, 0, wx.ALL, 5)
        btnSizer.Add(self.updateBtn, 0, wx.ALL, 5)
        btnSizer.Add(self.deleteBtn, 0, wx.ALL, 5)
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
        self.Bind(wx.EVT_BUTTON, self.onInsert, self.insertBtn)
        self.Bind(wx.EVT_BUTTON, self.onUpdate, self.updateBtn)
        self.Bind(wx.EVT_BUTTON, self.onDelete, self.deleteBtn)
        self.Bind(wx.EVT_BUTTON, self.onExit, exitBtn)

        #查询任务信息并显示
        self.populate_course_list()
#——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    def OnAbout(self,e):
        """事件处理函数：显示消息对话框"""
        dlg = wx.MessageDialog( self, "大学生校内悬赏任务大厅V1.0.0\nby 卢江涛、盛禹枫", "大学生校内悬赏任务大厅", wx.OK)
        dlg.ShowModal() # 显示模式对话框
        dlg.Destroy() # 销毁对话框

    def OnExit(self,e):
        self.Close(True)  # 关闭窗口

    def OnLogin(self, e):
        """ 事件处理函数：重新登录 """
        self.Close(True)  # 关闭窗口
        loginFrame = ui_login.LoginWindow(parent=None, title='重新登录')
        loginFrame.Show()  # 显示登录窗口
        loginFrame.Center()  # 窗口居中

    def OnChangePassword(self, e):
        """ 事件处理函数：保存文件 """
        changepasswordFrame = ui_change_password.ChangePasswordWindow(parent=None, title='修改密码')
        changepasswordFrame.Show()  # 显示登录窗口
        changepasswordFrame.Center()  # 窗口居中
        changepasswordFrame.userid  =  self.userid

    def OnUser(self, e):
        """ 事件处理函数：用户管理 """
        userFrame = ui_user.UserWindow(parent=None, title='用户管理')
        userFrame.Show()  # 显示登录窗口
        userFrame.Center()  # 窗口居中

    def OnPrizemanage(self, e):
        """ 事件处理函数：奖品管理 """
        prizemanageFrame = ui_prizemanage.ManageWindow(parent=None, title='兑换管理')
        prizemanageFrame.Show()  # 显示登录窗口
        prizemanageFrame.Center()  # 窗口居中
    
    def OnPrizecheck(self, e):
        """ 事件处理函数：兑奖记录 """
        title="兑奖记录"
        prizecheckFrame = ui_checkprize.checkPrizeWindow(None, title,userid=self.userid,usertype=self.usertype)
        prizecheckFrame.Show()  # 显示登录窗口
        prizecheckFrame.Center()  # 窗口居中

    def Onreceive(self, e):
        """ 事件处理函数：接取/完成任务 """
        receiveFrame = ui_receive.ReceiveWindow(parent=None, title='接取/完成任务',userid=self.userid, username=self.username,usertype=self.usertype)
        self.Close(True)
        receiveFrame.Show()  # 显示登录窗口
        receiveFrame.Center()  # 窗口居中

    def Oncancel(self, e):
        """ 事件处理函数：放弃任务 """
        cancelFrame = ui_cancel.CancelWindow(parent=None, title='放弃任务',userid=self.userid, username=self.username,usertype=self.usertype)
        self.Close(True)
        cancelFrame.Show()  # 显示登录窗口
        cancelFrame.Center()  # 窗口居中
    
    def OncourseED(self, e):
        """ 事件处理函数：已发布任务” """
        courseEDFrame = ui_courseED.EdWindow(parent=None, title='已发布任务',userid=self.userid,username=self.username)
        courseEDFrame.Show()  # 显示登录窗口
        courseEDFrame.Center()  # 窗口居中


    def Onprize(self, e):
        """ 事件处理函数：兑换奖励 """
        title='兑换奖励(当前积分为:{})'.format(data.check_point(self.userid))
        prizeFrame = ui_prize.PrizeWindow(None, title,userid=self.userid,point=self.point,usertype=self.usertype,username=self.username)
        self.Close(True)
        prizeFrame.Show()  # 显示登录窗口
        prizeFrame.Center()  # 窗口居中

    def OnPoint(self, e):
        self.Close(True)
        title = "大学生校内悬赏任务大厅(登录： {0} / {1} / {2} / 当前积分为：{3} )".format(self.userid, self.username, self.usertype,data.check_point(self.userid))
        mainFrame = MainWindow(None, title, self.userid, self.username, self.usertype)
        mainFrame.Show() #显示主窗口
        mainFrame.Center()  #窗口居中

#——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————原main，下面加入ui_teacher部分
    def populate_course_list(self):
        """查询任务表信息并显示"""
        if self.usertype=="用户":
            course_list = data.get_course_list_one()
        if self.usertype=="管理":
            course_list = data.get_course_list_all()
    
        self.listCourse.DeleteAllItems()
        index = 0
        for course in course_list:
            self.listCourse.InsertItem(index, course[0])
            self.listCourse.SetItem(index, 1, course[4])
            self.listCourse.SetItem(index, 2, str(course[2]))
            self.listCourse.SetItem(index, 3, course[1])
            self.listCourse.SetItem(index, 4, course[3])
            index += 1


    def onAction(self, e):
        """事情处理函数：根据操作类型（发布、修改、删除）设置不同控件的状态"""
        action = self.rboxAction.GetStringSelection()
        if action == "发布":
            self.inputTextCourseID.Enable()
            self.inputTextCredit.Enable()
            self.inputTextCourseName.Enable()
            self.inputTextDescription.Enable()
            self.inputTextKey.Enable()
            self.insertBtn.Enable()
            self.updateBtn.Disable()
            self.deleteBtn.Disable()

        elif action == "修改":
            if self.usertype=="管理" or self.userid==useridcheck:
                self.inputTextCourseID.Disable()
                self.inputTextCredit.Disable()
                self.inputTextCourseName.Enable()
                self.inputTextDescription.Enable()
                self.inputTextKey.Enable()
                self.insertBtn.Disable()
                self.updateBtn.Enable()
                self.deleteBtn.Disable()
            else:
                wx.MessageBox('只有管理员和发布者才能修改，管理员修改无需密钥')
                self.rboxAction.SetSelection(0)
        elif action == "删除":
            if self.usertype=="管理" or self.userid==useridcheck:
                self.inputTextCourseID.Disable()
                self.inputTextCredit.Disable()
                self.inputTextCourseName.Disable()
                self.inputTextDescription.Disable()
                self.inputTextKey.Disable()
                self.insertBtn.Disable()
                self.updateBtn.Disable()
                self.deleteBtn.Enable()
    
            else:
                wx.MessageBox('只有管理员和发布者才能修改')
                self.rboxAction.SetSelection(0)
        

    def onCourseList(self,e):
        """事件处理函数：在列表中选择任务，将内容显示在右侧"""
        global useridcheck
        index = e.GetIndex() #获得被激活表项的索引号
        self.inputTextCourseID.SetValue(self.listCourse.GetItem(index, 0).GetText())
        self.inputTextCourseName.SetValue(self.listCourse.GetItem(index, 3).GetText())
        self.inputTextCredit.SetValue(self.listCourse.GetItem(index, 2).GetText())
        self.inputTextDescription.SetValue(self.listCourse.GetItem(index, 4).GetText())
        useridcheck=self.listCourse.GetItem(index, 1).GetText()
        return useridcheck


    def onInsert(self,e):
        """事件处理函数：发布一条任务"""
        courseid = self.inputTextCourseID.GetValue()
        coursename = self.inputTextCourseName.GetValue()
        credit = self.inputTextCredit.GetValue()
        description = self.inputTextDescription.GetValue()
        key=self.inputTextKey.GetValue()
        userid=self.userid
        if len(str(courseid).strip()) == 0:
            wx.MessageBox('请输入任务ID！')
            self.inputTextCourseID.SetFocus()
            return None
        
        if len(credit.strip()) == 0:
            wx.MessageBox('请输入任务积分！')
            self.inputTextCredit.SetFocus()
            return None
        
        if len(str(coursename).strip()) == 0:
            wx.MessageBox('请输入任务名称！')
            self.inputTextCourseName.SetFocus()
            return None
        if len(str(description).strip()) == 0:
            wx.MessageBox('请输入要求说明！')
            self.inputTextDescription.SetFocus()
            return None
        
        if len(str(key).strip()) == 0:
            wx.MessageBox('请输入完成密钥！')
            self.inputTextKey.SetFocus()
            return None
        
        if data.check_course_id(courseid):
            wx.MessageBox("该任务已经存在！")
            self.inputTextCourseID.SetFocus()
            return None
        if self.point-int(credit)<=0:
            wx.MessageBox("积分不足！")
        else:
            wx.MessageBox("发布成功！")
            data.insert_course(courseid, coursename, credit, description,publisher_id=userid,receiver_id=None,state='待接取',key=key)
            data.kill_point(userid=self.userid,point=self.point-int(credit))
            
        #初始化界面
        self.refresh_screen()


    def refresh_screen(self):
        self.inputTextCourseID.SetValue('')
        self.inputTextCourseName.SetValue('')
        self.inputTextCredit.SetValue('')
        self.inputTextDescription.SetValue('')
        self.Close(True)  # 关闭窗口
        self.OnPoint(None)
        # 查询课程信息并显示
        self.populate_course_list()

    def onUpdate(self, e):
        """事件处理函数：修改一条任务"""
        courseid = self.inputTextCourseID.GetValue()
        coursename = self.inputTextCourseName.GetValue()
        credit = int(self.inputTextCredit.GetValue())
        description = self.inputTextDescription.GetValue()
        key=self.inputTextKey.GetValue()
        if len(str(coursename).strip()) == 0:
            wx.MessageBox('请输入任务名称！')
            self.inputTextCourseName.SetFocus()
            return None
        
        if len(str(description).strip()) == 0:
            wx.MessageBox('请输入要求说明！')
            self.inputTextDescription.SetFocus()
            return None
        
        if len(str(key).strip()) == 0 and self.usertype!="管理" :
            wx.MessageBox('请输入完成密钥！')
            self.inputTextKey.SetFocus()
            return None
        
        if self.point-int(credit)<=0:
            wx.MessageBox("积分不足！")
        #更新记录
        if self.usertype!="管理" and self.userid!=useridcheck:
            wx.MessageBox('只有管理员和发布者才能修改')
            self.rboxAction.SetSelection(0)
        else:
            wx.MessageBox('修改成功')
            data.update_course(courseid, coursename, credit, description,key)
        #初始化界面
        self.refresh_screen()

    def onDelete(self, e):
        """事件处理函数：删除一条"""
        courseid = self.inputTextCourseID.GetValue()
        credit = int(self.inputTextCredit.GetValue())
        #删除记录
        if self.usertype!="管理" and self.userid!=useridcheck:
            wx.MessageBox('只有管理员和发布者才能删除')
            self.rboxAction.SetSelection(0)
        else:
            wx.MessageBox('删除成功，积分已返还！')
            data.delete_course(courseid)
            data.kill_point(userid=self.userid,point=self.point+int(credit))
        #初始化界面
        self.refresh_screen()

    def onExit(self,e):
        self.Close(True)  # 关闭顶层框架窗口
