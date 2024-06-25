import wx
from data import data
from . import ui_login

class registerWindow(wx.Dialog):
    def __init__(self, parent, title):
        wx.Dialog.__init__(self, parent, title=title, size=(1024, 680))
        panel = wx.Panel(self, wx.ID_ANY)
        #创建控件
        labelUserID = wx.StaticText(panel, wx.ID_ANY, '用户ID:')
        self.inputTextUserID = wx.TextCtrl(panel, wx.ID_ANY, '')
        labelUserName = wx.StaticText(panel, wx.ID_ANY, '昵称:')
        self.inputTextUserName = wx.TextCtrl(panel, wx.ID_ANY, '')    
        labelPhone = wx.StaticText(panel, wx.ID_ANY, '手机号:')
        self.inputTextPhone = wx.TextCtrl(panel, wx.ID_ANY, '')   
        labelPassword = wx.StaticText(panel, wx.ID_ANY, '密  码:')
        self.inputTextPassword = wx.TextCtrl(panel, wx.ID_ANY, style=wx.TE_PASSWORD)

        okBtn = wx.Button(panel, wx.ID_ANY, '确定')
        cancelBtn = wx.Button(panel, wx.ID_ANY, '取消')


        topSizer = wx.BoxSizer(wx.VERTICAL)
        userSizer = wx.BoxSizer(wx.HORIZONTAL)
        nameSizer = wx.BoxSizer(wx.HORIZONTAL)
        phoneSizer = wx.BoxSizer(wx.HORIZONTAL)
        passwordSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)

        userSizer.Add(labelUserID, 0, wx.ALL, 5)
        userSizer.Add(self.inputTextUserID, 0, wx.ALL, 5)
        nameSizer.Add(labelUserName, 0, wx.ALL, 5)
        nameSizer.Add(self.inputTextUserName, 0, wx.ALL, 5)
        phoneSizer.Add(labelPhone, 0, wx.ALL, 5)
        phoneSizer.Add(self.inputTextPhone, 0, wx.ALL, 5)
        passwordSizer.Add(labelPassword, 0, wx.ALL, 5)
        passwordSizer.Add(self.inputTextPassword, 0, wx.ALL, 5)
       
        btnSizer.Add(okBtn, 0, wx.ALL, 5)
        btnSizer.Add(cancelBtn, 0, wx.ALL, 5)

        topSizer.Add(userSizer, 0, wx.ALL | wx.CENTER, 5)
        topSizer.Add(nameSizer, 0, wx.ALL | wx.CENTER, 5)
        topSizer.Add(phoneSizer, 0, wx.ALL | wx.CENTER, 5)
        topSizer.Add(passwordSizer, 0, wx.ALL | wx.CENTER, 5)
        topSizer.Add(btnSizer, 0, wx.ALL | wx.CENTER, 5)

        panel.SetSizer(topSizer)
        topSizer.Fit(self)

        # 绑定事件.
        self.Bind(wx.EVT_BUTTON, self.onOk, okBtn)
        self.Bind(wx.EVT_BUTTON, self.onCancel, cancelBtn)

    def onOk(self, e):
        """ 事件处理函数：登录确认 """
        userid = self.inputTextUserID.GetValue()
        password = self.inputTextPassword.GetValue()
        username = self.inputTextUserName.GetValue()
        phone = self.inputTextPhone.GetValue()
        usertype="用户"
        if userid.strip()=="admin":
            wx.MessageBox('您不能成为管理员')
        if len(userid.strip()) == 0:
            wx.MessageBox('请输入用户ID！')
            self.inputTextUserID.SetFocus()
            return None
        if len(username.strip()) == 0:
            wx.MessageBox('请输入昵称！')
            self.inputTextUserName.SetFocus()
            return None
        if len(phone.strip()) == 0:
            wx.MessageBox('请输入手机号！')
            self.inputTextPhone.SetFocus()
            return None
        if len(password.strip()) == 0:
            wx.MessageBox('请输入登录密码！')
            self.inputTextPassword.SetFocus()
            return None
        userid_check=data.check_user_id(userid)
        if userid_check ==False:
            wx.MessageBox('注册成功，默认积分为50，正在为您跳转到登陆界面！')
            data.register(usertype,userid, username, phone,password)
            self.Close(True)  # 关闭窗口
            loginframe = ui_login.LoginWindow(parent=None, title='大学生校内悬赏任务大厅登录')
            loginframe.Show()
            loginframe.Center()

        else:
            wx.MessageBox('注册失败，有相同用户ID！')
            return None



    def onCancel(self,e):
        self.Close(True)  # 关闭窗口

