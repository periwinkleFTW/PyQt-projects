from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3

con = sqlite3.connect("products.db")
cur = con.cursor()

defaultImg = "Resources/img/store.png"


class SellProducts(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sell products")
        self.setWindowIcon(QIcon('Resources/icons/icon.ico'))
        self.setGeometry(450, 150, 300, 600)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        # Top layout widgets
        self.sellProductImg = QLabel()
        self.img = QPixmap('Resources/icons/shop.png')
        self.sellProductImg.setPixmap(self.img)
        self.sellProductImg.setAlignment(Qt.AlignCenter)
        self.titleText = QLabel("Sell products")
        self.titleText.setAlignment(Qt.AlignCenter)
        # Bottom layout widgets
        self.productCombo = QComboBox()
        self.productCombo.currentIndexChanged.connect(self.changeComboValue)
        self.memberCombo = QComboBox()
        self.quantityCombo = QComboBox()
        self.submitBtn = QPushButton("Submit")
        self.submitBtn.clicked.connect(self.sellProduct)

        # Populate popup dropdown menus with data
        query1 = "SELECT * FROM products WHERE product_availability=?"
        products = cur.execute(query1, ('Available',)).fetchall()
        query2 = "SELECT member_id, member_name FROM members"
        members = cur.execute(query2).fetchall()
        quantity = products[0][4]

        for product in products:
            self.productCombo.addItem(product[1], product[0])

        for member in members:
            self.memberCombo.addItem(member[1], member[0])

        for i in range(1, quantity+1):
            self.quantityCombo.addItem(str(i))


    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.bottomFrame = QFrame()
        # Add widgets
        self.topLayout.addWidget(self.titleText)
        self.topLayout.addWidget(self.sellProductImg)
        self.topFrame.setLayout(self.topLayout)

        self.bottomLayout.addRow(QLabel("Product: "), self.productCombo)
        self.bottomLayout.addRow(QLabel("Member: "), self.memberCombo)
        self.bottomLayout.addRow(QLabel("Quantity: "), self.quantityCombo)
        self.bottomLayout.addRow(QLabel(""), self.submitBtn)
        self.bottomFrame.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)

        self.setLayout(self.mainLayout)

    def changeComboValue(self):
        self.quantityCombo.clear()
        # This instruction fetches id which is hidden
        product_id = self.productCombo.currentData()
        query = "SELECT product_quota FROM products WHERE product_id=?"
        quota = cur.execute(query, (product_id,)).fetchone()

        for i in range(1, quota[0]+1):
            self.quantityCombo.addItem(str(i))

    def sellProduct(self):
        global productName, productId, memberName, memberId, quantity
        productName = self.productCombo.currentText()
        # Current data fetches hidden id value
        productId = self.productCombo.currentData()
        memberName = self.memberCombo.currentText()
        memberId = self.memberCombo.currentData()
        quantity = int(self.quantityCombo.currentText())
        self.confirm = ConfirmWindow()
        self.close()

class ConfirmWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sell product")
        self.setWindowIcon(QIcon('Resources/icons/icon.ico'))
        self.setGeometry(450, 150, 350, 600)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        # Top layout widgets
        self.sellProductImg = QLabel()
        self.img = QPixmap('Resources/icons/shop.png')
        self.sellProductImg.setPixmap(self.img)
        self.sellProductImg.setAlignment(Qt.AlignCenter)
        self.titleText = QLabel("Sell product")
        self.titleText.setAlignment(Qt.AlignCenter)
        # Bottom layout widgets
        global productName, productId, memberName, memberId, quantity
        priceQuery = "SELECT product_price FROM products WHERE product_id=?"
        price = cur.execute(priceQuery,(productId,)).fetchone()
        self.amount = quantity * price[0]

        self.productName = QLabel()
        self.productName.setText(productName)
        self.memberName = QLabel()
        self.memberName.setText(memberName)
        self.amountLabel = QLabel()
        self.amountLabel.setText(str(price[0]) + 'x' + str(quantity) + '=' + str(self.amount))
        self.confirmBtn = QPushButton("Confirm")
        self.confirmBtn.clicked.connect(self.confirm)


    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.bottomFrame = QFrame()
        # Add widgets
        self.topLayout.addWidget(self.titleText)
        self.topLayout.addWidget(self.sellProductImg)
        self.topFrame.setLayout(self.topLayout)

        self.bottomLayout.addRow(QLabel("Product: "), self.productName)
        self.bottomLayout.addRow(QLabel("Member: "), self.memberName)
        self.bottomLayout.addRow(QLabel("Amount: "), self.amountLabel)
        self.bottomLayout.addRow(QLabel(""), self.confirmBtn)
        self.bottomFrame.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)

        self.setLayout(self.mainLayout)

    def confirm(self):
        global productName, productId, memberName, memberId, quantity
        try:
            sellQuery = "INSERT INTO sellings (selling_product_id, selling_member_id, " \
                        "selling_quantity, selling_amount)" \
                        "VALUES(?, ?, ?, ?)"
            cur.execute(sellQuery, (productId,memberId, quantity, self.amount))
            quotaQuery = "SELECT product_quota FROM products WHERE product_id=?"
            self.quota = cur.execute(quotaQuery, (productId,)).fetchone()
            con.commit()

            if (quantity == self.quota[0]):
                updateQuotaQuery = "UPDATE products SET product_quota=?, product_availability=?" \
                                   "WHERE product_id=?"
                # Set quota to 0 because you sold all you need to sell
                cur.execute(updateQuotaQuery,(0, 'Unavailable', productId))
                con.commit()
            else:
                newQuota = self.quota[0] - quantity
                updateQuotaQuery = "UPDATE products SET product_quota=?" \
                                   "WHERE product_id=?"
                cur.execute(updateQuotaQuery, (newQuota, productId))
                con.commit()

            QMessageBox.information(self, "Info", "Success")

        except:
            QMessageBox.information(self, "Info", "Something went wrong")

