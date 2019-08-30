# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 10:58:38 2019

@author: SYW
"""
import os
import wx
import win32api,win32con
class AnnotateTool():
    def __init__(self,ent_type_lst,size):
        panel = wx.Panel(win,size=size)
        self.text_pos = -1
        self.origin_text= []
        self.annotated_text = []
        #多行文本，显示当前原始文本
        self.file_content = wx.TextCtrl(panel,pos=(5,35),size=(250,220),style=wx.TE_MULTILINE|wx.TE_WORDWRAP)
        self.file_content.Bind(wx.EVT_LEFT_UP,self.leftUp)
        #单行文本，显示标注后的文本
        self.file_annotated = wx.TextCtrl(panel,pos=(350,35),size=(250,220),style=wx.TE_MULTILINE|wx.TE_RICH2|wx.TE_WORDWRAP)
        #单行文本，显示选中的字符串
        self.select_text = wx.TextCtrl(panel,pos=(100,5),size=(80,25))
        #单行文本，显示选中字符串的位置
        self.select_text_pos = wx.TextCtrl(panel,pos=(200,5),size=(80,25))
        #单行文本，显示选中字符串的实体类型
        self.select_text_type = wx.TextCtrl(panel,pos=(300,5),size=(80,25))
#        #下拉列表，选择实体类型
#        self.select_lst = wx.ComboBox(panel,pos=(260,120),value='',choices=ent_type_lst,style=wx.CB_SORT)
#        self.select_lst.Bind(wx.EVT_COMBOBOX,self.onComBoBox)
        #点击按钮,加载文件
        self.load_btn = wx.Button(panel,label='load text',pos=(5,5),size=(80,25))
        self.load_btn.Bind(wx.EVT_BUTTON,self.load)
        #点击按钮，清空当前文本所有标注信息
        self.clear_btn = wx.Button(panel,label='clear cur',pos=(300,265),size=(80,25))
        self.clear_btn.Bind(wx.EVT_BUTTON,self.clear)
        #点击按钮，导出标注信息
        self.export_btn = wx.Button(panel,label='export annotation',pos=(400,265),size=(130,25))
        self.export_btn.Bind(wx.EVT_BUTTON,self.exportAnnotation)
        #点击按钮，切换到前一个文件
        self.former_btn = wx.Button(panel,label='former',pos=(5,265),size=(80,25))
        self.former_btn.Bind(wx.EVT_BUTTON,self.getFormer)
        #点击按钮，切换到下一个文件
        self.next_btn = wx.Button(panel,label='next',pos=(200,265),size=(80,25))
        self.next_btn.Bind(wx.EVT_BUTTON,self.getNext)
    def getFormer(self,event):
        if self.text_pos==0:
            win32api.MessageBox(0,'This is the FIRST text!','warning',win32con.MB_ICONWARNING)
        else:
            self.text_pos -= 1
            self.file_content.SetValue(self.origin_text[self.text_pos])
            self.file_annotated.SetValue(self.origin_text[self.text_pos])
    def getNext(self,event):
        if self.text_pos==len(self.origin_text)-1:
            win32api.MessageBox(0,'This is the LAST text!','warning',win32con.MB_ICONWARNING)
        else:
            self.text_pos += 1
            self.file_content.SetValue(self.origin_text[self.text_pos])
            self.file_annotated.SetValue(self.origin_text[self.text_pos])
    def load(self,event):
        wildcard = 'All files(*.*)|*.*'
        dlg = wx.FileDialog(None,message='select',defaultDir=os.getcwd(),defaultFile='',wildcard=wildcard,style=wx.FD_OPEN)
        if dlg.ShowModal()==wx.ID_OK:
            file = dlg.GetPath()
            with open(file,'r',encoding='utf-8') as fr:
                conts=fr.read()
            self.origin_text = conts.split('\n')[:-1]
            self.annotated_text = [[] for _ in range(len(self.origin_text))]
        dlg.Destroy()
        if len(self.origin_text):
            self.text_pos = 0
            self.file_content.SetValue(self.origin_text[self.text_pos])
            self.file_annotated.SetValue(self.origin_text[self.text_pos])
        else:
            win32api.MessageBox(0,'Please load texts first!','warning',win32con.MB_ICONWARNING)
    def leftUp(self,event):
        selected_text = self.file_content.GetStringSelection()
        selected_pos = self.file_content.GetSelection()
        self.select_text.SetValue(selected_text)
        self.select_text_pos.SetValue(str(selected_pos[0])+','+str(selected_pos[1]))
        selected_type = self.select_text_type.GetValue()
        self.annotated_text[self.text_pos].append([selected_text,selected_type,selected_pos[0],selected_pos[1]])
        self.file_annotated.SetStyle(selected_pos[0],selected_pos[1],wx.TextAttr(wx.WHITE,wx.BLACK))
        event.Skip()#释放鼠标左键后能再次响应该事件
#    def onComBoBox(self,event):
#        selected_type = self.select_lst.GetValue()
#        self.select_text_type.SetValue(selected_type)
    def clear(self,event):
        self.annotated_text[self.text_pos] = []
        self.select_text.SetValue('')
        self.select_text_pos.SetValue('')
        self.select_text_type.SetValue('')
        self.file_annotated.SetValue('')
        self.file_annotated.SetValue(self.origin_text[self.text_pos])
    def exportAnnotation(self,event):
        wildcard = 'All fiels(*.*)|*.*'
        dlg = wx.FileDialog(None,message='save',defaultDir=os.getcwd(),defaultFile='',wildcard=wildcard,style=wx.FD_SAVE)
        if dlg.ShowModal() ==wx.ID_OK:
            file = dlg.GetFilename()
            path = dlg.GetDirectory()
            if not file:
                file = 'result.txt'
            with open(os.path.join(path,file),'a',encoding='utf-8') as fw:
                for i in range(len(self.origin_text)):
                    fw.write(self.origin_text[i]+'\n')
                    for item in self.annotated_text[i]:
                        fw.write(item[0]+'\t'+item[1]+'\t'+str(item[2])+'\t'+str(item[3])+'\n')
                    fw.write('\n')
            win32api.MessageBox(0,'Finish exporting!','warning',win32con.MB_ICONWARNING)
        dlg.Destroy()
if __name__=='__main__':
    size=(650,400)
    lst = ['disease','drug','mutation']
    app = wx.App()
#    del app
    win = wx.Frame(None,title='test',size=size)
    win.Show()
    LT = AnnotateTool(lst,size)
    app.MainLoop()
    del app