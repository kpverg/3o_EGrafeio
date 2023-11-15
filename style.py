def searchBoxStyle():
    return """
    QGroupBox{
    background-color:#9bc9ff;
    font:15pt Times Bold;
    color: White;
    border:2px solid gray;
    border-radius:15px;
    }
    """
    
def lstStyle():
    return """
    QTableWidget::item{
    
	background-color: white;
	color: black;
     }
    QTableView::item::selected{
        color: #4cf384;
        background-color:#041AE1;
        font:20pt Arial Bold;
    }

"""
def textEditStyle():
    return """
    QTextEdit{
        background: #ffffff;
    }
"""


def listBoxStyle():
    return """
    QGroupBox{
    background-color:#fcc324;
    font:15pt Arial Bold;
    color: White;
    border:2px solid gray;
    border-radius:15px;
    }
    """
def searchBtnStyle():
    return """
       QPushButton{
       background-color:#fcc324;
       border-style:outset;
       border-width:2px;
       border-radius:15px;
       border-color:beige;       
       font:12px;
       padding:6px;
       min-width:6em;
       }
       """
def ListBtnStyle():
    return """
       QPushButton{
       background-color:#9bc9ff;
       border-style:outset;
       border-width:2px;
       border-radius:15px;
       border-color:beige;       
       font:12px;
       padding:6px;
       min-width:6em;
       }
       """
def productbottomFrame():
    return """
       QFrame{
       font:10pt Times Bold;  
       background-color:#fcc324;
       }
       """
def productTopFrame():
    return """
       QFrame{
       font:10pt Times Bold;  
       background-color:white;
       }
       """