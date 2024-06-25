'''调用表Course，查看用户自己已发布的任务'''
from data import data
import wx



class EdWindow(wx.Dialog):
    def __init__(self, parent, title,userid,username):
        wx.Frame.__init__(self, parent, title=title, size=(750, 600))
        panel = wx.Panel(self, wx.ID_ANY)
        self.userid=userid
        self.username=username
        self.listCourseED = wx.ListCtrl(panel, wx.ID_ANY, size=(500, 500), style=wx.LC_REPORT)
        self.listCourseED.InsertColumn(0, '任务ID', width=50)
        self.listCourseED.InsertColumn(1, '任务名称',  width=80)
        self.listCourseED.InsertColumn(2, '积分', width=50)
        self.listCourseED.InsertColumn(3, '任务状态', width=80)
        self.listCourseED.InsertColumn(4, '接取用户', width=80)
        self.listCourseED.InsertColumn(5, '任务内容', width=100)





      

        topSizer = wx.BoxSizer(wx.VERTICAL)
        contentSizer = wx.BoxSizer(wx.HORIZONTAL)
        listSizer = wx.BoxSizer(wx.HORIZONTAL)

   

        listSizer.Add(self.listCourseED, 0, wx.ALL, 5)

        contentSizer.Add(listSizer, 0, wx.ALL, 5)
        topSizer.Add(contentSizer, 0, wx.ALL | wx.CENTER, 5)

        panel.SetSizer(topSizer)
        topSizer.Fit(self)


        #查询用户信息并显示
        self.populate_CourseED_list()

    def populate_CourseED_list(self):
        """查询用户信息并显示"""
        courseED_list = data.get_published_course_list(self.userid)
        self.listCourseED.DeleteAllItems()
        index = 0
        for courseED in courseED_list:
            self.listCourseED.InsertItem(index, courseED[0])#任务ID
            self.listCourseED.SetItem(index, 1, str(courseED[1]))#任务名称
            self.listCourseED.SetItem(index, 2, str(courseED[2]))#积分
            self.listCourseED.SetItem(index, 3, str(courseED[6]))#任务状态
            self.listCourseED.SetItem(index, 4, '暂无' if str(courseED[5])=='None' else str(courseED[5]))#接取用户
            self.listCourseED.SetItem(index, 5, str(courseED[3]))#任务内容
            index += 1


    # def refresh_screen(self):
    #     """重新刷新界面"""
    #     self.inputTextUserID.SetValue('')
    #     self.inputTextUserName.SetValue('')
    #     self.inputTextBirthday.SetValue('')
    #     self.inputTextDepartment.SetValue('')
    #     self.inputTextPhone.SetValue('')
    #     # 查询用户信息并显示
    #     self.populate_CourseED_list()



    def onExit(self,e):
        self.Close(True)  # 关闭顶层框架窗口
