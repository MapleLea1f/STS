from data import data
import wx
from . import ui_main

itemid=0
itempoint=0
inventory=0

class PrizeWindow(wx.Frame):
    def __init__(self, parent, title,userid,point, usertype,username):
        wx.Frame.__init__(self, parent, title=title, size=(400, 400))
        panel = wx.Panel(self, wx.ID_ANY)
        self.userid=userid
        self.point=point
        self.usertype=usertype
        self.username=username
        # 创建控件
        self.listitem = wx.ListCtrl(panel, wx.ID_ANY, size=(400, 400), style=wx.LC_REPORT)
        self.listitem.InsertColumn(0, '奖品ID', width=80)
        self.listitem.InsertColumn(1, '奖品名称', width=150)
        self.listitem.InsertColumn(2, '奖品积分', width=80)
        self.listitem.InsertColumn(3, '库存剩余', width=80)
        
        self.getBtn = wx.Button(panel, wx.ID_ANY, '兑换')
        exitBtn = wx.Button(panel, wx.ID_ANY, '返回')
        
        # 布局
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.listitem, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        vbox.Add(self.getBtn, flag=wx.EXPAND | wx.ALL, border=10)
        vbox.Add(exitBtn, flag=wx.EXPAND | wx.ALL, border=10)
        panel.SetSizer(vbox)
        self.Centre()
        
        # 绑定事件
        self.Bind(wx.EVT_LIST_ITEM_FOCUSED, self.onitemList, self.listitem)
        self.Bind(wx.EVT_BUTTON, self.onGet, self.getBtn)
        self.Bind(wx.EVT_BUTTON, self.onExit, exitBtn)

        #查询用户信息并显示
        self.populate_item_list()

    def populate_item_list(self):
        """查询奖品信息"""
        item_list = data.get_item_list()
        self.listitem.DeleteAllItems()
        index = 0
        for item in item_list:
            self.listitem.InsertItem(index, item[0])
            self.listitem.SetItem(index, 1, item[1])
            self.listitem.SetItem(index, 2, str(item[2]))
            self.listitem.SetItem(index, 3, str(item[3]))
            index += 1



    def onitemList(self,e):
        """事件处理函数：在列表中选择用户，内容显获取"""
        global itemid,itempoint,inventory
        index = e.GetIndex() #获得被激活表项的索引号
        itemid=self.listitem.GetItem(index, 0).GetText()
        itempoint=self.listitem.GetItem(index, 2).GetText()
        inventory=self.listitem.GetItem(index, 3).GetText()



    def onGet(self,e):
        """事件处理函数：兑换奖品"""
        inventory=data.inventory_check(itemid)
        #开始兑换
        if len(itemid)==0:
            wx.MessageBox("请选择兑换的奖品")
        if inventory<=0:
            wx.MessageBox("库存不足！")
            return None
        if self.point<int(itempoint):
            wx.MessageBox("积分不足！")
        else:
            data.get_item(itemid,self.userid,new_point=self.point-int(itempoint),new_inventory=int(inventory)-1)
            wx.MessageBox("兑换成功！奖品信息已发送到您的手机短信，请稍后查收！")
            self.onMain(None)
            self.Close(True)

        #初始化界面
        self.refresh_screen()


    def refresh_screen(self):
        """重新刷新界面"""
        # 查询用户信息并显示
        self.populate_item_list()

   
    def onExit(self,e):
        self.Close(True)  # 关闭顶层框架窗口
        self.onMain(None)

    def onMain(self,e):
        title = "大学生校内悬赏任务大厅(登录： {0} / {1} / {2} / 当前积分为：{3} )".format(self.userid, self.username, self.usertype,data.check_point(self.userid))
        mainFrame = ui_main.MainWindow(None, title, self.userid, self.username, self.usertype)
        mainFrame.Show() #显示主窗口
        mainFrame.Center()  #窗口居中
