from data import data
import wx

user_type=0

class UserWindow(wx.Dialog):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(800, 600))
        panel = wx.Panel(self, wx.ID_ANY)
        global user_type
        #创建控件
        lblListAction = ['插入', '修改', '删除']
        self.rboxAction = wx.RadioBox(panel, label='操作', choices=lblListAction)
        lblListType = ['用户', '管理']
        self.rboxUserType = wx.RadioBox(panel, label='角色', choices=lblListType)
        user_type=self.rboxUserType.GetStringSelection()

        self.listUser = wx.ListCtrl(panel, wx.ID_ANY, size=(600, 400), style=wx.LC_REPORT)
        self.listUser.InsertColumn(0, '用户ID', width=100)
        self.listUser.InsertColumn(1, '用户名',  width=100)
        self.listUser.InsertColumn(2, '积分', width=50)
        self.listUser.InsertColumn(3, '电话', width=150)
        self.listUser.InsertColumn(4, '用户类型', width=100)
        self.listUser.InsertColumn(5, '密码', width=150)

        labelUserID = wx.StaticText(panel, wx.ID_ANY, '用户ID:')
        self.inputTextUserID = wx.TextCtrl(panel, wx.ID_ANY, '')
        labelUserName = wx.StaticText(panel, wx.ID_ANY, '用户名:')
        self.inputTextUserName = wx.TextCtrl(panel, wx.ID_ANY, '')
        labelPassword = wx.StaticText(panel, wx.ID_ANY, '密码:')
        self.inputTextPassword = wx.TextCtrl(panel, wx.ID_ANY, '')
        labelPoint = wx.StaticText(panel, wx.ID_ANY, '积分:')
        self.inputTextUserPoint = wx.TextCtrl(panel, wx.ID_ANY, '')
        labelPhone = wx.StaticText(panel, wx.ID_ANY, '电话:')
        self.inputTextPhone = wx.TextCtrl(panel, wx.ID_ANY, '')


        self.insertBtn = wx.Button(panel, wx.ID_ANY, '插入')
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
        useridSizer = wx.BoxSizer(wx.HORIZONTAL)
        usernameSizer = wx.BoxSizer(wx.HORIZONTAL)
        passwordSizer=wx.BoxSizer(wx.HORIZONTAL)

        phoneSizer = wx.BoxSizer(wx.HORIZONTAL)
        pointSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)

        optionSizer.Add(self.rboxAction, 0, wx.ALL, 5)
        optionSizer.Add(self.rboxUserType, 0, wx.ALL, 5)

        listSizer.Add(self.listUser, 0, wx.ALL, 5)

        useridSizer.Add(labelUserID, 0, wx.ALL, 5)
        useridSizer.Add(self.inputTextUserID, 0, wx.ALL, 5)
        usernameSizer.Add(labelUserName, 0, wx.ALL, 5)
        usernameSizer.Add(self.inputTextUserName, 0, wx.ALL, 5)
        passwordSizer.Add(labelPassword, 0, wx.ALL, 5)
        passwordSizer.Add(self.inputTextPassword, 0, wx.ALL, 5)
        pointSizer.Add(labelPoint, 0, wx.ALL, 5)
        pointSizer.Add(self.inputTextUserPoint, 0, wx.ALL, 5)
        phoneSizer.Add(labelPhone, 0, wx.ALL, 5)
        phoneSizer.Add(self.inputTextPhone, 0, wx.ALL, 5)

        btnSizer.Add(self.insertBtn, 0, wx.ALL, 5)
        btnSizer.Add(self.updateBtn, 0, wx.ALL, 5)
        btnSizer.Add(self.deleteBtn, 0, wx.ALL, 5)
        btnSizer.Add(exitBtn, 0, wx.ALL, 5)

        editSizer.Add(useridSizer, 0, wx.ALL, 5)
        editSizer.Add(usernameSizer, 0, wx.ALL, 5)
        editSizer.Add(passwordSizer, 0, wx.ALL, 5)
        editSizer.Add(pointSizer, 0, wx.ALL, 5)
        editSizer.Add(phoneSizer, 0, wx.ALL, 5)
        editSizer.Add(btnSizer, 0, wx.ALL, 5)

        contentSizer.Add(listSizer, 0, wx.ALL, 5)
        contentSizer.Add(editSizer, 0, wx.ALL, 5)

        topSizer.Add(optionSizer, 0, wx.ALL | wx.CENTER, 5)
        topSizer.Add(contentSizer, 0, wx.ALL | wx.CENTER, 5)

        panel.SetSizer(topSizer)
        topSizer.Fit(self)

        #绑定事件.
        self.Bind(wx.EVT_RADIOBOX, self.onAction, self.rboxAction)
        self.Bind(wx.EVT_RADIOBOX, self.onUserType, self.rboxUserType)
        self.Bind(wx.EVT_LIST_ITEM_FOCUSED, self.onUserList, self.listUser)
        self.Bind(wx.EVT_BUTTON, self.onInsert, self.insertBtn)
        self.Bind(wx.EVT_BUTTON, self.onUpdate, self.updateBtn)
        self.Bind(wx.EVT_BUTTON, self.onDelete, self.deleteBtn)
        self.Bind(wx.EVT_BUTTON, self.onExit, exitBtn)

        #查询用户信息并显示
        self.populate_user_list()

    def populate_user_list(self):
        """查询用户信息并显示"""
        user_type = self.rboxUserType.GetStringSelection()
        user_list = data.get_user_list(user_type)
        self.listUser.DeleteAllItems()
        index = 0
        for user in user_list:
            self.listUser.InsertItem(index, user[0])
            self.listUser.SetItem(index, 1, user[1])
            self.listUser.SetItem(index, 2, str(user[2]))
            self.listUser.SetItem(index, 3, user[3])
            self.listUser.SetItem(index, 4, user[4])
            self.listUser.SetItem(index, 5, user[5])
            index += 1

    def onAction(self, e):
        """事情处理函数：根据操作类型（插入、修改、删除）设置不同控件的状态"""
        action = self.rboxAction.GetStringSelection()
        if action == "插入":
            self.rboxUserType.Enable()
            self.inputTextUserID.Enable()
            self.insertBtn.Enable()
            self.updateBtn.Disable()
            self.deleteBtn.Disable()
        elif action == "修改":
            self.rboxUserType.Disable()
            self.inputTextUserID.Disable()
            self.insertBtn.Disable()
            self.updateBtn.Enable()
            self.deleteBtn.Disable()
        elif action == "删除":
            self.rboxUserType.Disable()
            self.inputTextUserID.Disable()
            self.insertBtn.Disable()
            self.updateBtn.Disable()
            self.deleteBtn.Enable()

    def onUserType(self, e):
        """事件处理函数：用户类别改变时，显示对应的用户信息列表"""
        global user_type
        user_type=self.rboxUserType.GetStringSelection()
        self.populate_user_list()

    def onUserList(self,e):
        """事件处理函数：在列表中选择用户，内容显示在右侧"""
        index = e.GetIndex() #获得被激活表项的索引号
        self.inputTextUserID.SetValue(self.listUser.GetItem(index, 0).GetText())
        self.inputTextUserName.SetValue(self.listUser.GetItem(index, 1).GetText())
        self.inputTextUserPoint.SetValue(self.listUser.GetItem(index, 2).GetText())
        self.inputTextPhone.SetValue(self.listUser.GetItem(index, 3).GetText())
        self.inputTextPassword.SetValue(self.listUser.GetItem(index, 5).GetText())
        

    def onInsert(self,e):
        """事件处理函数：插入一条记录"""
        user_type = self.rboxUserType.GetStringSelection()
        userid = self.inputTextUserID.GetValue()
        username = self.inputTextUserName.GetValue()
        point = self.inputTextUserPoint.GetValue()
        phone = self.inputTextPhone.GetValue()
        password = self.inputTextPassword.GetValue()
        if len(userid.strip()) == 0:
            wx.MessageBox('请输入用户ID！')
            self.inputTextUserID.SetFocus()
            return None
        if len(username.strip()) == 0:
            wx.MessageBox('请输入用户名！')
            self.inputTextUserName.SetFocus()
            return None
        
        if len(password.strip()) == 0:
            wx.MessageBox('请输入密码！')
            self.inputTextPassword.SetFocus()
            return None       
        
        if len(point.strip()) == 0:
            wx.MessageBox('请输入积分（整数）！')
            self.inputTextUserPoint.SetFocus()
            return None
        
        if len(phone.strip()) == 0:
            wx.MessageBox('请输入电话！')
            self.inputTextPhone.SetFocus()
            return None    
        
        if data.check_user_id(userid):
            wx.MessageBox("该用户已经存在！")
            self.inputTextUserID.SetFocus()
            return None
        #插入记录
        else:
            data.insert_info(userid, username, point, phone, user_type, password)
            wx.MessageBox("插入成功！")
        
        #初始化界面
        self.refresh_screen()


    def refresh_screen(self):
        """重新刷新界面"""
        self.inputTextUserID.SetValue('')
        self.inputTextUserName.SetValue('')
        self.inputTextPassword.SetValue('')
        self.inputTextUserPoint.SetValue('')
        self.inputTextPhone.SetValue('')
        # 查询用户信息并显示
        self.populate_user_list()

    def onUpdate(self, e):
        """事件处理函数：更新一条记录"""
        userid = self.inputTextUserID.GetValue()
        username = self.inputTextUserName.GetValue()
        password = self.inputTextPassword.GetValue()
        point = self.inputTextUserPoint.GetValue()
        phone = self.inputTextPhone.GetValue()

        if len(username.strip()) == 0:
            wx.MessageBox('请输入用户名！')
            self.inputTextUserName.SetFocus()

        if len(password.strip()) == 0:
            wx.MessageBox('请输入密码！')
            self.inputTextPassword.SetFocus()
            return None          

        if len(point.strip()) == 0:
            wx.MessageBox('请输入积分（整数）！')
            self.inputTextUserPoint.SetFocus()
            return None
        
        if len(phone.strip()) == 0:
            wx.MessageBox('请输入电话！')
            self.inputTextPhone.SetFocus()
            return None    
        
        else:
        #更新记录
            data.update_user(userid, username, point, phone,user_type,password)
            wx.MessageBox("修改成功！")
        #初始化界面
        self.refresh_screen()

    def onDelete(self, e):
        
        """事件处理函数：删除一条记录"""
        userid = self.inputTextUserID.GetValue()
        if len(userid.strip()) == 0:
            wx.MessageBox('请选择一个用户！')
            self.inputTextUserID.SetFocus()
            return None
        #删除记录
        else:
            wx.MessageBox("删除成功！")
            data.delete_user(userid)
        #初始化界面
        self.refresh_screen()

    def onExit(self,e):
        self.Close(True)  # 关闭顶层框架窗口
