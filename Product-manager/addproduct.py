import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3
from PIL import Image

con = sqlite3.connect("products.db")
cur = con.cursor()

defaultImg = "Resources/img/store.png"

class AddProduct(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add product")
        self.setWindowIcon(QIcon("Resources/icons/icon.ico"))
        self.setGeometry(450, 150, 350, 550)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        # Widgets of top layout
        self.addProductImg = QLabel()
        self.img = QPixmap('Resources/icons/addproduct.png')
        self.addProductImg.setPixmap(self.img)
        self.titleText = QLabel("Add product")
        # Widgets of bottom layout
        self.nameEntry = QLineEdit()
        self.nameEntry.setPlaceholderText("Enter product name")
        self.manufacturerEntry = QLineEdit()
        self.manufacturerEntry.setPlaceholderText("Enter manufacturer")
        self.priceEntry = QLineEdit()
        self.priceEntry.setPlaceholderText("Enter price")
        self.quotaEntry = QLineEdit()
        self.quotaEntry.setPlaceholderText("Enter quota")
        self.uploadBtn = QPushButton("Upload")
        self.uploadBtn.clicked.connect(self.uploadImg)
        self.submitBtn = QPushButton("Submit")
        self.submitBtn.clicked.connect(self.addProduct)


    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.bottomFrame = QFrame()
        # Add widgets to top layout
        self.topLayout.addWidget(self.addProductImg)
        self.topLayout.addWidget(self.titleText)
        self.topFrame.setLayout(self.topLayout)
        # Add widgets to form layout
        self.bottomLayout.addRow(QLabel("Name"), self.nameEntry)
        self.bottomLayout.addRow(QLabel("Manufacturer"), self.manufacturerEntry)
        self.bottomLayout.addRow(QLabel("Price"), self.priceEntry)
        self.bottomLayout.addRow(QLabel("Upload"), self.uploadBtn)
        self.bottomLayout.addRow(QLabel("Quota"), self.quotaEntry)
        self.bottomLayout.addRow(QLabel(""), self.submitBtn)
        self.bottomFrame.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)
        self.setLayout(self.mainLayout)

    def uploadImg(self):
        global defaultImg
        size = (256, 256)
        self.filename,ok = QFileDialog().getOpenFileName(self, "Upload image", "",
                                                       "Image Files (*.jpg * png")
        if ok:
            print(self.filename)
            defaultImg = os.path.basename(self.filename)
            img = Image.open(self.filename)
            img = img.resize(size)
            img.save("img/{0}".format(defaultImg))


    def addProduct(self):
        global defaultImg
        name = self.nameEntry.text()
        manufacturer = self.manufacturerEntry.text()
        price = self.priceEntry.text()
        quota = self.quotaEntry.text()

        if (name and manufacturer and price and quota != ""):
            try:
                query = "INSERT INTO products (product_name, product_manufacturer, " \
                        "product_price, product_quota, product_img) VALUES(?, ?, ?, ?, ?)"
                cur.execute(query, (name, manufacturer, price, quota, defaultImg))
                con.commit()
                QMessageBox.information(self, "Info", "Product has been added")
            except:
                QMessageBox.information(self, "Info", "Product has not been added")
        else:
            QMessageBox.information(self, "Info", "Fields cannot be empty!")