import wx
from data import data
from . import ui_main
from . import ui_register

class LoginWindow(wx.Dialog):
    def __init__(self, parent, title):
        wx.Dialog.__init__(self, parent, title=title, size=(1024, 680))
        panel = wx.Panel(self, wx.ID_ANY)
        #创建控件
        labelUserID = wx.StaticText(panel, wx.ID_ANY, '用户ID:')
        self.inputTextUserID = wx.TextCtrl(panel, wx.ID_ANY, '')
        labelPassword = wx.StaticText(panel, wx.ID_ANY, '密  码:')
        self.inputTextPassword = wx.TextCtrl(panel, wx.ID_ANY, style=wx.TE_PASSWORD)

        okBtn = wx.Button(panel, wx.ID_ANY, '登录')
        cancelBtn = wx.Button(panel, wx.ID_ANY, '取消')
        registerBtn = wx.Button(panel, wx.ID_ANY, '注册')

        topSizer = wx.BoxSizer(wx.VERTICAL)
        userSizer = wx.BoxSizer(wx.HORIZONTAL)
        passwordSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)

        userSizer.Add(labelUserID, 0, wx.ALL, 5)
        userSizer.Add(self.inputTextUserID, 0, wx.ALL, 5)
        passwordSizer.Add(labelPassword, 0, wx.ALL, 5)
        passwordSizer.Add(self.inputTextPassword, 0, wx.ALL, 5)
       
        btnSizer.Add(okBtn, 0, wx.ALL, 5)
        btnSizer.Add(cancelBtn, 0, wx.ALL, 5)
        btnSizer.Add(registerBtn, 0, wx.ALL, 5)

        topSizer.Add(userSizer, 0, wx.ALL | wx.CENTER, 5)
        topSizer.Add(passwordSizer, 0, wx.ALL | wx.CENTER, 5)
        topSizer.Add(btnSizer, 0, wx.ALL | wx.CENTER, 5)

        panel.SetSizer(topSizer)
        topSizer.Fit(self)

        # 绑定事件.
        self.Bind(wx.EVT_BUTTON, self.onOk, okBtn)
        self.Bind(wx.EVT_BUTTON, self.onCancel, cancelBtn)
        self.Bind(wx.EVT_BUTTON, self.onRegister, registerBtn)

    def onOk(self, e):
        """ 事件处理函数：登录确认 """
        userid = self.inputTextUserID.GetValue()
        password = self.inputTextPassword.GetValue()
        usertype=data.check_usertype(userid)
        username = data.check_login(userid, password, usertype)
        if len(userid.strip()) == 0:
            wx.MessageBox('请输入用户ID！')
            self.inputTextUserID.SetFocus()
            return None
        
        if len(password.strip()) == 0:
            wx.MessageBox('请输入登录密码！')
            self.inputTextPassword.SetFocus()
            return None
        
        if not username:
            wx.MessageBox('用户名或密码或角色错误，请重新输入！')
            self.inputTextUserID.SetFocus()
        else:
            self.Close(True)  # 关闭窗口
            point=data.check_point(userid)
            title = "大学生校内悬赏任务大厅(登录： {0} / {1} / {2} / 当前积分为：{3} )".format(userid, username, usertype,point)
            mainFrame = ui_main.MainWindow(None, title, userid, username, usertype)
            mainFrame.Show() #显示主窗口
            mainFrame.Center()  #窗口居中


    def onCancel(self,e):
        self.Close(True)  # 关闭窗口

    def onRegister(self,e):
            self.Close(True)  # 关闭窗口
            registerFrame = ui_register.registerWindow(parent=None,title='注册系统')
            registerFrame.Show() #显示主窗口
            registerFrame.Center()  #窗口居中