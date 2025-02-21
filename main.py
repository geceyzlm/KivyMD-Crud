from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton,MDRectangleFlatButton
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout 
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable

class Tablo(MDApp):
    dialog=None#burada olucak 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_tables = None
    
    global contacts
    contacts = []

    def build(self):
        global ekran
        ekran=ScreenManager()
        ekran.add_widget(Builder.load_file("maug.kv"))
        return ekran
    
    
    def add_datatable(self):
        import sqlite3
        vt = sqlite3.connect('son.db')
        im = vt.cursor()
        im.execute("select * from COMPANY")
        veri=im.fetchall()
        self.data_tables = MDDataTable(
            size_hint=(0.5, 0.5),
            use_pagination=True,
            check=True,
            column_data=[
                ("id",dp(30)),
                ("ad", dp(30)),
                ("yaş", dp(30)),
                ("soyad", dp(30)),
                ("puan", dp(30))
            ],
            row_data=[
                (
                i[:][0],
                i[:][1],
                i[:][2],
                i[:][3],   
                i[:][4],
                )
                for i in veri  
            ],


        )
        self.data_tables.bind(on_check_press=self.on_check_press) 
        ekran.get_screen("you").ids.data.add_widget( self.data_tables)
       

    def on_start(self):#başlangıçta
        self.add_datatable()
   
    def on_check_press(self, instance_table,current_row):
        if current_row[0] not in contacts:
            contacts.append(current_row[0])
        else:
            contacts.remove(current_row[0])

        print(contacts)

    def delete(self):
        if not self.dialog:
            self.dialog=MDDialog(
                text="SİLME İŞLEMİNDEN EMİNMİSİNİZ",
                buttons=[
                    MDFlatButton(text="[color=3338FF]iptal[/color]",on_release=self.close),
                    MDRectangleFlatButton(text="[color=096C7F]kabul[/color]",on_release=self.open)
                ],

            )
            self.dialog.open()
    def close(self,obj):
            self.dialog.dismiss()
    def open(self,obj):     
            for i in contacts:
                if i:
                    import sqlite3
                    vt = sqlite3.connect('son.db')
                    im = vt.cursor()
                    im.execute(f"delete from COMPANY where id={i} " )  
                    vt.commit()
                    ekran.get_screen("you").ids.data.remove_widget(self.data_tables)
                    self.add_datatable()
            self.dialog.dismiss() 

    def guncelle(self,password,user):
        for i in contacts:
                if i:
                    import sqlite3
                    vt = sqlite3.connect('son.db')
                    im = vt.cursor()
                    im.execute(f"update COMPANY  set ad=?,yas=? where id={i}",(user,int(password)))  #int çunku yasın turu o
                    vt.commit()
                    ekran.get_screen("you").ids.data.remove_widget(self.data_tables)
                    self.add_datatable()

    def aramax(self,arama):
        import sqlite3
        vt = sqlite3.connect('son.db')
        im = vt.cursor()
        im.execute(f"select * from COMPANY where ad like '{arama}%'  ")
        
        veri=im.fetchall()

        self.arama_tables = MDDataTable(
            size_hint=(0.5, 0.5),
            use_pagination=True,
            check=True,
            column_data=[
                ("id",dp(30)),
                ("ad", dp(30)),
                ("yaş", dp(30)),
                ("soyad", dp(30)),
                ("puan", dp(30))
            ],
            row_data=[
                (
                i[:][0],
                i[:][1],
                i[:][2],
                i[:][3],   
                i[:][4],
                )
                for i in veri  
            ],


        )
        ekran.get_screen("you").ids.data.remove_widget(self.data_tables)

        ekran.get_screen("you").ids.data.add_widget(self.arama_tables)   

    def ekleme(self,password,user,soyad,puan): #passwordu yaş diye al
        import sqlite3
        vt = sqlite3.connect('son.db')
        im = vt.cursor()
        im.execute("insert into COMPANY( ad, yas,soyad, puan)  VALUES(?,?,?,?)",(user,password,soyad,int(puan)))
        vt.commit()

        ekran.get_screen("you").ids.data.remove_widget(self.data_tables)
        self.add_datatable()


Tablo().run()
