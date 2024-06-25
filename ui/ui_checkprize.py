from data import data
import wx


userid2=0


class checkPrizeWindow(wx.Frame):
    def __init__(self, parent, title,userid,usertype):
        wx.Frame.__init__(self, parent, title=title, size=(500, 500))
        panel = wx.Panel(self, wx.ID_ANY)
        self.userid=userid
        global userid2
        self.usertype=usertype
        userid2=userid
        # 创建控件
        self.listget = wx.ListCtrl(panel, wx.ID_ANY, size=(500, 500), style=wx.LC_REPORT)
        self.listget.InsertColumn(0, '奖品ID', width=100)
        self.listget.InsertColumn(1, '用户ID',  width=100)
        self.listget.InsertColumn(2, '兑换时间', width=200)
        
        # 布局
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.listget, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        panel.SetSizer(vbox)
        self.Centre()        

        #查询用户信息并显示
        if usertype=="管理":
            self.populate_get_list_all()
        if usertype=="用户":
            self.populate_get_list_one(userid2)

        
    def populate_get_list_all(self):
        """查询奖品信息"""
        get_list = data.get_get_list_all()
        self.listget.DeleteAllItems()
        index = 0
        for get in get_list:
            self.listget.InsertItem(index, get[0])
            self.listget.SetItem(index, 1, get[1])
            self.listget.SetItem(index, 2, get[2])
            index += 1

    def populate_get_list_one(self,userid):
        """查询奖品信息"""
        get_list = data.get_get_list_one(userid)
        self.listget.DeleteAllItems()
        index = 0
        for get in get_list:
            self.listget.InsertItem(index, get[0])
            self.listget.SetItem(index, 1, get[1])
            self.listget.SetItem(index, 2, get[2])
            index += 1

    def refresh_screen(self):
        """重新刷新界面"""
        # 查询用户信息并显示
        self.populate_item_list()

