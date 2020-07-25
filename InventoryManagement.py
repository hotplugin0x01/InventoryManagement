# Create by Abdul Wassay
# USERNAME = admin
# PASSWORD = admin
#-------------------------
# Importing Modules
from tkinter import *
import tkinter.messagebox
import sqlite3
import tkinter.ttk as ttk


# Database class
class Database:
    """This class will interact with inventory database to control data saving envents."""
    
    def __init__(self):
        """The Constructor will connect will database and start cursor."""
        self.conn = sqlite3.connect("inventory_database.db")
        self.cursor = self.conn.cursor()
       
    def AddNew(self):
        """This method will get new products and add them into database."""
        try:
            self.cursor.execute("INSERT INTO product (product_name, product_qty, product_price) VALUES(?, ?, ?)",
                                (str(self.PRODUCT_NAME.get()), int(self.PRODUCT_QTY.get()), int(self.PRODUCT_PRICE.get())))
            self.conn.commit()
        except:
            tkinter.messagebox.showerror('Error', 'Integers Required for Quantity and Price!')
        self.PRODUCT_NAME.set("")
        self.PRODUCT_PRICE.set("")
        self.PRODUCT_QTY.set("")

    def DisplayData(self):
        """This method will connect data with tree view to show saved entries in database."""
        
        self.cursor.execute("SELECT * FROM product")
        fetch = self.cursor.fetchall()
        for data in fetch:
            self.tree.insert('', 'end', values=(data))

            
# Admin Class           
class Admin:
    """This class will control all the events of admin."""
    
    def Login(self, event=None):
        """This function will be used for login check of admin."""
        if self.USERNAME.get()== "" or self.PASSWORD.get() == "":
            tkinter.messagebox.showerror('Warning', 'Fill Complete Information!')
        else:
            if self.USERNAME.get() == 'admin' and self.PASSWORD.get() == 'admin':
                self.cursor.execute("""CREATE TABLE IF NOT EXISTS product (product_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                    product_name TEXT, product_qty TEXT, product_price TEXT)""")
                self.USERNAME.set("")
                self.PASSWORD.set("")
                self.root.destroy()
                self.Show_Home()
            else:
                tkinter.messagebox.showerror('Warning', 'Invalid Username/Password')
                self.USERNAME.set("")
                self.PASSWORD.set("")
    
    def Logout(self):
        """This method will be used to logout the admin."""
        
        result = tkinter.messagebox.askquestion('Jewelry Inventory System', 'Are you sure you want to logout?',
                                                icon="warning")
        if result == 'yes': 
            self.Home.destroy()
            Main.__init__(self)

    def AddNewItem(self):
        """This method will used to show window for adding new products in inventory database."""
        
        self.addnewform = Toplevel()
        self.addnewform.title("Jewelry Inventory System/Add new")
        width = 600
        height = 500
        screen_width = self.Home.winfo_screenwidth()
        screen_height = self.Home.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.addnewform.geometry("%dx%d+%d+%d" % (width, height, x, y))
        self.addnewform.resizable(0, 0)
        
        # Calling GUI form from Main child class
        self.Show_AddNew_Form()            

    def View(self):
        """This method will be used to open the view window to view existing products in inventory."""
        
        self.viewform = Toplevel()
        self.viewform.title("Jewelry Inventory System/View Product")
        width = 600
        height = 400
        screen_width = self.Home.winfo_screenwidth()
        screen_height = self.Home.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.viewform.geometry("%dx%d+%d+%d" % (width, height, x, y))
        self.viewform.resizable(0, 0)
        
        # Calling GUI form from Main child class
        self.Show_View_Form()
        
    def Search(self):
        """This method will bed used to search products in inventory database in  view window."""
        
        if self.SEARCH.get() != "":
            self.tree.delete(*self.tree.get_children())
            self.cursor.execute("SELECT * FROM product WHERE `product_name` LIKE ?", ('%'+str(self.SEARCH.get())+'%',))
            fetch = self.cursor.fetchall()
            for data in fetch:
                self.tree.insert('', 'end', values=(data))

    def Reset(self):
        """This method will reset the search entry in view window."""
        
        self.tree.delete(*self.tree.get_children())
        self.SEARCH.set("")
        
    def Delete(self):
        """This method will delete the selected product in the view window."""
        
        if not self.tree.selection():
            tkinter.messagebox.showerror('Jewelry Inventory System','Please select an item!')
        else:
            result = tkinter.messagebox.askquestion('Jewelry Inventory System', 'Are you sure you want to delete this record?', icon="warning")
            if result == 'yes':
                curItem = self.tree.focus()
                contents =(self.tree.item(curItem))
                selecteditem = contents['values']
                self.tree.delete(curItem)
                self.cursor.execute("DELETE FROM `product` WHERE `product_id` = %d" % selecteditem[0])
                self.conn.commit()


# Main Child GUI class using Multiple Inheritence
class Main(Database, Admin):
    """This class is inherited from both Database class and Admin class. It will connect the admin and
    database events with eachother and GUI."""
    
    def __init__(self):
        """The constructor will start the Login window"""
        
        Database.__init__(self)
        
        # Initializing Main Login Window
        self.root = Tk()
        self.root.title("Jewelry Inventory System")
        width = 1024
        height = 520
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.root.geometry("%dx%d+%d+%d" % (width, height, x, y))
        self.root.resizable(0, 0)
        
        # Login Entry Varibles
        self.USERNAME = StringVar()
        self.PASSWORD = StringVar()
        
        # Username and Password Label and Entries
        self.label_username = Label(self.root, text="USERNAME", width=20, fg='black', font=('arial', 25), bd=18)
        self.label_username.place(x=190, y=130)
        Entry(self.root, textvar=self.USERNAME, width=15, font=('arial',14)).place(x=520, y=152)
        
        self.label_password = Label(self.root, text="PASSWORD", width=20, fg='black', font=('arial', 25), bd=18)
        self.label_password.place(x=190, y=200)
        Entry(self.root, textvar=self.PASSWORD, width=15, show='*', font=('arial',14)).place(x=520, y=222)

        # Login Button
        self.btn_login = Button(self.root, text="Login", font=('arial', 18), width=18, command=super().Login)
        self.btn_login.place(x=360, y=320)
        self.root.bind('<Return>', super().Login) 
        
        # MainLoop
        self.root.mainloop()

    def Show_Home(self):
        """This method will show the Home window after logging input."""
        
        self.Home = Tk()
        self.Home.title("Jewelry Inventory System")
        width = 1024
        height = 520
        screen_width = self.Home.winfo_screenwidth()
        screen_height = self.Home.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.Home.geometry("%dx%d+%d+%d" % (width, height, x, y))
        self.Home.resizable(0, 0)
        
        # Adding Frame
        Title = Frame(self.Home, bd=1, relief=SOLID)
        Title.pack(pady=10)
        lbl_display = Label(Title, text="Jewelry Inventory System", font=('arial', 45))
        lbl_display.pack()
        
        # ADD New Item Button
        self.btn_add = Button(self.Home, text="ADD New Items", font=('arial', 18), width=18, command=super().AddNewItem)
        self.btn_add.place(x=360, y=120)
        
        # View Items Button
        self.btn_view = Button(self.Home, text="View Items", font=('arial', 18), width=18, command=super().View)
        self.btn_view.place(x=360, y=220)
        
        # Log out Button
        self.btn_logout = Button(self.Home, text="Log Out", font=('arial', 18), width=18, command=super().Logout)
        self.btn_logout.place(x=360, y=320)
        
    def Show_AddNew_Form(self):
        """This method will be called to open a new window to add new items."""
        
        # Entry Variables
        self.PRODUCT_NAME = StringVar()
        self.PRODUCT_PRICE = IntVar()
        self.PRODUCT_QTY = IntVar()
        
        # Adding Frame
        TopAddNew = Frame(self.addnewform, width=600, height=100, bd=1, relief=SOLID)
        TopAddNew.pack(side=TOP, pady=20)
        lbl_text = Label(TopAddNew, text="Add New Product", font=('arial', 18), width=600).pack(fill=X)
        MidAddNew = Frame(self.addnewform, width=600)
        MidAddNew.pack(side=TOP, pady=50)
        
        # Item Name, Quantity, Price Labels and Entries
        lbl_productname = Label(MidAddNew, text="Item Name:", font=('arial', 25), bd=10)
        lbl_productname.grid(row=0, sticky=W)
        
        lbl_qty = Label(MidAddNew, text="Item Quantity:", font=('arial', 25), bd=10)
        lbl_qty.grid(row=1, sticky=W)
        
        lbl_price = Label(MidAddNew, text="Item Price:", font=('arial', 25), bd=10)
        lbl_price.grid(row=2, sticky=W)
        
        productname = Entry(MidAddNew, textvar=self.PRODUCT_NAME, font=('arial', 25), width=15)
        productname.grid(row=0, column=1)
        
        productqty = Entry(MidAddNew, textvar=self.PRODUCT_QTY, font=('arial', 25), width=15)
        productqty.grid(row=1, column=1)
        
        productprice = Entry(MidAddNew, textvar=self.PRODUCT_PRICE, font=('arial', 25), width=15)
        productprice.grid(row=2, column=1)
        
        # ADD button
        btn_add = Button(MidAddNew, text="ADD", font=('arial', 18), width=20, command=super().AddNew)
        btn_add.grid(row=3, columnspan=2, pady=20)
        
    def Show_View_Form(self):
        """This method will show the window to show tree view of inventory items."""
        
        # Entry Variable
        self.SEARCH = StringVar()
        
        # Adding Frames
        TopViewForm = Frame(self.viewform, width=600, bd=1, relief=SOLID)
        TopViewForm.pack(side=TOP, fill=X)
        LeftViewForm = Frame(self.viewform, width=600)
        LeftViewForm.pack(side=LEFT, fill=Y)
        MidViewForm = Frame(self.viewform, width=600)
        MidViewForm.pack(side=RIGHT)
        
        lbl_text = Label(TopViewForm, text="View Items", font=('arial', 18), width=600)
        lbl_text.pack(fill=X)
        
        lbl_txtsearch = Label(LeftViewForm, text="Search", font=('arial', 15))
        lbl_txtsearch.pack(side=TOP, anchor=W)
        
        search = Entry(LeftViewForm, textvariable=self.SEARCH, font=('arial', 15), width=10)
        search.pack(side=TOP,  padx=10, fill=X)
        
        # Search Button
        btn_search = Button(LeftViewForm, text="Search", command=super().Search)
        btn_search.pack(side=TOP, padx=10, pady=10, fill=X)
        
        # Reset Button
        btn_reset = Button(LeftViewForm, text="Reset", command=super().Reset)
        btn_reset.pack(side=TOP, padx=10, pady=10, fill=X)
        
        # Delete Button
        btn_delete = Button(LeftViewForm, text="Delete", command=super().Delete)
        btn_delete.pack(side=TOP, padx=10, pady=10, fill=X)
        
        # Scroll Bar to view items
        scrollbarx = Scrollbar(MidViewForm, orient=HORIZONTAL)
        scrollbary = Scrollbar(MidViewForm, orient=VERTICAL)
        self.tree = ttk.Treeview(MidViewForm, columns=("ProductID", "Product Name", "Product Qty", "Product Price"),
                                 selectmode="extended", height=100, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        scrollbary.config(command=self.tree.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx.config(command=self.tree.xview)
        scrollbarx.pack(side=BOTTOM, fill=X)
        
        # Tree view to view items in inventory 
        self.tree.heading('ProductID', text="ProductID",anchor=W)
        self.tree.heading('Product Name', text="Product Name",anchor=W)
        self.tree.heading('Product Qty', text="Product Qty",anchor=W)
        self.tree.heading('Product Price', text="Product Price",anchor=W)
        self.tree.column('#0', stretch=NO, minwidth=0, width=0)
        self.tree.column('#1', stretch=NO, minwidth=0, width=0)
        self.tree.column('#2', stretch=NO, minwidth=0, width=200)
        self.tree.column('#3', stretch=NO, minwidth=0, width=120)
        self.tree.column('#4', stretch=NO, minwidth=0, width=120)
        self.tree.pack()
        
        # Linking Tree view to Database function to fetch items from database
        super().DisplayData()

# Driver Code
if __name__ == '__main__':
    program = Main()
