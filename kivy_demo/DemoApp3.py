### system setting ###
import kivy
kivy.require('2.0.0')

### UI loading ###
from kivy.lang import Builder
Builder.load_file('./layout/login.kv')
Builder.load_file('./layout/helloworld.kv')
Builder.load_file('./layout/checkpwd.kv')
Builder.load_file('./layout/leave.kv')

### data loading ###
import json
with open('./data/accounts.json', 'r', encoding='utf-8') as f:
    accounts = json.load(f)

### windows ###
from kivy.core.window import Window
Window.size = (640,400)

### screen manage ###
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition

# login.kv
pwd_show = ''
class Login(Screen): 
    def __init__(self, **kwargs):
        super(Login, self).__init__(**kwargs)

    # login
    def app_login(self):
        #print('hello  world !')
        #demo_app.sm.switch_to(HelloWorld(name='HW'))
        global pwd_show
        if self.ids.usr.text in accounts: #account exist
            if self.ids.pwd.text==accounts[self.ids.usr.text]:
                pwd_show = 'Password Correct !'
            else:
                pwd_show = 'Password Error !'
        else:
            pwd_show = self.ids.pwd.text

        demo_app.sm.switch_to(CheckPwd(name='Check')) #change page

    # quit app
    def app_quit(self):
        #demo_app.stop()
        Leave().open()

# helloworld.kv
class HelloWorld(Screen):
    def __init__(self, **kwargs):
        super(HelloWorld, self).__init__(**kwargs)

# checkpwd.kv
from kivy.clock import Clock
class CheckPwd(Screen):
    def __init__(self, **kwargs):
        super(CheckPwd, self).__init__(**kwargs)
        self.ids.now_pwd.text = pwd_show
        self.bar_start()
    
    def bar_start(self):
        self.t0 = 0
        self.tn = 10
        self.ids.process_bar.value_normalized = 0
        self.bar_event = Clock.schedule_interval(self.bar_running, 1)

    def bar_running(self,dt):
        t_p = round(self.t0/(self.tn),2)
        self.ids.process_bar.value_normalized = t_p
        if self.t0 < self.tn:
            self.t0 = self.t0 + 1
        else :
            self.t0 = self.tn
            self.bar_event.cancel()
    
    def back_page(self):
        demo_app.sm.switch_to(Login(name='Login'))

# leave.kv
from kivy.uix.popup import Popup
class Leave(Popup):
    def __init__(self, **kwargs):
        super(Leave, self).__init__(**kwargs)

    def confirm(self):
        demo_app.stop()
    
    def stayhere(self):
        self.dismiss()

### run program ###
from kivy.app import App
class DemoApp(App):
    def build(self):
        self.sm = ScreenManager(transition=NoTransition())
        self.sm.add_widget(Login(name='Login')) #just add main
        return self.sm

if __name__ == "__main__":
    demo_app = DemoApp()
    demo_app.run()