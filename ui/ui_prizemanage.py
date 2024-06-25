from data import data
import wx

class ManageWindow(wx.Dialog):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(800, 600))
        panel = wx.Panel(self, wx.ID_ANY)
        #创建控件
        lblListAction = ['插入', '修改', '删除']
        self.rboxAction = wx.RadioBox(panel, label='操作', choices=lblListAction)

        self.listitem = wx.ListCtrl(panel, wx.ID_ANY, size=(550, 400), style=wx.LC_REPORT)
        self.listitem.InsertColumn(0, '奖品ID', width=150)
        self.listitem.InsertColumn(1, '奖品名称',  width=150)
        self.listitem.InsertColumn(2, '奖品积分', width=100)
        self.listitem.InsertColumn(3, '库存余量', width=150)



        labelITEMID = wx.StaticText(panel, wx.ID_ANY, '奖品I D:')
        self.inputTextITEMID = wx.TextCtrl(panel, wx.ID_ANY, '')
        labelITEMName = wx.StaticText(panel, wx.ID_ANY, '奖品名称:')
        self.inputTextITEMName = wx.TextCtrl(panel, wx.ID_ANY, '')
        labelPoint = wx.StaticText(panel, wx.ID_ANY, '奖品积分:')
        self.inputTextPoint = wx.TextCtrl(panel, wx.ID_ANY, '')
        labelINVENTORY = wx.StaticText(panel, wx.ID_ANY, '库存余量:')
        self.inputTextINVENTORY = wx.TextCtrl(panel, wx.ID_ANY, '')


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
        ITEMIDSizer = wx.BoxSizer(wx.HORIZONTAL)
        ITEMnameSizer = wx.BoxSizer(wx.HORIZONTAL)

        inventorySizer = wx.BoxSizer(wx.HORIZONTAL)
        pointSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)

        optionSizer.Add(self.rboxAction, 0, wx.ALL, 5)

        listSizer.Add(self.listitem, 0, wx.ALL, 5)
    

        ITEMIDSizer.Add(labelITEMID, 0, wx.ALL, 5)
        ITEMIDSizer.Add(self.inputTextITEMID, 0, wx.ALL, 5)
        ITEMnameSizer.Add(labelITEMName, 0, wx.ALL, 5)
        ITEMnameSizer.Add(self.inputTextITEMName, 0, wx.ALL, 5)
        inventorySizer.Add(labelINVENTORY, 0, wx.ALL, 5)
        inventorySizer.Add(self.inputTextINVENTORY, 0, wx.ALL, 5)
        pointSizer.Add(labelPoint, 0, wx.ALL, 5)
        pointSizer.Add(self.inputTextPoint, 0, wx.ALL, 5)


        btnSizer.Add(self.insertBtn, 0, wx.ALL, 5)
        btnSizer.Add(self.updateBtn, 0, wx.ALL, 5)
        btnSizer.Add(self.deleteBtn, 0, wx.ALL, 5)
        btnSizer.Add(exitBtn, 0, wx.ALL, 5)

        editSizer.Add(ITEMIDSizer, 0, wx.ALL, 5)
        editSizer.Add(ITEMnameSizer, 0, wx.ALL, 5)
        editSizer.Add(pointSizer, 0, wx.ALL, 5)
        editSizer.Add(inventorySizer, 0, wx.ALL, 5)
        editSizer.Add(btnSizer, 0, wx.ALL, 5)

        contentSizer.Add(listSizer, 0, wx.ALL, 5)
        contentSizer.Add(editSizer, 0, wx.ALL, 5)

        topSizer.Add(optionSizer, 0, wx.ALL | wx.CENTER, 5)
        topSizer.Add(contentSizer, 0, wx.ALL | wx.CENTER, 5)

        panel.SetSizer(topSizer)
        topSizer.Fit(self)

        #绑定事件.
        self.Bind(wx.EVT_RADIOBOX, self.onAction, self.rboxAction)
        self.Bind(wx.EVT_LIST_ITEM_FOCUSED, self.onitemList, self.listitem)
        self.Bind(wx.EVT_BUTTON, self.onInsert, self.insertBtn)
        self.Bind(wx.EVT_BUTTON, self.onUpdate, self.updateBtn)
        self.Bind(wx.EVT_BUTTON, self.onDelete, self.deleteBtn)
        self.Bind(wx.EVT_BUTTON, self.onExit, exitBtn)

        #查询用户信息并显示
        self.populate_item_list()

    def populate_item_list(self):
        """查询用户信息并显示"""
        ITEM_list = data.get_item_list()
        self.listitem.DeleteAllItems()
        index = 0
        for ITEM in ITEM_list:
            self.listitem.InsertItem(index, ITEM[0])
            self.listitem.SetItem(index, 1, ITEM[1])
            self.listitem.SetItem(index, 2, str(ITEM[2]))
            self.listitem.SetItem(index, 3, str(ITEM[3]))
            index += 1

    def onAction(self, e):
        """事情处理函数：根据操作类型（插入、修改、删除）设置不同控件的状态"""
        action = self.rboxAction.GetStringSelection()
        if action == "插入":
            self.inputTextITEMID.Enable()
            self.insertBtn.Enable()
            self.updateBtn.Disable()
            self.deleteBtn.Disable()
        elif action == "修改":
            self.inputTextITEMID.Disable()
            self.insertBtn.Disable()
            self.updateBtn.Enable()
            self.deleteBtn.Disable()
        elif action == "删除":
            self.inputTextITEMID.Disable()
            self.insertBtn.Disable()
            self.updateBtn.Disable()
            self.deleteBtn.Enable()



    def onitemList(self,e):
        """事件处理函数：在列表中选择用户，内容显示在右侧"""
        index = e.GetIndex() #获得被激活表项的索引号
        self.inputTextITEMID.SetValue(self.listitem.GetItem(index, 0).GetText())
        self.inputTextITEMName.SetValue(self.listitem.GetItem(index, 1).GetText())
        self.inputTextPoint.SetValue(self.listitem.GetItem(index, 2).GetText())
        self.inputTextINVENTORY.SetValue(self.listitem.GetItem(index, 3).GetText())
        

    def onInsert(self,e):
        """事件处理函数：插入一条记录"""
        
        itemid = self.inputTextITEMID.GetValue()
        ITEMName = self.inputTextITEMName.GetValue()
        point = self.inputTextPoint.GetValue()
        inventory = self.inputTextINVENTORY.GetValue()
        if len(itemid.strip()) == 0:
            wx.MessageBox('请输入奖品ID！')
            self.inputTextITEMID.SetFocus()
            return None
        if len(ITEMName.strip()) == 0:
            wx.MessageBox('请输入奖品名称！')
            self.inputTextITEMName.SetFocus()
            return None
        
        if len(point.strip()) == 0:
            wx.MessageBox('请输入奖品积分（整数）！')
            self.inputTextPoint.SetFocus()
            return None
        
        if len(inventory.strip()) == 0:
            wx.MessageBox('请输入库存余量！')
            self.inputTextINVENTORY.SetFocus()
            return None    
        
        if data.check_item_id(itemid):
            wx.MessageBox("该奖品已经存在！")
            self.inputTextITEMID.SetFocus()
            return None
        #插入记录
        else:
            data.insert_item(itemid, ITEMName, point, inventory)
            wx.MessageBox("插入成功！")
        
        #初始化界面
        self.refresh_screen()


    def refresh_screen(self):
        """重新刷新界面"""
        self.inputTextITEMID.SetValue('')
        self.inputTextITEMName.SetValue('')
        self.inputTextPoint.SetValue('')
        self.inputTextINVENTORY.SetValue('')
        # 查询用户信息并显示
        self.populate_item_list()

    def onUpdate(self, e):
        """事件处理函数：更新一条记录"""
        itemid = self.inputTextITEMID.GetValue()
        ITEMName = self.inputTextITEMName.GetValue()
        point = self.inputTextPoint.GetValue()
        inventory = self.inputTextINVENTORY.GetValue()


        if len(ITEMName.strip()) == 0:
            wx.MessageBox('请输入奖品名称！')
            self.inputTextITEMName.SetFocus()
            return None
        
        if len(point.strip()) == 0:
            wx.MessageBox('请输入奖品积分（整数）！')
            self.inputTextPoint.SetFocus()
            return None
        
        if len(inventory.strip()) == 0:
            wx.MessageBox('请输入库存余量！')
            self.inputTextINVENTORY.SetFocus()
            return None    
        
        else:
        #更新记录
            data.update_item(itemid, ITEMName, point, inventory)
            wx.MessageBox("修改成功！")
        #初始化界面
        self.refresh_screen()

    def onDelete(self, e):
        
        """事件处理函数：删除一条记录"""
        itemid = self.inputTextITEMID.GetValue()
        if len(itemid.strip()) == 0:
            wx.MessageBox('请选择一个奖品！')
            self.inputTextITEMID.SetFocus()
            return None
        #删除记录
        else:
            wx.MessageBox("删除成功！")
            data.delete_item(itemid)
        #初始化界面
        self.refresh_screen()

    def onExit(self,e):
        self.Close(True)  # 关闭顶层框架窗口
