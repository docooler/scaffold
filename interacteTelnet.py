#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# code by elaiyan (Laiyuan yang)
import wx
import os
import datetime
from telnetlib import Telnet # core module
#---------------------------------------------------------------------------

class UpdateTimer(wx.Timer):
    def __init__(self, target, dur=1000):
        wx.Timer.__init__(self)
        self.target = target
        self.Start(dur)

    def Notify(self):
        """Called every timer interval"""
        if self.target:
            self.target.OnUpdate()


class wxEdit(wx.Frame):
    """docstring for wxEdit"""
    def __init__(self, parent, title, host, port):
        wx.Frame.__init__(self, parent, title=title, size=(1000,900))
        
        self.CreateStatusBar()

        # Setting up the menu.
        filemenu = wx.Menu()
        menuOpen = filemenu.Append(wx.ID_OPEN, "O&pen", "open testcase.xml")
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About", "code by elaiyan")
        # filemenu.AppendSeparator()
        menuExit = filemenu.Append(wx.ID_EXIT,  "E&xit", "Terminate the program")
        menuSave = filemenu.Append(wx.ID_SAVE, "S&ave", "save file")
        
        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        self.SetMenuBar(menuBar)

        # Events.
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnSave, menuSave)

        # self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
  #         self.buttons = []
  #         for i in range(0, 6):
  #             self.buttons.append(wx.Button(self, -1, "Button &"+str(i)))
  #             self.sizer2.Add(self.buttons[i], 1, wx.EXPAND)
        
  #         # Use some sizers to see layout options
  #         self.sizer = wx.BoxSizer(wx.VERTICAL)
  #         self.sizer.Add(self.control, 1, wx.EXPAND)
  #         self.sizer.Add(self.sizer2, 0, wx.EXPAND)
        
  #         #Layout sizers
  #         self.SetSizer(self.sizer)
  #         self.SetAutoLayout(1)
  #         self.sizer.Fit(self)
        self.panel = wx.Panel(self, -1)
        
        self.output = wx.TextCtrl(self.panel, -1, value="", size=(950,600), style=wx.TE_MULTILINE)

        font = wx.Font(8, wx.MODERN, wx.NORMAL, wx.NORMAL, faceName="Lucida Console")
        commandId = wx.NewId()
        self.control = wx.TextCtrl(self.panel, commandId, value="[command]", pos=(0,600),  size=(990,30), style=wx.TE_PROCESS_ENTER)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnEnter, self.control)
        
        self.tn = Telnet(host, port) # connect to host
        self.timer = UpdateTimer(self, 100) # update five times a second

        self.Show(True)

    def OnUpdate(self):
        """Output what's in the telnet buffer"""
        try:
            newtext = self.tn.read_very_eager()
            if newtext:
                lines = newtext.split('\n') # This keeps it from printing out extra blank lines.
                timestamp = datetime.datetime.now()
                tt = str(timestamp)
                first = True
                for line in lines:
                    if first:
                        context = line
                        first = False
                    else:
                        context = tt + ": " + line
                    self.output.AppendText(context)
                    print context
        except EOFError:
            self.tn.close()
            self.timer.Stop()
            self.output.AppendText("Disconnected by remote host")

    def OnOpen(self, e):
        self.dirname = ""
        dlg = wx.FileDialog(self, "Choose the testcases.xml", self.dirname, "", "testcases.xml", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname, self.filename), 'r')
            self.control.SetValue(f.read())
            f.close()
            self.tcs = testcases.TestCases(os.path.join(self.dirname, self.filename))
            pdt = self.tcs.getAllProductType()
            for x in sorted(pdt.keys()):
                self.choice.Append(x)       

        dlg.Destroy()
    def OnSave(self, e):
        if self.dirname == None:
            self.dirname = os.getcwd()
        dlg = wx.FileDialog(self, "please choice save file", self.dirname, "", "*.txt", wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetFilename()
            dirname = dlg.GetDirectory()
            self.control.SaveFile(os.path.join(dirname, filename))
            
        

    def OnAbout(self, e):
        dlg = wx.MessageDialog(self, "code by elaiyan", "List case from hardware", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
    
    def OnExit(self, e):
        self.Close(True)
    def OnEnter(self, e):
        """The user has entered a command.  Send it!"""
        cmd = e.GetString()
        cmd = unicode(cmd).encode('utf8')
        # print cmd
        self.tn.write(cmd + "\r\n")
        self.control.SetSelection(0, self.control.GetLastPosition())
        self.control.Clear()
    

def parse_xml(fd):
    return
def main(host, port):
    app = wx.App(False)
    edit = wxEdit(None, 'telnet terminal', host, port)
    app.MainLoop()
if __name__ == '__main__':
    import sys

    reload(sys)

    sys.setdefaultencoding('utf8')
    main(sys.argv[1],sys.argv[2])
        
