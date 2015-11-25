import sublime, sublime_plugin  #这是sublime插件必须要引入的两个库
import smtplib          #这是smtp邮件发送库
from email.mime.text import MIMEText
import threading

SETTINGS_FILE = 'Email.sublime-settings' #加载配置的配置文件名

class EmailCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    #这里用了python的正则表达式，如果看不懂的朋友，请先自行补习一下正则表达式的相关文法。
    a = self.view.find_all(r'#To:\S+@\S+\n', sublime.IGNORECASE)  #读取目标邮件地址
    mailto_list = []
    for i in a:
      mailto_list.append(self.view.substr(i)[4:])   #这是python中的截取字符串操作

    b = self.view.find(r'#Subject:\S+\n', sublime.IGNORECASE)
    subject = self.view.substr(b)[9:]
    # self.view.insert(edit,0,subject)

    c =  self.view.find(r'#Context:[\S|\s]+', sublime.IGNORECASE)
    context = self.view.substr(c)[10:]
    # self.view.insert(edit,0,context)

    settings = sublime.load_settings(SETTINGS_FILE) #加载设置哈希表

    # return_ans = send_mail(mailto_list,subject,context,
    #   settings.get("user_name"),settings.get("mail_addr"),
    #   settings.get("mail_host"),settings.get("mail_pass"))
    # if return_ans==True:
    #   sublime.status_message("发送成功")
    # else:
    #   sublime.status_message("发送失败")

    # 尝试方法1
    # threading.start_new_thread(send_mail,(
    #   mailto_list,subject,context,
    #   settings.get("user_name"),settings.get("mail_addr"),
    #   settings.get("mail_host"),settings.get("mail_pass")
    #   ))
    work = ThreadRun(mailto_list,subject,context,settings)
    work.start()

#这是一段用多线程实现发送邮件的代码，防止UI线程卡掉
class ThreadRun(threading.Thread):
  """docstring for ThreadRun"""
  mailto_list = []
  subject = None
  context = None
  psettings = None
  def __init__(self,mailto_list,subject,context,settings):
    self.mailto_list = mailto_list
    self.subject = subject
    self.context = context
    self.psettings = settings
    threading.Thread.__init__(self)

  def run(self):
    settings = self.psettings
    return_ans = send_mail(self.mailto_list,self.subject,self.context,
      settings.get("user_name"),settings.get("mail_addr"),
      settings.get("mail_host"),settings.get("mail_pass"))
    #get方法是sublimeAPI提供的，获取当前加载的设置中key对应的键值。
    if return_ans==True:
      sublime.status_message("发送成功")
    else:
      sublime.status_message("发送失败")



# 发送邮件函数
def send_mail(to_list, sub, context,user_name,mail_addr,mail_host,mail_pass):
    '''''
    to_list: ice@wedn.net
    sub: 主题
    context: 内容
    send_mail("xxx@163.com","sub","context")
    '''
    me = user_name+"<"+mail_addr+">"
    msg = MIMEText(context)
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        send_smtp = smtplib.SMTP()
        send_smtp.connect(mail_host)
        send_smtp.login(mail_addr, mail_pass)
        send_smtp.sendmail(me, to_list, msg.as_string())
        send_smtp.close()
        return True
        # sublime.status_message("发送成功")
    except (Exception, e):
        print(str(e))
        return False
        # sublime.status_message("发送失败")


