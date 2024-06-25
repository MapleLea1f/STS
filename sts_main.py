import wx
from ui import ui_login

class App(wx.App):
    def OnInit(self):
        frame = ui_login.LoginWindow(parent=None, title='大学生校内悬赏任务大厅登录')
        frame.Show()
        frame.Center()
        return True

if __name__ == '__main__':
    app = App()
    app.MainLoop()