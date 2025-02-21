from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager

from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton,MDRectangleFlatButton
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout 
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable


class Table(MDApp):
    dialog=None
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_tables = None
    
        global contacts
        contacts = []
    

    def build(self):
        global sc
        sc=ScreenManager()
        sc.add_widget(Builder.load_file("main.kv")) #1
        sc.add_widget(Builder.load_file("update.kv")) #2
        sc.add_widget(Builder.load_file("add.kv")) #3
        return sc

    def add_datatable(self):
        import sqlite3
        vt = sqlite3.connect('zl.db')
        im = vt.cursor()
        im.execute("select * from person") #person table name
        data=im.fetchall()
        self.data_tables = MDDataTable(
            size_hint=(0.75, 0.5),
            use_pagination=True,
            check=True,
            column_data=[
                ("id",dp(30)),
                ("name", dp(30)),
                ("age", dp(30)),
                ("city", dp(30))
               
            ],
            row_data=[
                (
                i[:][0],
                i[:][1],
                i[:][2],
                i[:][3],   
                
                )
                for i in data 
            ],


        )
        self.data_tables.bind(on_check_press=self.on_check_press) 
        sc.get_screen("page").ids.datatable.add_widget( self.data_tables)    

    def on_start(self):
        self.add_datatable() 

    def on_check_press(self, instance_table,current_row):
            if current_row[0] not in contacts:
                contacts.append(current_row[0])
            else:
                contacts.remove(current_row[0])

            print(contacts)

     #delete data
    def delete(self):  
            #alert(message box)
           self.dialog=MDDialog(
                text="are you sure",
                buttons=[
                    MDFlatButton(text="[color=3338FF]no[/color]",on_release=self.close),
                    MDRectangleFlatButton(text="[color=096C7F]yes[/color]",on_release=self.open)
                ],

            )
           self.dialog.open()
    def close(self,obj):
            self.dialog.dismiss()
    def open(self,obj):     
            for i in contacts:
                if i:
                    import sqlite3
                    vt = sqlite3.connect('zl.db')
                    im = vt.cursor()
                    im.execute(f"delete from person where person_id={i} " )  
                    vt.commit()
                    sc.get_screen("page").ids.datatable.remove_widget(self.data_tables)
                    self.add_datatable()
            self.dialog.dismiss() 
            contacts.clear() 

    # open update.kv
    def updatenewpage(self):
        for i in contacts:
                if i:
                    import sqlite3
                    vt = sqlite3.connect('zl.db')
                    im = vt.cursor()
                    im.execute("select * from person where person_id=?",(i)) #person table name
                    data=im.fetchall()
                    for j in data:
                        sc.get_screen("upd").ids.name.text=j[1]
                        sc.get_screen("upd").ids.age.text=j[2]
                        sc.get_screen("upd").ids.city.text=j[3]
                       
        sc.current="upd"



        #open ad.kv
    def addnewpage(self):
        sc.current="add"

    #open main.kv
    def back(self):
        sc.current="page" #page nane/screen name

    #update data
    def update(self,username,age,city):
        for i in contacts:
                if i:
                    import sqlite3
                    vt = sqlite3.connect('zl.db')
                    im = vt.cursor()
                    im.execute("update person set username=?,age=?,city=? where person_id=?",(username,age,city,i))   
                    vt.commit()
                    sc.get_screen("page").ids.datatable.remove_widget(self.data_tables)
                    self.add_datatable() 

        contacts.clear() 
        sc.current="page"


    def add(self,username,age,city):
        import sqlite3
        vt = sqlite3.connect('zl.db')
        im = vt.cursor()
        im.execute("insert into person(username,age,city) VALUES(?,?,?)",(username,age,city))
        vt.commit()

        sc.get_screen("page").ids.datatable.remove_widget(self.data_tables)
        self.add_datatable() #functıon

        contacts.clear() 
        sc.current="page"    

Table().run()
