#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Don Spickler

Image viewer and annotator.

"""
import pickle
import traceback
from math import *

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtPrintSupport import *
from PySide6.QtWidgets import *

import sys
import os
import platform
import webbrowser


class appcss:
    def __init__(self):
        super().__init__()
        self.css = """
            QMenu::separator { 
                background-color: #BBBBBB; 
                height: 1px; 
                margin: 2px 5px 2px 5px;
            }

            QMenu {padding: 4px 0px 4px 0px; }

            QListWidget::item {
                color:#000000;
                background-color:transparent;
            }

            QListWidget::item:selected {
                background: rgb(193,225,236);
            }
        """

    def getCSS(self):
        return self.css


class QHLine(QFrame):
    """
    Creates a horizontal line for dialog boxes.
    """

    def __init__(self):
        super(QHLine, self).__init__()
        try:
            self.setFrameShape(QFrame.Shape.HLine)
            self.setFrameShadow(QFrame.Shadow.Sunken)
        except:
            self.setFrameShape(QFrame.HLine)
            self.setFrameShadow(QFrame.Sunken)


class ColorSelectButtonBox(QLabel):
    colorChange = Signal(QColor)

    def __init__(self, color = QColor(0,0,0), Parent=None, minwidth = 50, maxwidth = 100):
        """
        Creates the UI for the label.

        :param color: Color of the box, designating the selected color.
        :param Parent: Parent object.
        :param minwidth: Minimum width of the label.
        :param maxwidth: Maximum width of the label.
        """
        super(ColorSelectButtonBox, self).__init__(Parent)
        self.parent = Parent
        self.setText('')
        self.setMaximumWidth(maxwidth)
        self.setMinimumWidth(minwidth)
        self.color = color
        self.setColor(self.color)
        self.setFrameShape(QFrame.Panel)
        self.setLineWidth(1)

    def setColor(self, color):
        """
        Sets the background color of the label.

        :param color: Label color.
        :return: None
        """
        self.color = color
        self.setStyleSheet(f'background-color: rgb({self.color.red()}, {self.color.green()}, {self.color.blue()});')

    def mousePressEvent(self, ev):
        """
        Sets the moused pressed event to open up a color dialog box for the user to select a color.

        :param ev: Moused pressed event.
        :return: None
        """
        newcolor = QColorDialog.getColor(self.color, self.parent, 'Select Color',
                                         QColorDialog.DontUseNativeDialog)

        if newcolor.isValid():
            self.setColor(newcolor)
            self.colorChange.emit(self.color)


class StringsNumbersInputDialog(QDialog):
    def __init__(self, parent=None, title="Input Strings and Numbers", message="", itemMessages=[], numMessages=[],
        numRanges=[], checkMessages=[], checkValues=[], mininputwidth=200, spinwidth=50, checkEmptyInputs=True,
                 checkInputSyntax=True):
        """
        Constructor: Sets up the UI for the dialog box.

        :param parent: Parent object.
        :param title: Dialog title.
        :param message: General message at the top.
        :param itemMessages: List of labels for the input boxes.
        :param numMessages: List of labels for the spin boxes.
        :param numRanges: List of ranges for the spin boxes [lb, ub, val].
        :param checkMessages: List of labels for the checkboxes.
        :param checkValues:  List of states for the checkboxes.
        :param mininputwidth: Minimum width for the input boxes.
        :param spinwidth: Minimum width for the spin boxes.
        :param checkEmptyInputs: Flag to check that all inputs are given.
        :param checkInputSyntax: Flag to check that all inputs are syntactically correct.
        """
        super().__init__(parent)
        self.setWindowTitle(title)
        self.parent = parent
        self.checkEmptyInputs = checkEmptyInputs
        self.checkInputSyntax = checkInputSyntax

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        buttonBox = QDialogButtonBox(QBtn)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        buttonBox.button(QDialogButtonBox.Ok).setAutoDefault(True)
        buttonBox.button(QDialogButtonBox.Ok).setDefault(True)
        buttonBox.button(QDialogButtonBox.Cancel).setAutoDefault(False)
        buttonBox.button(QDialogButtonBox.Cancel).setDefault(False)

        messagelabel = QLabel(message)
        messagelabel.setWordWrap(True)

        inputs = QGridLayout()
        self.LineEditList = []
        for i in range(len(itemMessages)):
            lineed = QLineEdit()
            lineed.setMinimumWidth(mininputwidth)
            self.LineEditList.append(lineed)
            inputs.addWidget(QLabel(itemMessages[i]), i, 0, Qt.AlignRight)
            inputs.addWidget(self.LineEditList[i], i, 1)

        self.SpinList = []
        for i in range(len(numMessages)):
            spincont = QSpinBox()
            spincont.setMinimumWidth(spinwidth)
            spincont.setMaximumWidth(spinwidth)
            spincont.setMinimum(numRanges[i][0])
            spincont.setMaximum(numRanges[i][1])
            spincont.setValue(numRanges[i][2])
            self.SpinList.append(spincont)
            inputs.addWidget(QLabel(numMessages[i]), i + len(itemMessages), 0, Qt.AlignRight)
            inputs.addWidget(self.SpinList[i], i + len(itemMessages), 1)

        self.CheckList = []
        for i in range(len(checkMessages)):
            checkcont = QCheckBox()
            checkcont.setChecked(checkValues[i])
            self.CheckList.append(checkcont)
            inputs.addWidget(QLabel(checkMessages[i]), i + len(itemMessages)+ len(numMessages), 0, Qt.AlignRight)
            inputs.addWidget(self.CheckList[i], i + len(itemMessages)+ len(numMessages), 1)

        centerlayout = QVBoxLayout()
        centerlayout.addWidget(messagelabel)
        inputsection = QHBoxLayout()
        inputsection.addLayout(inputs)
        inputsection.addStretch(1)
        centerlayout.addLayout(inputsection)
        centerlayout.addWidget(buttonBox)
        self.setLayout(centerlayout)
        self.adjustSize()
        self.setFixedSize(self.size())

    def accept(self):
        """
        Override of the accept function to check the validity of the inputs before closing.

        :return: None
        """
        i = 1
        for tb in self.LineEditList:
            expstr, experobj = self.parent.TestInputStringValid(tb.text())
            if len(expstr) == 0 and self.checkEmptyInputs:
                QMessageBox.warning(self, "Empty Input", 'The input for input #'+ str(i) + ' must be given.',
                                    QMessageBox.Ok)
                tb.setFocus()
                return
            elif experobj is None and self.checkInputSyntax:
                QMessageBox.warning(self, "Input Syntax Error",
                                    'There is a syntax error in input #' + str(i) + '.', QMessageBox.Ok)
                tb.setFocus()
                return
            i+=1
        super().accept()


    def getText(self, pos = 0):
        """ Gets the text from the text input box #pos. """
        return self.LineEditList[pos].text()

    def setText(self, pos = 0, mes = ''):
        """ Gets the text from the text input box #pos. """
        self.LineEditList[pos].setText(mes)

    def getVal(self, pos = 0):
        """ Gets the spinner control #pos value. """
        return self.SpinList[pos].value()

    def setVal(self, pos = 0, val = 10):
        """ Gets the spinner control #pos value. """
        self.SpinList[pos].setValue(val)

    def getChecked(self, pos = 0):
        """ Gets the check control #pos value. """
        return self.CheckList[pos].isChecked()

    def setChecked(self, pos = 0, val = False):
        """ Gets the check control #pos value. """
        self.CheckList[pos].setChecked(val)


class Canvas(QWidget):
    def __init__(self, img=None):
        """
        Widget for displaying an image in the center of the widget.  Automatically resizes the image to fit
        the available area.

        :param img: Image to display.
        """
        super().__init__()
        self.image = img
        if self.image is None:
            self.image = QImage()

    def setImage(self, img=None):
        """
        Sets the image to be displayed.

        :param img: Image to be displayed.
        :return: None
        """
        if img is None:
            self.image = QImage()
        else:
            self.image = img
        self.repaint()

    def paintEvent(self, event):
        """
        Overrides the widget paint event to display the current image.

        :param event: Paint event
        :return: None
        """
        painter = QPainter()
        painter.begin(self)

        imgwidth = self.image.width()
        imgheight = self.image.height()

        if imgwidth > self.width():
            ar = imgwidth/imgheight
            imgwidth = self.width()
            imgheight = imgwidth/ar

        if imgheight > self.height():
            ar = imgwidth/imgheight
            imgheight = self.height()
            imgwidth = imgheight*ar

        xpos = (self.width() - imgwidth)//2
        ypos = (self.height() - imgheight) // 2

        painter.drawImage(QRect(xpos, ypos, imgwidth, imgheight), self.image)
        painter.end()

## Graphics Objects Data Classes

class TextObject():
    def __init__(self):
        """
        Object for storing the attributes of a text annotation.
        """
        self.show = True
        self.text = 'Insert Text'
        self.font = QFont()
        self.font.setPointSize(12)
        self.xpos = 0
        self.ypos = 0
        self.color = QColor(Qt.black)
        self.includeBox = False
        self.backgroundColor = QColor(Qt.white)
        self.borderColor = QColor(Qt.black)
        self.borderWidth = 1
        self.justify = 'left'
        self.xPadding = 0
        self.yPadding = 0
        self.transparency = 0
        self.rotation = 0

    def toDisplayString(self):
        """
        Creates a string representing the object for display in the annotation list.

        :return: Information display string.
        """
        rettext = 'Text: ' + self.text + '  x: ' + str(self.xpos) + '  y: '+ str(self.ypos)
        if not self.show:
            rettext += '  (Hidden)'
        return rettext

    def toList(self):
        """
        Saves the object attributes to a list for saving to a file.

        :return: List of attributes.
        """
        datalist = ['TextObject']
        datalist.append(self.show)
        datalist.append(self.text)
        datalist.append(self.font.toString())
        datalist.append(self.xpos)
        datalist.append(self.ypos)
        datalist.append(self.color.rgba())
        datalist.append(self.includeBox)
        datalist.append(self.backgroundColor.rgba())
        datalist.append(self.borderColor.rgba())
        datalist.append(self.borderWidth)
        datalist.append(self.justify)
        datalist.append(self.xPadding)
        datalist.append(self.yPadding)
        datalist.append(self.transparency)
        datalist.append(self.rotation)
        return datalist

    def fromList(self, datalist):
        """
        Loads the object attributes from a list that was stored in a file.

        :param datalist: List of object attributes to be loaded.  List is of the same format as with the
        toList function.
        :return:  None
        """
        self.show = datalist[1]
        self.text = datalist[2]
        self.font = QFont()
        self.font.fromString(datalist[3])
        self.xpos = datalist[4]
        self.ypos = datalist[5]
        self.color = QColor(Qt.black)
        self.color.setRgba(datalist[6])
        self.includeBox = datalist[7]
        self.backgroundColor = QColor(Qt.white)
        self.backgroundColor.setRgba(datalist[8])
        self.borderColor = QColor(Qt.black)
        self.borderColor.setRgba(datalist[9])
        self.borderWidth = datalist[10]
        self.justify = datalist[11]
        self.xPadding = datalist[12]
        self.yPadding = datalist[13]
        self.transparency = datalist[14]
        self.rotation = datalist[15]


class ImageObject():
    def __init__(self):
        """
        Object for storing the attributes of an image annotation.
        """
        self.show = True
        self.image = QImage()
        self.xpos = 0
        self.ypos = 0
        self.includeBox = False
        self.backgroundColor = QColor(Qt.white)
        self.borderColor = QColor(Qt.black)
        self.borderWidth = 1
        self.xPadding = 0
        self.yPadding = 0
        self.transparency = 0
        self.useTransparentColor = False
        self.transparentColor = QColor(255, 255, 255)
        self.aspectratio = 1
        self.scale = 1
        self.FlipHorizontal = False
        self.FlipVertical = False
        self.rotation = 0

    def toDisplayString(self):
        """
        Creates a string representing the object for display in the annotation list.

        :return: Information display string.
        """
        rettext = 'Image: (' + str(self.image.width()) + ' X ' + str(self.image.height()) + ')  x: ' + str(self.xpos) + '  y: '+ str(self.ypos)
        if not self.show:
            rettext += '  (Hidden)'
        return rettext

    def toList(self):
        """
        Saves the object attributes to a list for saving to a file.

        :return: List of attributes.
        """
        datalist = ['ImageObject']
        datalist.append(self.show)

        buffer = QBuffer()
        buffer.open(QIODeviceBase.OpenModeFlag.WriteOnly)
        self.image.save(buffer, "PNG")
        raw_image_bytes = buffer.data()

        image_data = {
            "width": self.image.width(),
            "height": self.image.height(),
            "format": self.image.format(),
            "data": bytes(raw_image_bytes),
        }

        datalist.append(image_data)
        datalist.append(self.xpos)
        datalist.append(self.ypos)
        datalist.append(self.includeBox)
        datalist.append(self.backgroundColor.rgba())
        datalist.append(self.borderColor.rgba())
        datalist.append(self.borderWidth)
        datalist.append(self.xPadding)
        datalist.append(self.yPadding)
        datalist.append(self.transparency)
        datalist.append(self.useTransparentColor)
        datalist.append(self.transparentColor.rgba())
        datalist.append(self.aspectratio)
        datalist.append(self.scale)
        datalist.append(self.FlipHorizontal)
        datalist.append(self.FlipVertical)
        datalist.append(self.rotation)
        return datalist

    def fromList(self, datalist):
        """
        Loads the object attributes from a list that was stored in a file.

        :param datalist: List of object attributes to be loaded.  List is of the same format as with the
        toList function.
        :return:  None
        """
        self.show = datalist[1]

        restored_image = QImage.fromData(
            datalist[2]["data"],
            "PNG"
        )

        self.image = restored_image

        self.xpos = datalist[3]
        self.ypos = datalist[4]
        self.includeBox = datalist[5]
        self.backgroundColor = QColor(Qt.white)
        self.backgroundColor.setRgba(datalist[6])
        self.borderColor = QColor(Qt.black)
        self.borderColor.setRgba(datalist[7])
        self.borderWidth = datalist[8]
        self.xPadding = datalist[9]
        self.yPadding = datalist[10]
        self.transparency = datalist[11]
        self.useTransparentColor = datalist[12]
        self.transparentColor = QColor(255, 255, 255)
        self.transparentColor.setRgba(datalist[13])
        self.aspectratio = datalist[14]
        self.scale = datalist[15]
        self.FlipHorizontal = datalist[16]
        self.FlipVertical = datalist[17]
        self.rotation = datalist[18]


class LineObject():
    def __init__(self):
        """
        Object for storing the attributes of a line annotation.
        """
        self.show = True
        self.startxpos = 10
        self.startypos = 10
        self.endxpos = 100
        self.endypos = 100
        self.color = QColor(Qt.black)
        self.width = 1

    def toDisplayString(self):
        """
        Creates a string representing the object for display in the annotation list.

        :return: Information display string.
        """
        rettext = 'Line: (' + str(self.startxpos) + ', ' + str(self.startypos) + ') - ('
        rettext += str(self.endxpos) + ', ' + str(self.endypos) + ')'
        if not self.show:
            rettext += '  (Hidden)'
        return rettext

    def toList(self):
        """
        Saves the object attributes to a list for saving to a file.

        :return: List of attributes.
        """
        datalist = ['LineObject']
        datalist.append(self.show)
        datalist.append(self.startxpos)
        datalist.append(self.startypos)
        datalist.append(self.endxpos)
        datalist.append(self.endypos)
        datalist.append(self.color.rgba())
        datalist.append(self.width)
        return datalist

    def fromList(self, datalist):
        """
        Loads the object attributes from a list that was stored in a file.

        :param datalist: List of object attributes to be loaded.  List is of the same format as with the
        toList function.
        :return:  None
        """
        self.show = datalist[1]
        self.startxpos = datalist[2]
        self.startypos = datalist[3]
        self.endxpos = datalist[4]
        self.endypos = datalist[5]
        self.color = QColor(Qt.black)
        self.color.setRgba(datalist[6])
        self.width = datalist[7]

class ArrowObject():
    def __init__(self):
        """
        Object for storing the attributes of an arrow annotation.
        """
        self.show = True
        self.startxpos = 10
        self.startypos = 10
        self.endxpos = 100
        self.endypos = 100
        self.color = QColor(Qt.black)
        self.width = 1
        self.arrowAngle = 30
        self.arrowSize = 10

    def toDisplayString(self):
        """
        Creates a string representing the object for display in the annotation list.

        :return: Information display string.
        """
        rettext = 'Arrow: (' + str(self.startxpos) + ', ' + str(self.startypos) + ') - ('
        rettext += str(self.endxpos) + ', ' + str(self.endypos) + ')'
        if not self.show:
            rettext += '  (Hidden)'
        return rettext

    def toList(self):
        """
        Saves the object attributes to a list for saving to a file.

        :return: List of attributes.
        """
        datalist = ['ArrowObject']
        datalist.append(self.show)
        datalist.append(self.startxpos)
        datalist.append(self.startypos)
        datalist.append(self.endxpos)
        datalist.append(self.endypos)
        datalist.append(self.color.rgba())
        datalist.append(self.width)
        datalist.append(self.arrowAngle)
        datalist.append(self.arrowSize)
        return datalist

    def fromList(self, datalist):
        """
        Loads the object attributes from a list that was stored in a file.

        :param datalist: List of object attributes to be loaded.  List is of the same format as with the
        toList function.
        :return:  None
        """
        self.show = datalist[1]
        self.startxpos = datalist[2]
        self.startypos = datalist[3]
        self.endxpos = datalist[4]
        self.endypos = datalist[5]
        self.color = QColor(Qt.black)
        self.color.setRgba(datalist[6])
        self.width = datalist[7]
        self.arrowAngle = datalist[8]
        self.arrowSize = datalist[9]


class RectangleObject():
    def __init__(self):
        """
        Object for storing the attributes of a rectangle annotation.
        """
        self.show = True
        self.xpos = 0
        self.ypos = 0
        self.width = 100
        self.height = 100
        self.cornerrad = 0
        self.color = QColor(Qt.black)
        self.linewidth = 1
        self.fill = False
        self.fillcolor = QColor(Qt.white)

    def toDisplayString(self):
        """
        Creates a string representing the object for display in the annotation list.

        :return: Information display string.
        """
        rettext = 'Rectangle: (' + str(self.xpos) + ', ' + str(self.ypos) + ') - ('
        rettext += str(self.width) + ', ' + str(self.height) + ')'
        if not self.show:
            rettext += '  (Hidden)'
        return rettext

    def toList(self):
        """
        Saves the object attributes to a list for saving to a file.

        :return: List of attributes.
        """
        datalist = ['RectangleObject']
        datalist.append(self.show)
        datalist.append(self.xpos)
        datalist.append(self.ypos)
        datalist.append(self.width)
        datalist.append(self.height)
        datalist.append(self.cornerrad)
        datalist.append(self.color.rgba())
        datalist.append(self.linewidth)
        datalist.append(self.fill)
        datalist.append(self.fillcolor.rgba())
        return datalist

    def fromList(self, datalist):
        """
        Loads the object attributes from a list that was stored in a file.

        :param datalist: List of object attributes to be loaded.  List is of the same format as with the
        toList function.
        :return:  None
        """
        self.show = datalist[1]
        self.xpos = datalist[2]
        self.ypos = datalist[3]
        self.width = datalist[4]
        self.height = datalist[5]
        self.cornerrad = datalist[6]
        self.color = QColor(Qt.black)
        self.color.setRgba(datalist[7])
        self.linewidth = datalist[8]
        self.fill = datalist[9]
        self.fillcolor = QColor(Qt.black)
        self.fillcolor.setRgba(datalist[10])

class EllipseObject():
    def __init__(self):
        """
        Object for storing the attributes of an ellipse annotation.
        """
        self.show = True
        self.xpos = 0
        self.ypos = 0
        self.width = 100
        self.height = 100
        self.color = QColor(Qt.black)
        self.linewidth = 1
        self.fill = False
        self.fillcolor = QColor(Qt.white)

    def toDisplayString(self):
        """
        Creates a string representing the object for display in the annotation list.

        :return: Information display string.
        """
        rettext = 'Ellipse: (' + str(self.xpos) + ', ' + str(self.ypos) + ') - ('
        rettext += str(self.width) + ', ' + str(self.height) + ')'
        if not self.show:
            rettext += '  (Hidden)'
        return rettext

    def toList(self):
        """
        Saves the object attributes to a list for saving to a file.

        :return: List of attributes.
        """
        datalist = ['EllipseObject']
        datalist.append(self.show)
        datalist.append(self.xpos)
        datalist.append(self.ypos)
        datalist.append(self.width)
        datalist.append(self.height)
        datalist.append(self.color.rgba())
        datalist.append(self.linewidth)
        datalist.append(self.fill)
        datalist.append(self.fillcolor.rgba())
        return datalist

    def fromList(self, datalist):
        """
        Loads the object attributes from a list that was stored in a file.

        :param datalist: List of object attributes to be loaded.  List is of the same format as with the
        toList function.
        :return:  None
        """
        self.show = datalist[1]
        self.xpos = datalist[2]
        self.ypos = datalist[3]
        self.width = datalist[4]
        self.height = datalist[5]
        self.color = QColor(Qt.black)
        self.color.setRgba(datalist[6])
        self.linewidth = datalist[7]
        self.fill = datalist[8]
        self.fillcolor = QColor(Qt.black)
        self.fillcolor.setRgba(datalist[9])

## Graphics Objects Edit Panels

class TextBoxOptions(QWidget):
    changeMade = Signal()

    def __init__(self, parent=None):
        """
        Widget for displaying the properties of the text annotation object.

        :param parent: Parent object.
        """
        super().__init__(parent)

        self.textobj = None

        self.showItem = QCheckBox()
        self.showItem.clicked.connect(self.objChanged)

        self.textEditor = QPlainTextEdit()
        self.textEditor.textChanged.connect(self.objChanged)
        self.textEditor.setMaximumHeight(100)
        self.textEditor.setWordWrapMode(QTextOption.WrapMode.NoWrap)

        self.fontsize = QSpinBox()
        self.fontsize.setMinimum(5)
        self.fontsize.setMaximum(100)
        self.fontsize.setValue(12)
        self.fontsize.setMinimumWidth(100)
        self.fontsize.setMaximumWidth(100)
        self.fontsize.valueChanged.connect(self.objChanged)

        self.font = QFont()

        fontButton = QPushButton('Edit Font')
        fontButton.clicked.connect(self.editFont)

        self.textColor = ColorSelectButtonBox()
        self.textColor.colorChange.connect(self.objChanged)
        self.textColor.setMaximumWidth(50)

        self.xslider = QSlider(Qt.Orientation.Horizontal)
        self.xslider.valueChanged.connect(self.objChanged)

        xslidertools = self.createXPosToolbar()
        xslidertools.setContentsMargins(0, 0, 0, 0)
        xslidertoolsLayout = QHBoxLayout()
        xslidertoolsLayout.addWidget(self.xslider)
        xslidertoolsLayout.addWidget(xslidertools)
        xslidertoolsLayout.setContentsMargins(0, 0, 0, 0)

        self.yslider = QSlider(Qt.Orientation.Horizontal)
        self.yslider.valueChanged.connect(self.objChanged)

        yslidertools = self.createYPosToolbar()
        yslidertools.setContentsMargins(0, 0, 0, 0)
        yslidertoolsLayout = QHBoxLayout()
        yslidertoolsLayout.addWidget(self.yslider)
        yslidertoolsLayout.addWidget(yslidertools)
        yslidertoolsLayout.setContentsMargins(0, 0, 0, 0)

        self.justLeft = QRadioButton('Left')
        self.justCenter = QRadioButton('Center')
        self.justRight = QRadioButton('Right')
        jbg = QButtonGroup()
        jbg.addButton(self.justRight)
        jbg.addButton(self.justCenter)
        jbg.addButton(self.justLeft)
        self.justLeft.setChecked(True)
        self.justLeft.clicked.connect(self.objChanged)
        self.justCenter.clicked.connect(self.objChanged)
        self.justRight.clicked.connect(self.objChanged)
        justifyselectors = QHBoxLayout()
        justifyselectors.addWidget(self.justLeft)
        justifyselectors.addWidget(self.justCenter)
        justifyselectors.addWidget(self.justRight)
        justifyselectors.addStretch(1)

        self.includeBox = QCheckBox()
        self.includeBox.clicked.connect(self.objChanged)

        self.backgroundColor = ColorSelectButtonBox()
        self.backgroundColor.colorChange.connect(self.objChanged)
        self.backgroundColor.setMaximumWidth(50)
        self.backgroundColor.setColor(QColor(255,255,255))

        self.borderColor = ColorSelectButtonBox()
        self.borderColor.colorChange.connect(self.objChanged)
        self.borderColor.setMaximumWidth(50)

        self.borderWidth = QSpinBox()
        self.borderWidth.setMinimum(0)
        self.borderWidth.setMaximum(100)
        self.borderWidth.setValue(1)
        self.borderWidth.setMinimumWidth(100)
        self.borderWidth.setMaximumWidth(100)
        self.borderWidth.valueChanged.connect(self.objChanged)

        self.XPadding = QSpinBox()
        self.XPadding.setMinimum(0)
        self.XPadding.setMaximum(100)
        self.XPadding.setValue(0)
        self.XPadding.setMinimumWidth(100)
        self.XPadding.setMaximumWidth(100)
        self.XPadding.valueChanged.connect(self.objChanged)

        self.YPadding = QSpinBox()
        self.YPadding.setMinimum(0)
        self.YPadding.setMaximum(100)
        self.YPadding.setValue(0)
        self.YPadding.setMinimumWidth(100)
        self.YPadding.setMaximumWidth(100)
        self.YPadding.valueChanged.connect(self.objChanged)

        self.rotateslider = QSlider(Qt.Orientation.Horizontal)
        self.rotateslider.valueChanged.connect(self.objChanged)
        self.rotateslider.setMinimum(-360)
        self.rotateslider.setMaximum(360)
        self.rotateslider.setValue(0)

        rotationtools = self.createRotationToolbar()
        rotationtools.setContentsMargins(0, 0, 0, 0)
        RotationLayout = QHBoxLayout()
        RotationLayout.addWidget(self.rotateslider)
        RotationLayout.addWidget(rotationtools)
        RotationLayout.setContentsMargins(0, 0, 0, 0)

        self.transparentslider = QSlider(Qt.Orientation.Horizontal)
        self.transparentslider.valueChanged.connect(self.objChanged)
        self.transparentslider.setMinimum(0)
        self.transparentslider.setMaximum(1000)
        self.transparentslider.setValue(0)

        inputs = QGridLayout()
        inputs.addWidget(QLabel("Show: "), 0, 0, Qt.AlignRight)
        inputs.addWidget(self.showItem, 0, 1)
        inputs.addWidget(QLabel("Text: "), 1, 0, Qt.AlignRight)
        inputs.addWidget(self.textEditor, 1, 1)
        inputs.addWidget(QLabel("Text Color: "), 2, 0, Qt.AlignRight)
        inputs.addWidget(self.textColor, 2, 1)
        inputs.addWidget(QLabel("Font: "), 3, 0, Qt.AlignRight)
        inputs.addWidget(fontButton, 3, 1)
        inputs.addWidget(QLabel("Font Size: "), 4, 0, Qt.AlignRight)
        inputs.addWidget(self.fontsize, 4, 1)

        inputs.addWidget(QHLine(), 5, 0, 1, 2)

        inputs.addWidget(QLabel("Anchor X Position: "), 6, 0, Qt.AlignRight)
        inputs.addLayout(xslidertoolsLayout, 6, 1)
        inputs.addWidget(QLabel("Anchor Y Position: "), 7, 0, Qt.AlignRight)
        inputs.addLayout(yslidertoolsLayout, 7, 1)

        inputs.addWidget(QHLine(), 8, 0, 1, 2)

        inputs.addWidget(QLabel("Justify: "), 9, 0, Qt.AlignRight)
        inputs.addLayout(justifyselectors, 9, 1)

        inputs.addWidget(QHLine(), 10, 0, 1, 2)

        inputs.addWidget(QLabel("Include Box: "), 11, 0, Qt.AlignRight)
        inputs.addWidget(self.includeBox, 11, 1)

        inputs.addWidget(QLabel("Background Color: "), 12, 0, Qt.AlignRight)
        inputs.addWidget(self.backgroundColor, 12, 1)

        inputs.addWidget(QLabel("Border Color: "), 15, 0, Qt.AlignRight)
        inputs.addWidget(self.borderColor, 15, 1)

        inputs.addWidget(QLabel("Border Width: "), 16, 0, Qt.AlignRight)
        inputs.addWidget(self.borderWidth, 16, 1)

        inputs.addWidget(QHLine(), 17, 0, 1, 2)

        inputs.addWidget(QLabel("Horizontal Padding: "), 18, 0, Qt.AlignRight)
        inputs.addWidget(self.XPadding, 18, 1)

        inputs.addWidget(QLabel("Vertical Padding: "), 19, 0, Qt.AlignRight)
        inputs.addWidget(self.YPadding, 19, 1)

        inputs.addWidget(QHLine(), 22, 0, 1, 2)

        inputs.addWidget(QLabel("Rotation: "), 23, 0, Qt.AlignRight)
        inputs.addLayout(RotationLayout, 23, 1)

        inputs.addWidget(QLabel("Transparency: "), 24, 0, Qt.AlignRight)
        inputs.addWidget(self.transparentslider, 24, 1)

        centerlayoutV = QVBoxLayout()
        centerlayoutV.addLayout(inputs)
        centerlayoutV.addStretch(1)

        centerlayout = QHBoxLayout()
        centerlayout.addLayout(centerlayoutV)
        centerlayout.addStretch(1)
        self.setLayout(centerlayout)

    def resource_path(self, relative_path):
        """
        Creates a system path that is relative to the position of the running application.

        :param relative_path: The relative path of the file from the base position of the running application.
        :return: The full OS path.
        """
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

    def createRotationToolbar(self):
        """
        Creates the rotation toolbar for the rotation slider.

        :return: Toolbar
        """
        Reset_act = QAction(QIcon(self.resource_path('icons/Center.png')), "Reset the Rotation to 0", self)
        Reset_act.setStatusTip('Reset the rotation to 0.')
        Reset_act.triggered.connect(self.ResetRotation)

        Plus90_act = QAction(QIcon(self.resource_path('icons/zoomin.png')), "Add 90 Degrees", self)
        Plus90_act.setStatusTip('Add 90 degrees to the rotation.')
        Plus90_act.triggered.connect(self.Add90Rotation)

        Minus90_act = QAction(QIcon(self.resource_path('icons/zoomout.png')), "Subtract 90 Degrees", self)
        Minus90_act.setStatusTip('Subtract 90 degrees to the rotation.')
        Minus90_act.triggered.connect(self.Subtract90Rotation)

        tool_bar = QToolBar("Rotation Toolbar")
        tool_bar.setIconSize(QSize(14, 14))
        tool_bar.setMovable(False)
        tool_bar.addAction(Reset_act)
        tool_bar.addAction(Plus90_act)
        tool_bar.addAction(Minus90_act)
        return tool_bar

    def createXPosToolbar(self):
        """
        Creates the X Position toolbar for the position slider.

        :return: Toolbar
        """
        Reset_act = QAction(QIcon(self.resource_path('icons/Axes2.png')), "Reset the X Anchor Position", self)
        Reset_act.setStatusTip('Reset the X anchor position to 0.')
        Reset_act.triggered.connect(self.ResetXPos)

        tool_bar = QToolBar("X Position Toolbar")
        tool_bar.setIconSize(QSize(14, 14))
        tool_bar.setMovable(False)
        tool_bar.addAction(Reset_act)
        return tool_bar

    def createYPosToolbar(self):
        """
        Creates the Y Position toolbar for the position slider.

        :return: Toolbar
        """
        Reset_act = QAction(QIcon(self.resource_path('icons/Axes2.png')), "Reset the Y Anchor Position", self)
        Reset_act.setStatusTip('Reset the Y anchor position to 0.')
        Reset_act.triggered.connect(self.ResetYPos)

        tool_bar = QToolBar("Y Position Toolbar")
        tool_bar.setIconSize(QSize(14, 14))
        tool_bar.setMovable(False)
        tool_bar.addAction(Reset_act)
        return tool_bar

    def ResetXPos(self):
        """ Resets the x-slider to 0. """
        self.xslider.setValue(0)

    def ResetYPos(self):
        """ Resets the y-slider to 0. """
        self.yslider.setValue(0)

    def ResetRotation(self):
        """ Resets the rotation to 0. """
        self.rotateslider.setValue(0)

    def Add90Rotation(self):
        """ Adds 90 degrees the rotation. """
        val = self.rotateslider.value()
        self.rotateslider.setValue(val + 90)

    def Subtract90Rotation(self):
        """ Subtracts 90 degrees the rotation. """
        val = self.rotateslider.value()
        self.rotateslider.setValue(val - 90)

    def editFont(self):
        """
        UI for selecting the font of the text annotation.

        :return: None
        """
        dialog = QFontDialog(self)
        dialog.setCurrentFont(self.font)
        if dialog.exec():
            self.BlockAllSignals(True)
            self.font = dialog.selectedFont()
            self.fontsize.setValue(self.font.pointSize())
            self.BlockAllSignals(False)
            self.objChanged()

    def objChanged(self):
        """
        Sets the object attributes to the UI values.

        :return: None
        """
        self.textobj.show = self.showItem.isChecked()
        self.textobj.text = self.textEditor.toPlainText()
        self.textobj.xpos = self.xslider.value()
        self.textobj.ypos = self.yslider.value()
        self.textobj.font = self.font
        self.textobj.font.setPointSize(self.fontsize.value())
        self.textobj.color = self.textColor.color

        if self.justLeft.isChecked():
            self.textobj.justify = 'left'
        elif self.justCenter.isChecked():
            self.textobj.justify = 'center'
        if self.justRight.isChecked():
            self.textobj.justify = 'right'

        self.textobj.includeBox = self.includeBox.isChecked()
        self.textobj.backgroundColor = self.backgroundColor.color
        self.textobj.borderColor = self.borderColor.color
        self.textobj.borderWidth = self.borderWidth.value()
        self.textobj.xPadding = self.XPadding.value()
        self.textobj.yPadding = self.YPadding.value()
        self.textobj.transparency = self.transparentslider.value() / 1000
        self.textobj.rotation = self.rotateslider.value()
        self.setSliderMinimumsToImageSize()
        self.changeMade.emit()

    def BlockAllSignals(self, b):
        """
        Helper function to block update signals for the UI.

        :param b: Boolean for the blocking.
        :return: None
        """
        for obj in self.findChildren(QWidget):
            try:
                obj.blockSignals(b)
            except:
                pass

    def setImageSize(self, size):
        """
        Sets the size sliders to match the size of the image.

        :param size: Size of the image.
        :return: None
        """
        self.xslider.setMaximum(size.width())
        self.yslider.setMaximum(size.height())

    def setObject(self, txtobj):
        """
        Sets the UI values to match the object values.

        :param txtobj: Annotation object to load.
        :return: None
        """
        self.BlockAllSignals(True)
        self.textobj = txtobj
        self.showItem.setChecked(self.textobj.show)
        self.textEditor.setPlainText(self.textobj.text)
        self.font = self.textobj.font
        self.fontsize.setValue(self.textobj.font.pointSize())
        self.xslider.setValue(self.textobj.xpos)
        self.yslider.setValue(self.textobj.ypos)
        self.textColor.setColor(self.textobj.color)

        if self.textobj.justify == 'left':
            self.justLeft.setChecked(True)
        elif self.textobj.justify == 'center':
            self.justCenter.setChecked(True)
        elif self.textobj.justify == 'right':
            self.justRight.setChecked(True)

        self.includeBox.setChecked(self.textobj.includeBox)
        self.backgroundColor.setColor(QColor(self.textobj.backgroundColor.red(), self.textobj.backgroundColor.green(),
                                             self.textobj.backgroundColor.blue()))
        self.borderColor.setColor(QColor(self.textobj.borderColor.red(), self.textobj.borderColor.green(),
                                         self.textobj.borderColor.blue()))

        self.borderWidth.setValue(self.textobj.borderWidth)
        self.XPadding.setValue(self.textobj.xPadding)
        self.YPadding.setValue(self.textobj.yPadding)
        self.transparentslider.setValue(int(self.textobj.transparency*1000))
        self.rotateslider.setValue(self.textobj.rotation)
        self.setSliderMinimumsToImageSize()
        self.BlockAllSignals(False)
        self.changeMade.emit()

    def setSliderMinimumsToImageSize(self):
        """
        Resets the minimum for the position sliders do that the anchor point can be off the image.

        :return: None
        """
        self.BlockAllSignals(True)
        strlst = self.textobj.text.split('\n')
        fm = QFontMetrics(self.textobj.font)
        fontheight = fm.lineSpacing()
        numlines = len(strlst)
        maxAdvance = 0
        for line in strlst:
            maxAdvance = max(maxAdvance, fm.horizontalAdvance(line))

        self.xslider.setMinimum(-int(maxAdvance + 2 * (self.textobj.xPadding + self.textobj.borderWidth)))
        self.yslider.setMinimum(-int(fontheight) * numlines - 2 * (self.textobj.yPadding + self.textobj.borderWidth))
        self.BlockAllSignals(False)

    def UpdateShow(self, b):
        """
        Updates the showing of the object.

        :param b: Boolean for the showing.
        :return: None
        """
        self.showItem.setChecked(b)


class ImageOptions(QWidget):
    changeMade = Signal()

    def __init__(self, parent=None):
        """
        Widget for displaying the properties of the image annotation object.

        :param parent: Parent object.
        """
        super().__init__(parent)

        self.imageobj = None
        self.clipboard = QApplication.clipboard()

        self.showItem = QCheckBox()
        self.showItem.clicked.connect(self.objChanged)

        self.imageViewer = Canvas()
        self.imageViewer.setFixedHeight(100)
        self.imageViewer.setFixedWidth(200)

        imageViewerContainer = QFrame()
        imageViewerContainer.setStyleSheet("border: 1px solid black")
        imageViewerContainer.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        imageViewerContainer.setLineWidth(1)
        imageViewerContainerLayout = QHBoxLayout()
        imageViewerContainerLayout.addWidget(self.imageViewer)
        imageViewerContainerLayout.setContentsMargins(0,0,0,0)
        imageViewerContainer.setLayout(imageViewerContainerLayout)

        self.toolbar = self.createImageToolbar()
        self.toolbar.setContentsMargins(0,0,0,0)

        self.xslider = QSlider(Qt.Orientation.Horizontal)
        self.xslider.valueChanged.connect(self.objChanged)

        xslidertools = self.createXPosToolbar()
        xslidertools.setContentsMargins(0, 0, 0, 0)
        xslidertoolsLayout = QHBoxLayout()
        xslidertoolsLayout.addWidget(self.xslider)
        xslidertoolsLayout.addWidget(xslidertools)
        xslidertoolsLayout.setContentsMargins(0, 0, 0, 0)

        self.yslider = QSlider(Qt.Orientation.Horizontal)
        self.yslider.valueChanged.connect(self.objChanged)

        yslidertools = self.createYPosToolbar()
        yslidertools.setContentsMargins(0, 0, 0, 0)
        yslidertoolsLayout = QHBoxLayout()
        yslidertoolsLayout.addWidget(self.yslider)
        yslidertoolsLayout.addWidget(yslidertools)
        yslidertoolsLayout.setContentsMargins(0, 0, 0, 0)

        self.scaleslider = QSlider(Qt.Orientation.Horizontal)
        self.scaleslider.valueChanged.connect(self.objChanged)
        self.scaleslider.setMaximum(1000)
        self.scaleslider.setValue(500)

        scaletools = self.createScaleToolbar()
        scaletools.setContentsMargins(0,0,0,0)
        ScaleLayout = QHBoxLayout()
        ScaleLayout.addWidget(self.scaleslider)
        ScaleLayout.addWidget(scaletools)
        ScaleLayout.setContentsMargins(0, 0, 0, 0)

        self.aspectslider = QSlider(Qt.Orientation.Horizontal)
        self.aspectslider.valueChanged.connect(self.objChanged)
        self.aspectslider.setMinimum(0)
        self.aspectslider.setMaximum(1000)
        self.aspectslider.setValue(500)

        aspecttools = self.createAspectToolbar()
        aspecttools.setContentsMargins(0,0,0,0)
        AspectLayout = QHBoxLayout()
        AspectLayout.addWidget(self.aspectslider)
        AspectLayout.addWidget(aspecttools)
        AspectLayout.setContentsMargins(0, 0, 0, 0)

        self.useTransColor = QCheckBox()
        self.useTransColor.clicked.connect(self.objChanged)

        self.transColor = ColorSelectButtonBox()
        self.transColor.colorChange.connect(self.objChanged)
        self.transColor.setMaximumWidth(50)
        self.transColor.setColor(QColor(255, 255, 255))

        self.flipH = QCheckBox()
        self.flipH.clicked.connect(self.objChanged)

        self.flipV = QCheckBox()
        self.flipV.clicked.connect(self.objChanged)

        self.rotateslider = QSlider(Qt.Orientation.Horizontal)
        self.rotateslider.valueChanged.connect(self.objChanged)
        self.rotateslider.setMinimum(-360)
        self.rotateslider.setMaximum(360)
        self.rotateslider.setValue(0)

        rotationtools = self.createRotationToolbar()
        rotationtools.setContentsMargins(0, 0, 0, 0)
        RotationLayout = QHBoxLayout()
        RotationLayout.addWidget(self.rotateslider)
        RotationLayout.addWidget(rotationtools)
        RotationLayout.setContentsMargins(0, 0, 0, 0)

        self.transparentslider = QSlider(Qt.Orientation.Horizontal)
        self.transparentslider.valueChanged.connect(self.objChanged)
        self.transparentslider.setMinimum(0)
        self.transparentslider.setMaximum(1000)
        self.transparentslider.setValue(0)

        self.includeBox = QCheckBox()
        self.includeBox.clicked.connect(self.objChanged)

        self.backgroundColor = ColorSelectButtonBox()
        self.backgroundColor.colorChange.connect(self.objChanged)
        self.backgroundColor.setMaximumWidth(50)
        self.backgroundColor.setColor(QColor(255,255,255))

        self.borderColor = ColorSelectButtonBox()
        self.borderColor.colorChange.connect(self.objChanged)
        self.borderColor.setMaximumWidth(50)

        self.borderWidth = QSpinBox()
        self.borderWidth.setMinimum(0)
        self.borderWidth.setMaximum(100)
        self.borderWidth.setValue(1)
        self.borderWidth.setMinimumWidth(100)
        self.borderWidth.setMaximumWidth(100)
        self.borderWidth.valueChanged.connect(self.objChanged)

        self.XPadding = QSpinBox()
        self.XPadding.setMinimum(0)
        self.XPadding.setMaximum(100)
        self.XPadding.setValue(0)
        self.XPadding.setMinimumWidth(100)
        self.XPadding.setMaximumWidth(100)
        self.XPadding.valueChanged.connect(self.objChanged)

        self.YPadding = QSpinBox()
        self.YPadding.setMinimum(0)
        self.YPadding.setMaximum(100)
        self.YPadding.setValue(0)
        self.YPadding.setMinimumWidth(100)
        self.YPadding.setMaximumWidth(100)
        self.YPadding.valueChanged.connect(self.objChanged)

        inputs = QGridLayout()
        inputs.addWidget(QLabel("Show: "), 0, 0, Qt.AlignRight)
        inputs.addWidget(self.showItem, 0, 1)

        inputs.addWidget(self.toolbar, 1, 1)

        inputs.addWidget(QLabel("Image: "), 2, 0, Qt.AlignRight)
        inputs.addWidget(imageViewerContainer, 2, 1)

        inputs.addWidget(QHLine(), 5, 0, 1, 2)

        inputs.addWidget(QLabel("Anchor X Position: "), 6, 0, Qt.AlignRight)
        inputs.addLayout(xslidertoolsLayout, 6, 1)
        inputs.addWidget(QLabel("Anchor Y Position: "), 7, 0, Qt.AlignRight)
        inputs.addLayout(yslidertoolsLayout, 7, 1)

        inputs.addWidget(QHLine(), 8, 0, 1, 2)

        inputs.addWidget(QLabel("Scaling: "), 9, 0, Qt.AlignRight)
        inputs.addLayout(ScaleLayout, 9, 1)

        inputs.addWidget(QLabel("Aspect Ratio: "), 10, 0, Qt.AlignRight)
        inputs.addLayout(AspectLayout, 10, 1)

        inputs.addWidget(QLabel("Flip Horizontally: "), 11, 0, Qt.AlignRight)
        inputs.addWidget(self.flipH, 11, 1)

        inputs.addWidget(QLabel("Flip Vertically: "), 12, 0, Qt.AlignRight)
        inputs.addWidget(self.flipV, 12, 1)

        inputs.addWidget(QLabel("Rotation: "), 13, 0, Qt.AlignRight)
        inputs.addLayout(RotationLayout, 13, 1)

        inputs.addWidget(QHLine(), 100, 0, 1, 2)

        inputs.addWidget(QLabel("Use Transparent Color: "), 101, 0, Qt.AlignRight)
        inputs.addWidget(self.useTransColor, 101, 1)

        inputs.addWidget(QLabel("Transparent Color: "), 102, 0, Qt.AlignRight)
        inputs.addWidget(self.transColor, 102, 1)

        inputs.addWidget(QHLine(), 103, 0, 1, 2)

        inputs.addWidget(QLabel("Image Transparency: "), 200, 0, Qt.AlignRight)
        inputs.addWidget(self.transparentslider, 200, 1)

        inputs.addWidget(QHLine(), 201, 0, 1, 2)

        inputs.addWidget(QLabel("Include Box: "), 211, 0, Qt.AlignRight)
        inputs.addWidget(self.includeBox, 211, 1)

        inputs.addWidget(QLabel("Padding Color: "), 212, 0, Qt.AlignRight)
        inputs.addWidget(self.backgroundColor, 212, 1)

        inputs.addWidget(QLabel("Border Color: "), 215, 0, Qt.AlignRight)
        inputs.addWidget(self.borderColor, 215, 1)

        inputs.addWidget(QLabel("Border Width: "), 216, 0, Qt.AlignRight)
        inputs.addWidget(self.borderWidth, 216, 1)

        inputs.addWidget(QLabel("Horizontal Padding: "), 218, 0, Qt.AlignRight)
        inputs.addWidget(self.XPadding, 218, 1)

        inputs.addWidget(QLabel("Vertical Padding: "), 219, 0, Qt.AlignRight)
        inputs.addWidget(self.YPadding, 219, 1)

        centerlayoutV = QVBoxLayout()
        centerlayoutV.addLayout(inputs)
        centerlayoutV.addStretch(1)

        centerlayout = QHBoxLayout()
        centerlayout.addLayout(centerlayoutV)
        centerlayout.addStretch(1)
        self.setLayout(centerlayout)

    def resource_path(self, relative_path):
        """
        Creates a system path that is relative to the position of the running application.

        :param relative_path: The relative path of the file from the base position of the running application.
        :return: The full OS path.
        """
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

    def createImageToolbar(self):
        """
        Creates the toolbar for the image loading.

        :return: Toolbar
        """
        openImage_act = QAction(QIcon(self.resource_path('icons/FileOpen.png')), "Open Image File...", self)
        openImage_act.setStatusTip('Open an image file.')
        openImage_act.triggered.connect(self.openImageFile)

        pasteImage_act = QAction(QIcon(self.resource_path('icons/paste.png')), "Paste Image", self)
        pasteImage_act.setStatusTip('Paste an image from the clipboard.')
        pasteImage_act.triggered.connect(self.pasteImage)

        tool_bar = QToolBar("Image Toolbar")
        tool_bar.setIconSize(QSize(18, 18))
        tool_bar.setMovable(False)
        tool_bar.addAction(openImage_act)
        tool_bar.addAction(pasteImage_act)
        return tool_bar

    def createScaleToolbar(self):
        """
        Creates the toolbar for the scaling.

        :return: Toolbar
        """
        ScaleImageTo1_act = QAction(QIcon(self.resource_path('icons/zoom1t1.png')), "Set Scale Factor to 1", self)
        ScaleImageTo1_act.setStatusTip('Set the scaling factor to 1.')
        ScaleImageTo1_act.triggered.connect(self.ScaleImageTo1)

        tool_bar = QToolBar("Scale Toolbar")
        tool_bar.setIconSize(QSize(14, 14))
        tool_bar.setMovable(False)
        tool_bar.addAction(ScaleImageTo1_act)
        return tool_bar

    def createAspectToolbar(self):
        """
        Creates the toolbar for the aspect ratio.

        :return: Toolbar
        """
        AspectImageTo1_act = QAction(QIcon(self.resource_path('icons/zoom1t1.png')), "Set Aspect Ratio to 1:1", self)
        AspectImageTo1_act.setStatusTip('Set the aspect ratio to 1:1.')
        AspectImageTo1_act.triggered.connect(self.AspectImageTo1)

        tool_bar = QToolBar("Aspect Ratio Toolbar")
        tool_bar.setIconSize(QSize(14, 14))
        tool_bar.setMovable(False)
        tool_bar.addAction(AspectImageTo1_act)
        return tool_bar

    def createXPosToolbar(self):
        """
        Creates the toolbar for the x anchor position.

        :return: Toolbar
        """
        Reset_act = QAction(QIcon(self.resource_path('icons/Axes2.png')), "Reset the X Anchor Position", self)
        Reset_act.setStatusTip('Reset the X anchor position to 0.')
        Reset_act.triggered.connect(self.ResetXPos)

        tool_bar = QToolBar("X Position Toolbar")
        tool_bar.setIconSize(QSize(14, 14))
        tool_bar.setMovable(False)
        tool_bar.addAction(Reset_act)
        return tool_bar

    def createYPosToolbar(self):
        """
        Creates the toolbar for the y anchor position.

        :return: Toolbar
        """
        Reset_act = QAction(QIcon(self.resource_path('icons/Axes2.png')), "Reset the Y Anchor Position", self)
        Reset_act.setStatusTip('Reset the Y anchor position to 0.')
        Reset_act.triggered.connect(self.ResetYPos)

        tool_bar = QToolBar("Y Position Toolbar")
        tool_bar.setIconSize(QSize(14, 14))
        tool_bar.setMovable(False)
        tool_bar.addAction(Reset_act)
        return tool_bar

    def createRotationToolbar(self):
        """
        Creates the toolbar for the rotation.

        :return: Toolbar
        """
        Reset_act = QAction(QIcon(self.resource_path('icons/Center.png')), "Reset the Rotation to 0", self)
        Reset_act.setStatusTip('Reset the rotation to 0.')
        Reset_act.triggered.connect(self.ResetRotation)

        Plus90_act = QAction(QIcon(self.resource_path('icons/zoomin.png')), "Add 90 Degrees", self)
        Plus90_act.setStatusTip('Add 90 degrees to the rotation.')
        Plus90_act.triggered.connect(self.Add90Rotation)

        Minus90_act = QAction(QIcon(self.resource_path('icons/zoomout.png')), "Subtract 90 Degrees", self)
        Minus90_act.setStatusTip('Subtract 90 degrees to the rotation.')
        Minus90_act.triggered.connect(self.Subtract90Rotation)

        tool_bar = QToolBar("Rotation Toolbar")
        tool_bar.setIconSize(QSize(14, 14))
        tool_bar.setMovable(False)
        tool_bar.addAction(Reset_act)
        tool_bar.addAction(Plus90_act)
        tool_bar.addAction(Minus90_act)
        return tool_bar

    def ScaleImageTo1(self):
        """ Sets the scaling factor to 1. """
        self.scaleslider.setValue(500)

    def AspectImageTo1(self):
        """ Sets the aspect ratio to 1:1. """
        self.aspectslider.setValue(500)

    def ResetXPos(self):
        """ Sets the x anchor position to 1. """
        self.xslider.setValue(0)

    def ResetRotation(self):
        """ Sets the rotation to 0. """
        self.rotateslider.setValue(0)

    def Add90Rotation(self):
        """ Adds 90 degrees to the rotation. """
        val = self.rotateslider.value()
        self.rotateslider.setValue(val + 90)

    def Subtract90Rotation(self):
        """ Subtracts 90 degrees to the rotation. """
        val = self.rotateslider.value()
        self.rotateslider.setValue(val - 90)

    def ResetYPos(self):
        """ Sets the y anchor position to 1. """
        self.yslider.setValue(0)

    def openImageFile(self):
        """
        Opens an image to be loaded and displayed.

        :return: None
        """
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "",
                                                   "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*.*)")

        try:
            if file_name:
                t = QImage()
                t.load(file_name)
                self.setImage(t)
                self.setSliderMinimumsToImageSize()
        except:
            # traceback.print_exc()
            QMessageBox.warning(self, "File Not Opened", "The file " + file_name + " could not be opened.",
                                QMessageBox.Ok)

    def pasteImage(self):
        """ Pastes an image from the clipboard. """
        img = self.clipboard.image()
        self.setImage(img)
        self.setSliderMinimumsToImageSize()

    def setImage(self, img):
        """ Sets the image. """
        self.imageobj.image = img
        self.imageViewer.setImage(img)
        self.changeMade.emit()

    def objChanged(self):
        """
        Sets the object attributes to the UI values.

        :return: None
        """
        try:
            self.imageobj.show = self.showItem.isChecked()
            self.imageobj.xpos = self.xslider.value()
            self.imageobj.ypos = self.yslider.value()
            self.imageViewer.setImage(self.imageobj.image)

            sc = self.scaleslider.value()
            self.imageobj.scale = 10 ** (sc / 500 - 1)

            self.imageobj.useTransparentColor = self.useTransColor.isChecked()
            self.imageobj.transparentColor = self.transColor.color

            ar = self.aspectslider.value()
            self.imageobj.aspectratio = 10**(ar/500 - 1)

            self.imageobj.FlipHorizontal = self.flipH.isChecked()
            self.imageobj.FlipVertical = self.flipV.isChecked()

            self.imageobj.rotation = self.rotateslider.value()
            self.imageobj.transparency = self.transparentslider.value()/1000
            self.imageobj.includeBox = self.includeBox.isChecked()
            self.imageobj.backgroundColor = self.backgroundColor.color
            self.imageobj.borderColor = self.borderColor.color
            self.imageobj.borderWidth = self.borderWidth.value()
            self.imageobj.xPadding = self.XPadding.value()
            self.imageobj.yPadding = self.YPadding.value()
            self.setSliderMinimumsToImageSize()
        except:
            pass

        self.changeMade.emit()

    def BlockAllSignals(self, b):
        """
        Helper function to block update signals for the UI.

        :param b: Boolean for the blocking.
        :return: None
        """
        for obj in self.findChildren(QWidget):
            try:
                obj.blockSignals(b)
            except:
                pass

    def setSliderMinimumsToImageSize(self):
        """ Sets the minimum for the anchor sliders so that the image anchor can be off the screen. """
        self.BlockAllSignals(True)
        imgsize = self.imageobj.image.size()
        neww = (imgsize.width() * self.imageobj.scale * self.imageobj.aspectratio +
                2*(self.imageobj.xPadding + self.imageobj.borderWidth))
        newh = (imgsize.height() * self.imageobj.scale / self.imageobj.aspectratio +
                2*(self.imageobj.yPadding + self.imageobj.borderWidth))

        self.xslider.setMinimum(-int(neww))
        self.yslider.setMinimum(-int(newh))
        self.BlockAllSignals(False)

    def setImageSize(self, size):
        """
        Sets the size sliders to match the size of the image.

        :param size: Size of the image.
        :return: None
        """
        self.BlockAllSignals(True)
        self.xslider.setMaximum(size.width())
        self.yslider.setMaximum(size.height())
        self.BlockAllSignals(False)

    def setObject(self, imageobj):
        """
        Sets the UI values to match the object values.

        :param imageobj: Annotation object to load.
        :return: None
        """
        self.BlockAllSignals(True)
        self.imageobj = imageobj
        self.showItem.setChecked(self.imageobj.show)

        self.xslider.setValue(self.imageobj.xpos)
        self.yslider.setValue(self.imageobj.ypos)
        self.imageViewer.setImage(self.imageobj.image)
        self.useTransColor.setChecked(self.imageobj.useTransparentColor)
        self.transColor.setColor(self.imageobj.transparentColor)
        self.scaleslider.setValue(int((log(self.imageobj.scale)/log(10) + 1) * 500))
        self.aspectslider.setValue(int((log(self.imageobj.aspectratio)/log(10) + 1) * 500))
        self.flipH.setChecked(self.imageobj.FlipHorizontal)
        self.flipV.setChecked(self.imageobj.FlipVertical)
        self.rotateslider.setValue(self.imageobj.rotation)
        self.setSliderMinimumsToImageSize()
        self.transparentslider.setValue(int(self.imageobj.transparency * 1000))
        self.includeBox.setChecked(self.imageobj.includeBox)
        self.backgroundColor.setColor(self.imageobj.backgroundColor)
        self.borderColor.setColor(self.imageobj.borderColor)
        self.borderWidth.setValue(self.imageobj.borderWidth)
        self.XPadding.setValue(self.imageobj.xPadding)
        self.YPadding.setValue(self.imageobj.yPadding)
        self.BlockAllSignals(False)
        self.changeMade.emit()

    def UpdateShow(self, b):
        """
        Updates the showing of the object.

        :param b: Boolean for the showing.
        :return: None
        """
        self.showItem.setChecked(b)


class LineOptions(QWidget):
    changeMade = Signal()

    def __init__(self, parent=None):
        """
        Widget for displaying the properties of the line object.

        :param parent: Parent object.
        """
        super().__init__(parent)

        self.lineobj = None

        self.showItem = QCheckBox()
        self.showItem.clicked.connect(self.objChanged)

        self.linewidth = QSpinBox()
        self.linewidth.setMinimum(1)
        self.linewidth.setMaximum(20)
        self.linewidth.setValue(1)
        self.linewidth.setMinimumWidth(100)
        self.linewidth.setMaximumWidth(100)
        self.linewidth.valueChanged.connect(self.objChanged)

        self.lineColor = ColorSelectButtonBox()
        self.lineColor.colorChange.connect(self.objChanged)
        self.lineColor.setMaximumWidth(50)

        sliderWidth = 200

        self.startxslider = QSlider(Qt.Orientation.Horizontal)
        self.startxslider.valueChanged.connect(self.objChanged)
        self.startxslider.setMinimumWidth(sliderWidth)

        self.startyslider = QSlider(Qt.Orientation.Horizontal)
        self.startyslider.valueChanged.connect(self.objChanged)
        self.startyslider.setMinimumWidth(sliderWidth)

        self.endxslider = QSlider(Qt.Orientation.Horizontal)
        self.endxslider.valueChanged.connect(self.objChanged)
        self.endxslider.setMinimumWidth(sliderWidth)

        self.endyslider = QSlider(Qt.Orientation.Horizontal)
        self.endyslider.valueChanged.connect(self.objChanged)
        self.endyslider.setMinimumWidth(sliderWidth)

        inputs = QGridLayout()
        inputs.addWidget(QLabel("Show: "), 0, 0, Qt.AlignRight)
        inputs.addWidget(self.showItem, 0, 1)
        inputs.addWidget(QLabel("Color: "), 2, 0, Qt.AlignRight)
        inputs.addWidget(self.lineColor, 2, 1)
        inputs.addWidget(QLabel("Line Width: "), 4, 0, Qt.AlignRight)
        inputs.addWidget(self.linewidth, 4, 1)

        inputs.addWidget(QHLine(), 5, 0, 1, 2)

        inputs.addWidget(QLabel("Start X Position: "), 6, 0, Qt.AlignRight)
        inputs.addWidget(self.startxslider, 6, 1)
        inputs.addWidget(QLabel("Start Y Position: "), 7, 0, Qt.AlignRight)
        inputs.addWidget(self.startyslider, 7, 1)

        inputs.addWidget(QHLine(), 10, 0, 1, 2)

        inputs.addWidget(QLabel("End X Position: "), 11, 0, Qt.AlignRight)
        inputs.addWidget(self.endxslider, 11, 1)
        inputs.addWidget(QLabel("End Y Position: "), 12, 0, Qt.AlignRight)
        inputs.addWidget(self.endyslider, 12, 1)

        centerlayoutV = QVBoxLayout()
        centerlayoutV.addLayout(inputs)
        centerlayoutV.addStretch(1)

        centerlayout = QHBoxLayout()
        centerlayout.addLayout(centerlayoutV)
        centerlayout.addStretch(1)
        self.setLayout(centerlayout)

    def objChanged(self):
        """
        Sets the object attributes to the UI values.

        :return: None
        """
        self.lineobj.show = self.showItem.isChecked()
        self.lineobj.color = self.lineColor.color
        self.lineobj.width = self.linewidth.value()
        self.lineobj.startxpos = self.startxslider.value()
        self.lineobj.startypos = self.startyslider.value()
        self.lineobj.endxpos = self.endxslider.value()
        self.lineobj.endypos = self.endyslider.value()
        self.changeMade.emit()

    def BlockAllSignals(self, b):
        """
        Helper function to block update signals for the UI.

        :param b: Boolean for the blocking.
        :return: None
        """
        for obj in self.findChildren(QWidget):
            try:
                obj.blockSignals(b)
            except:
                pass

    def setImageSize(self, size):
        """
        Sets the size sliders to match the size of the image.

        :param size: Size of the image.
        :return: None
        """
        self.startxslider.setMaximum(size.width())
        self.startyslider.setMaximum(size.height())
        self.endxslider.setMaximum(size.width())
        self.endyslider.setMaximum(size.height())

    def setObject(self, lineobj):
        """
        Sets the UI values to match the object values.

        :param txtobj: Annotation object to load.
        :return: None
        """
        self.BlockAllSignals(True)
        self.lineobj = lineobj
        self.showItem.setChecked(self.lineobj.show)
        self.startxslider.setValue(self.lineobj.startxpos)
        self.startyslider.setValue(self.lineobj.startypos)
        self.endxslider.setValue(self.lineobj.endxpos)
        self.endyslider.setValue(self.lineobj.endypos)
        self.lineColor.setColor(self.lineobj.color)
        self.linewidth.setValue(self.lineobj.width)
        self.BlockAllSignals(False)
        self.changeMade.emit()

    def UpdateShow(self, b):
        """
        Updates the showing of the object.

        :param b: Boolean for the showing.
        :return: None
        """
        self.showItem.setChecked(b)


class ArrowOptions(QWidget):
    changeMade = Signal()

    def __init__(self, parent=None):
        """
        Widget for displaying the properties of the arrow object.

        :param parent: Parent object.
        """
        super().__init__(parent)

        self.arrowobj = None

        self.showItem = QCheckBox()
        self.showItem.clicked.connect(self.objChanged)

        self.linewidth = QSpinBox()
        self.linewidth.setMinimum(1)
        self.linewidth.setMaximum(20)
        self.linewidth.setValue(1)
        self.linewidth.setMinimumWidth(100)
        self.linewidth.setMaximumWidth(100)
        self.linewidth.valueChanged.connect(self.objChanged)

        self.arrowSize = QSpinBox()
        self.arrowSize.setMinimum(1)
        self.arrowSize.setMaximum(100)
        self.arrowSize.setValue(10)
        self.arrowSize.setMinimumWidth(100)
        self.arrowSize.setMaximumWidth(100)
        self.arrowSize.valueChanged.connect(self.objChanged)

        self.arrowAngle = QSpinBox()
        self.arrowAngle.setMinimum(1)
        self.arrowAngle.setMaximum(90)
        self.arrowAngle.setValue(30)
        self.arrowAngle.setMinimumWidth(100)
        self.arrowAngle.setMaximumWidth(100)
        self.arrowAngle.valueChanged.connect(self.objChanged)

        self.lineColor = ColorSelectButtonBox()
        self.lineColor.colorChange.connect(self.objChanged)
        self.lineColor.setMaximumWidth(50)

        sliderWidth = 200

        self.startxslider = QSlider(Qt.Orientation.Horizontal)
        self.startxslider.valueChanged.connect(self.objChanged)
        self.startxslider.setMinimumWidth(sliderWidth)

        self.startyslider = QSlider(Qt.Orientation.Horizontal)
        self.startyslider.valueChanged.connect(self.objChanged)
        self.startyslider.setMinimumWidth(sliderWidth)

        self.endxslider = QSlider(Qt.Orientation.Horizontal)
        self.endxslider.valueChanged.connect(self.objChanged)
        self.endxslider.setMinimumWidth(sliderWidth)

        self.endyslider = QSlider(Qt.Orientation.Horizontal)
        self.endyslider.valueChanged.connect(self.objChanged)
        self.endyslider.setMinimumWidth(sliderWidth)

        inputs = QGridLayout()
        inputs.addWidget(QLabel("Show: "), 0, 0, Qt.AlignRight)
        inputs.addWidget(self.showItem, 0, 1)
        inputs.addWidget(QLabel("Color: "), 2, 0, Qt.AlignRight)
        inputs.addWidget(self.lineColor, 2, 1)
        inputs.addWidget(QLabel("Line Width: "), 4, 0, Qt.AlignRight)
        inputs.addWidget(self.linewidth, 4, 1)

        inputs.addWidget(QHLine(), 5, 0, 1, 2)

        inputs.addWidget(QLabel("Start X Position: "), 6, 0, Qt.AlignRight)
        inputs.addWidget(self.startxslider, 6, 1)
        inputs.addWidget(QLabel("Start Y Position: "), 7, 0, Qt.AlignRight)
        inputs.addWidget(self.startyslider, 7, 1)

        inputs.addWidget(QHLine(), 10, 0, 1, 2)

        inputs.addWidget(QLabel("End X Position: "), 11, 0, Qt.AlignRight)
        inputs.addWidget(self.endxslider, 11, 1)
        inputs.addWidget(QLabel("End Y Position: "), 12, 0, Qt.AlignRight)
        inputs.addWidget(self.endyslider, 12, 1)

        inputs.addWidget(QHLine(), 13, 0, 1, 2)

        inputs.addWidget(QLabel("Arrow Size: "), 14, 0, Qt.AlignRight)
        inputs.addWidget(self.arrowSize, 14, 1)

        inputs.addWidget(QLabel("Arrow Angle: "), 15, 0, Qt.AlignRight)
        inputs.addWidget(self.arrowAngle, 15, 1)

        centerlayoutV = QVBoxLayout()
        centerlayoutV.addLayout(inputs)
        centerlayoutV.addStretch(1)

        centerlayout = QHBoxLayout()
        centerlayout.addLayout(centerlayoutV)
        centerlayout.addStretch(1)
        self.setLayout(centerlayout)

    def objChanged(self):
        """
        Sets the object attributes to the UI values.

        :return: None
        """
        self.arrowobj.show = self.showItem.isChecked()
        self.arrowobj.color = self.lineColor.color
        self.arrowobj.width = self.linewidth.value()
        self.arrowobj.startxpos = self.startxslider.value()
        self.arrowobj.startypos = self.startyslider.value()
        self.arrowobj.endxpos = self.endxslider.value()
        self.arrowobj.endypos = self.endyslider.value()
        self.arrowobj.arrowSize = self.arrowSize.value()
        self.arrowobj.arrowAngle = self.arrowAngle.value()
        self.changeMade.emit()

    def BlockAllSignals(self, b):
        """
        Helper function to block update signals for the UI.

        :param b: Boolean for the blocking.
        :return: None
        """
        for obj in self.findChildren(QWidget):
            try:
                obj.blockSignals(b)
            except:
                pass

    def setImageSize(self, size):
        """
        Sets the size sliders to match the size of the image.

        :param size: Size of the image.
        :return: None
        """
        self.startxslider.setMaximum(size.width())
        self.startyslider.setMaximum(size.height())
        self.endxslider.setMaximum(size.width())
        self.endyslider.setMaximum(size.height())

    def setObject(self, arrowobj):
        """
        Sets the UI values to match the object values.

        :param arrowobj: Annotation object to load.
        :return: None
        """
        self.BlockAllSignals(True)
        self.arrowobj = arrowobj
        self.showItem.setChecked(self.arrowobj.show)
        self.startxslider.setValue(self.arrowobj.startxpos)
        self.startyslider.setValue(self.arrowobj.startypos)
        self.endxslider.setValue(self.arrowobj.endxpos)
        self.endyslider.setValue(self.arrowobj.endypos)
        self.lineColor.setColor(self.arrowobj.color)
        self.linewidth.setValue(self.arrowobj.width)
        self.arrowSize.setValue(self.arrowobj.arrowSize)
        self.arrowAngle.setValue(self.arrowobj.arrowAngle)
        self.BlockAllSignals(False)
        self.changeMade.emit()

    def UpdateShow(self, b):
        """
        Updates the showing of the object.

        :param b: Boolean for the showing.
        :return: None
        """
        self.showItem.setChecked(b)


class RectangleOptions(QWidget):
    changeMade = Signal()

    def __init__(self, parent=None):
        """
        Widget for displaying the properties of the rectangle object.

        :param parent: Parent object.
        """
        super().__init__(parent)

        self.rectobj = None

        self.showItem = QCheckBox()
        self.showItem.clicked.connect(self.objChanged)

        self.fillRect = QCheckBox()
        self.fillRect.clicked.connect(self.objChanged)

        self.fillColor = ColorSelectButtonBox()
        self.fillColor.colorChange.connect(self.objChanged)
        self.fillColor.setMaximumWidth(50)

        self.linewidth = QSpinBox()
        self.linewidth.setMinimum(1)
        self.linewidth.setMaximum(20)
        self.linewidth.setValue(1)
        self.linewidth.setMinimumWidth(100)
        self.linewidth.setMaximumWidth(100)
        self.linewidth.valueChanged.connect(self.objChanged)

        self.cornerRad = QSpinBox()
        self.cornerRad.setMinimum(0)
        self.cornerRad.setMaximum(100)
        self.cornerRad.setValue(0)
        self.cornerRad.setMinimumWidth(100)
        self.cornerRad.setMaximumWidth(100)
        self.cornerRad.valueChanged.connect(self.objChanged)

        self.lineColor = ColorSelectButtonBox()
        self.lineColor.colorChange.connect(self.objChanged)
        self.lineColor.setMaximumWidth(50)

        sliderWidth = 200

        self.xposslider = QSlider(Qt.Orientation.Horizontal)
        self.xposslider.valueChanged.connect(self.objChanged)
        self.xposslider.setMinimumWidth(sliderWidth)

        self.yposslider = QSlider(Qt.Orientation.Horizontal)
        self.yposslider.valueChanged.connect(self.objChanged)
        self.yposslider.setMinimumWidth(sliderWidth)

        self.widthslider = QSlider(Qt.Orientation.Horizontal)
        self.widthslider.valueChanged.connect(self.objChanged)
        self.widthslider.setMinimumWidth(sliderWidth)

        self.heightslider = QSlider(Qt.Orientation.Horizontal)
        self.heightslider.valueChanged.connect(self.objChanged)
        self.heightslider.setMinimumWidth(sliderWidth)

        inputs = QGridLayout()
        inputs.addWidget(QLabel("Show: "), 0, 0, Qt.AlignRight)
        inputs.addWidget(self.showItem, 0, 1)
        inputs.addWidget(QLabel("Color: "), 2, 0, Qt.AlignRight)
        inputs.addWidget(self.lineColor, 2, 1)
        inputs.addWidget(QLabel("Line Width: "), 4, 0, Qt.AlignRight)
        inputs.addWidget(self.linewidth, 4, 1)

        inputs.addWidget(QHLine(), 5, 0, 1, 2)

        inputs.addWidget(QLabel("Anchor X Position: "), 6, 0, Qt.AlignRight)
        inputs.addWidget(self.xposslider, 6, 1)
        inputs.addWidget(QLabel("Anchor Y Position: "), 7, 0, Qt.AlignRight)
        inputs.addWidget(self.yposslider, 7, 1)

        inputs.addWidget(QHLine(), 10, 0, 1, 2)

        inputs.addWidget(QLabel("Width: "), 11, 0, Qt.AlignRight)
        inputs.addWidget(self.widthslider, 11, 1)
        inputs.addWidget(QLabel("Height: "), 12, 0, Qt.AlignRight)
        inputs.addWidget(self.heightslider, 12, 1)

        inputs.addWidget(QHLine(), 13, 0, 1, 2)

        inputs.addWidget(QLabel("Fill Rectangle: "), 14, 0, Qt.AlignRight)
        inputs.addWidget(self.fillRect, 14, 1)
        inputs.addWidget(QLabel("Fill Color: "), 15, 0, Qt.AlignRight)
        inputs.addWidget(self.fillColor, 15, 1)

        inputs.addWidget(QHLine(), 16, 0, 1, 2)

        inputs.addWidget(QLabel("Corner Radius: "), 17, 0, Qt.AlignRight)
        inputs.addWidget(self.cornerRad, 17, 1)

        centerlayoutV = QVBoxLayout()
        centerlayoutV.addLayout(inputs)
        centerlayoutV.addStretch(1)

        centerlayout = QHBoxLayout()
        centerlayout.addLayout(centerlayoutV)
        centerlayout.addStretch(1)
        self.setLayout(centerlayout)

    def objChanged(self):
        """
        Sets the object attributes to the UI values.

        :return: None
        """
        self.rectobj.show = self.showItem.isChecked()
        self.rectobj.color = self.lineColor.color
        self.rectobj.linewidth = self.linewidth.value()
        self.rectobj.xpos = self.xposslider.value()
        self.rectobj.ypos = self.yposslider.value()
        self.rectobj.width = self.widthslider.value()
        self.rectobj.height = self.heightslider.value()
        self.rectobj.cornerrad = self.cornerRad.value()
        self.rectobj.fill = self.fillRect.isChecked()
        self.rectobj.fillcolor = self.fillColor.color
        self.changeMade.emit()

    def BlockAllSignals(self, b):
        """
        Helper function to block update signals for the UI.

        :param b: Boolean for the blocking.
        :return: None
        """
        for obj in self.findChildren(QWidget):
            try:
                obj.blockSignals(b)
            except:
                pass

    def setImageSize(self, size):
        """
        Sets the size sliders to match the size of the image.

        :param size: Size of the image.
        :return: None
        """
        self.xposslider.setMaximum(size.width())
        self.yposslider.setMaximum(size.height())
        self.widthslider.setMaximum(size.width())
        self.heightslider.setMaximum(size.height())

    def setObject(self, rectobj):
        """
        Sets the UI values to match the object values.

        :param rectobj: Annotation object to load.
        :return: None
        """
        self.BlockAllSignals(True)
        self.rectobj = rectobj
        self.showItem.setChecked(self.rectobj.show)
        self.xposslider.setValue(self.rectobj.xpos)
        self.yposslider.setValue(self.rectobj.ypos)
        self.widthslider.setValue(self.rectobj.width)
        self.heightslider.setValue(self.rectobj.height)
        self.lineColor.setColor(self.rectobj.color)
        self.linewidth.setValue(self.rectobj.linewidth)
        self.cornerRad.setValue(self.rectobj.cornerrad)
        self.fillRect.setChecked(self.rectobj.fill)
        self.fillColor.setColor(self.rectobj.fillcolor)
        self.BlockAllSignals(False)
        self.changeMade.emit()

    def UpdateShow(self, b):
        """
        Updates the showing of the object.

        :param b: Boolean for the showing.
        :return: None
        """
        self.showItem.setChecked(b)


class EllipseOptions(QWidget):
    changeMade = Signal()

    def __init__(self, parent=None):
        """
        Widget for displaying the properties of the ellipse object.

        :param parent: Parent object.
        """
        super().__init__(parent)

        self.rectobj = None

        self.showItem = QCheckBox()
        self.showItem.clicked.connect(self.objChanged)

        self.fillRect = QCheckBox()
        self.fillRect.clicked.connect(self.objChanged)

        self.fillColor = ColorSelectButtonBox()
        self.fillColor.colorChange.connect(self.objChanged)
        self.fillColor.setMaximumWidth(50)

        self.linewidth = QSpinBox()
        self.linewidth.setMinimum(1)
        self.linewidth.setMaximum(20)
        self.linewidth.setValue(1)
        self.linewidth.setMinimumWidth(100)
        self.linewidth.setMaximumWidth(100)
        self.linewidth.valueChanged.connect(self.objChanged)

        self.cornerRad = QSpinBox()
        self.cornerRad.setMinimum(0)
        self.cornerRad.setMaximum(100)
        self.cornerRad.setValue(0)
        self.cornerRad.setMinimumWidth(100)
        self.cornerRad.setMaximumWidth(100)
        self.cornerRad.valueChanged.connect(self.objChanged)

        self.lineColor = ColorSelectButtonBox()
        self.lineColor.colorChange.connect(self.objChanged)
        self.lineColor.setMaximumWidth(50)

        sliderWidth = 200

        self.xposslider = QSlider(Qt.Orientation.Horizontal)
        self.xposslider.valueChanged.connect(self.objChanged)
        self.xposslider.setMinimumWidth(sliderWidth)

        self.yposslider = QSlider(Qt.Orientation.Horizontal)
        self.yposslider.valueChanged.connect(self.objChanged)
        self.yposslider.setMinimumWidth(sliderWidth)

        self.widthslider = QSlider(Qt.Orientation.Horizontal)
        self.widthslider.valueChanged.connect(self.objChanged)
        self.widthslider.setMinimumWidth(sliderWidth)

        self.heightslider = QSlider(Qt.Orientation.Horizontal)
        self.heightslider.valueChanged.connect(self.objChanged)
        self.heightslider.setMinimumWidth(sliderWidth)

        inputs = QGridLayout()
        inputs.addWidget(QLabel("Show: "), 0, 0, Qt.AlignRight)
        inputs.addWidget(self.showItem, 0, 1)
        inputs.addWidget(QLabel("Color: "), 2, 0, Qt.AlignRight)
        inputs.addWidget(self.lineColor, 2, 1)
        inputs.addWidget(QLabel("Line Width: "), 4, 0, Qt.AlignRight)
        inputs.addWidget(self.linewidth, 4, 1)

        inputs.addWidget(QHLine(), 5, 0, 1, 2)

        inputs.addWidget(QLabel("Anchor X Position: "), 6, 0, Qt.AlignRight)
        inputs.addWidget(self.xposslider, 6, 1)
        inputs.addWidget(QLabel("Anchor Y Position: "), 7, 0, Qt.AlignRight)
        inputs.addWidget(self.yposslider, 7, 1)

        inputs.addWidget(QHLine(), 10, 0, 1, 2)

        inputs.addWidget(QLabel("Width: "), 11, 0, Qt.AlignRight)
        inputs.addWidget(self.widthslider, 11, 1)
        inputs.addWidget(QLabel("Height: "), 12, 0, Qt.AlignRight)
        inputs.addWidget(self.heightslider, 12, 1)

        inputs.addWidget(QHLine(), 13, 0, 1, 2)

        inputs.addWidget(QLabel("Fill Ellipse: "), 14, 0, Qt.AlignRight)
        inputs.addWidget(self.fillRect, 14, 1)
        inputs.addWidget(QLabel("Fill Color: "), 15, 0, Qt.AlignRight)
        inputs.addWidget(self.fillColor, 15, 1)

        centerlayoutV = QVBoxLayout()
        centerlayoutV.addLayout(inputs)
        centerlayoutV.addStretch(1)

        centerlayout = QHBoxLayout()
        centerlayout.addLayout(centerlayoutV)
        centerlayout.addStretch(1)
        self.setLayout(centerlayout)

    def objChanged(self):
        """
        Sets the object attributes to the UI values.

        :return: None
        """
        self.rectobj.show = self.showItem.isChecked()
        self.rectobj.color = self.lineColor.color
        self.rectobj.linewidth = self.linewidth.value()
        self.rectobj.xpos = self.xposslider.value()
        self.rectobj.ypos = self.yposslider.value()
        self.rectobj.width = self.widthslider.value()
        self.rectobj.height = self.heightslider.value()
        self.rectobj.fill = self.fillRect.isChecked()
        self.rectobj.fillcolor = self.fillColor.color
        self.changeMade.emit()

    def BlockAllSignals(self, b):
        """
        Helper function to block update signals for the UI.

        :param b: Boolean for the blocking.
        :return: None
        """
        for obj in self.findChildren(QWidget):
            try:
                obj.blockSignals(b)
            except:
                pass

    def setImageSize(self, size):
        """
        Sets the size sliders to match the size of the image.

        :param size: Size of the image.
        :return: None
        """
        self.xposslider.setMaximum(size.width())
        self.yposslider.setMaximum(size.height())
        self.widthslider.setMaximum(size.width())
        self.heightslider.setMaximum(size.height())

    def setObject(self, rectobj):
        """
        Sets the UI values to match the object values.

        :param txtobj: Annotation object to load.
        :return: None
        """
        self.BlockAllSignals(True)
        self.rectobj = rectobj
        self.showItem.setChecked(self.rectobj.show)
        self.xposslider.setValue(self.rectobj.xpos)
        self.yposslider.setValue(self.rectobj.ypos)
        self.widthslider.setValue(self.rectobj.width)
        self.heightslider.setValue(self.rectobj.height)
        self.lineColor.setColor(self.rectobj.color)
        self.linewidth.setValue(self.rectobj.linewidth)
        self.fillRect.setChecked(self.rectobj.fill)
        self.fillColor.setColor(self.rectobj.fillcolor)
        self.BlockAllSignals(False)
        self.changeMade.emit()

    def UpdateShow(self, b):
        """
        Updates the showing of the object.

        :param b: Boolean for the showing.
        :return: None
        """
        self.showItem.setChecked(b)

## Main Window

class ImageViewer(QMainWindow):
    def __init__(self, parent=None, img=None, title='Image Annotator'):
        """
        Image viewer and annotator.

        :param parent: Parent object calling this application.
        :param img: Image to be displayed.
        :param title: Window title.
        """
        super().__init__()
        self.Parent = parent
        self.OriginalImage = img
        self.IncludeBorder = False
        self.PropertiesWidgetIndex = 0

        self.authors = "Don Spickler"
        self.version = "1.1.1"
        self.program_title = "Image Annotator"
        self.copyright = "2026"
        self.licence = "\nThis software is distributed under the GNU General Public License version 3.\n\n" + \
                       "This program is free software: you can redistribute it and/or modify it under the terms of the GNU " + \
                       "General Public License as published by the Free Software Foundation, either version 3 of the License, " + \
                       "or (at your option) any later version. This program is distributed in the hope that it will be useful, " + \
                       "but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A " + \
                       "PARTICULAR PURPOSE. See the GNU General Public License for more details http://www.gnu.org/licenses/."

        self.clipboard = QApplication.clipboard()
        self.setMinimumSize(800, 600)
        self.setWindowTitle(title)
        icon = QIcon(self.resource_path("icons/ImageAnnIcon.png"))
        self.setWindowIcon(icon)

        self.Platform = platform.system()
        styles = QStyleFactory.keys()
        if "Fusion" in styles:
            app.setStyle('Fusion')

        self.Annotations = []

        menubar, toolbar = self.createToolBar()
        self.imageCanvas = Canvas()

        self.ItemListDisplay = QListWidget()
        self.ItemListDisplay.setAlternatingRowColors(True)
        self.ItemListDisplay.currentRowChanged.connect(self.AnnotationItemChanged)
        self.ItemListDisplay.doubleClicked.connect(self.AnnotationShowHide)

        graphManagerAndTools = QWidget()
        graphManagerAndToolsLayout = QVBoxLayout()

        self.PropertiesDisplay = QWidget()
        self.PropertiesDisplayLayout = QStackedLayout()

        self.PropertiesDisplayLayout.insertWidget(0, QWidget())

        self.TextBoxOptions = TextBoxOptions(self)
        self.TextBoxOptions.changeMade.connect(self.changeMade)
        self.PropertiesDisplayLayout.insertWidget(1, self.TextBoxOptions)

        self.LineOptions = LineOptions(self)
        self.LineOptions.changeMade.connect(self.changeMade)
        self.PropertiesDisplayLayout.insertWidget(2, self.LineOptions)

        self.RectangleOptions = RectangleOptions(self)
        self.RectangleOptions.changeMade.connect(self.changeMade)
        self.PropertiesDisplayLayout.insertWidget(3, self.RectangleOptions)

        self.EllipseOptions = EllipseOptions(self)
        self.EllipseOptions.changeMade.connect(self.changeMade)
        self.PropertiesDisplayLayout.insertWidget(4, self.EllipseOptions)

        self.ArrowOptions = ArrowOptions(self)
        self.ArrowOptions.changeMade.connect(self.changeMade)
        self.PropertiesDisplayLayout.insertWidget(5, self.ArrowOptions)

        self.ImageOptions = ImageOptions(self)
        self.ImageOptions.changeMade.connect(self.changeMade)
        self.PropertiesDisplayLayout.insertWidget(6, self.ImageOptions)

        self.PropertiesDisplayLayout.setCurrentIndex(0)
        self.PropertiesDisplay.setLayout(self.PropertiesDisplayLayout)

        propertiesScrollContainer = QScrollArea(self)
        propertiesScrollContainer.setWidgetResizable(True)
        propertiesScrollContainer.setWidget(self.PropertiesDisplay)

        self.itemDescAndType = QLineEdit()
        self.itemDescAndType.setReadOnly(True)
        propertiesTypeContainer = QWidget(self)
        propertiesTypeContainerLayout = QGridLayout()
        propertiesTypeContainerLayout.addWidget(self.itemDescAndType, 0, 0)
        propertiesTypeContainerLayout.addWidget(propertiesScrollContainer, 1, 0)

        propertiesTypeContainerLayout.setContentsMargins(0, 0, 0, 0)
        propertiesTypeContainer.setLayout(propertiesTypeContainerLayout)

        ItemsAndTitle = QWidget()
        ItemsAndTitleLayout = QGridLayout()
        ItemsAndTitleLayout.addWidget(QLabel('Annotations'), 0, 0)
        ItemsAndTitleLayout.addWidget(self.ItemListDisplay, 1, 0)
        ItemsAndTitleLayout.setContentsMargins(0, 0, 0, 0)
        ItemsAndTitle.setLayout(ItemsAndTitleLayout)

        graphManagerAndSliders = QSplitter()
        graphManagerAndSliders.setOrientation(Qt.Vertical)
        graphManagerAndSliders.addWidget(ItemsAndTitle)
        graphManagerAndSliders.addWidget(propertiesTypeContainer)
        graphManagerAndToolsLayout.addWidget(graphManagerAndSliders)
        graphManagerAndSliders.setStretchFactor(0, 1)
        graphManagerAndSliders.setStretchFactor(1, 1)
        graphManagerAndToolsLayout.setStretchFactor(graphManagerAndSliders, 1)

        graphManagerAndToolsLayout.setContentsMargins(0, 0, 0, 0)
        graphManagerAndTools.setLayout(graphManagerAndToolsLayout)

        graphAndManagerLayout = QHBoxLayout()
        graphAndManagerLayout.addWidget(graphManagerAndTools)
        graphAndManagerLayout.addWidget(self.imageCanvas)
        graphAndManagerLayout.setContentsMargins(0, 0, 0, 0)
        graphAndManagerLayout.setStretchFactor(graphManagerAndTools, 0)
        graphAndManagerLayout.setStretchFactor(self.imageCanvas, 1)

        centerWidget = QWidget()
        centerLayout = QVBoxLayout()
        centerLayout.addWidget(toolbar)
        centerLayout.addLayout(graphAndManagerLayout)

        centerWidget.setLayout(centerLayout)
        centerLayout.setContentsMargins(5,5,5,5)
        self.setMenuBar(menubar)

        self.setImage(img)
        self.setCentralWidget(centerWidget)
        self.setStatusBar(QStatusBar(self))
        self.resize(1200, 800)
        self.ItemListDisplay.setFocus()
        self.show()

    def setImage(self, img):
        """
        Sets the image for the application.

        :param img: Image to be displayed.
        :return: None
        """
        if img is None:
            return

        self.OriginalImage = img
        self.UpdateImage()

    def AnnotationItemChanged(self):
        """
        Updates the UI for the currently selected annotation object from the list.

        :return: None
        """
        if len(self.Annotations) == 0:
            self.PropertiesWidgetIndex = 0
            self.PropertiesDisplayLayout.setCurrentIndex(0)
            self.itemDescAndType.setText('')
            self.itemDescAndType.setCursorPosition(0)
        else:
            r = self.ItemListDisplay.currentRow()
            if r < 0:
                self.ItemListDisplay.setCurrentRow(0)
                r = 0
            elif r >= self.ItemListDisplay.count():
                self.ItemListDisplay.setCurrentRow(self.ItemListDisplay.count() - 1)
                r = self.ItemListDisplay.count() - 1

            if r >= len(self.Annotations):
                self.ItemListDisplay.setCurrentRow(len(self.Annotations) - 1)
                r = len(self.Annotations) - 1

            self.PropertiesWidgetIndex = 0
            if isinstance(self.Annotations[r], TextObject):
                self.PropertiesWidgetIndex = 1
            elif isinstance(self.Annotations[r], LineObject):
                self.PropertiesWidgetIndex = 2
            elif isinstance(self.Annotations[r], RectangleObject):
                self.PropertiesWidgetIndex = 3
            elif isinstance(self.Annotations[r], EllipseObject):
                self.PropertiesWidgetIndex = 4
            elif isinstance(self.Annotations[r], ArrowObject):
                self.PropertiesWidgetIndex = 5
            elif isinstance(self.Annotations[r], ImageObject):
                self.PropertiesWidgetIndex = 6

            self.PropertiesDisplayLayout.setCurrentIndex(self.PropertiesWidgetIndex)
            optwid = self.PropertiesDisplayLayout.currentWidget()
            optwid.setObject(self.Annotations[r])

            if self.OriginalImage is not None:
                optwid.setImageSize(self.OriginalImage.size())

            DescAndTypeText = 'Properties: ' + self.Annotations[r].toDisplayString()
            self.itemDescAndType.setText(DescAndTypeText)
            self.itemDescAndType.setCursorPosition(0)

    def AnnotationShowHide(self):
        """
        Toggles the showing of the currently selected annotation.

        :return: None
        """
        r = self.ItemListDisplay.currentRow()
        if r < 0:
            return

        self.Annotations[r].show = not self.Annotations[r].show
        try:
            optwid = self.PropertiesDisplayLayout.currentWidget()
            optwid.UpdateShow(self.Annotations[r].show)
        except:
            pass
        self.changeMade()


    def TextToImage(self, txtobj):
        """
        Creates the input text object to an image.

        :param txtobj: String to convert to image.
        """
        try:
            horpixadd = txtobj.xPadding
            verpixadd = txtobj.yPadding

            strlst = txtobj.text.split('\n')
            fm = QFontMetrics(txtobj.font)
            fontheight = fm.lineSpacing()
            numlines = len(strlst)
            maxAdvance = 0
            for line in strlst:
                maxAdvance = max(maxAdvance, fm.horizontalAdvance(line))

            additionalWidth = 4
            maxAdvance += additionalWidth  # Additional pixels to stop line wrap on drawText for long objects.
            # maxAdvance += 2  # Additional pixels to stop line wrap on drawText for long objects.

            image = QPixmap(QSize(maxAdvance + horpixadd, numlines * fontheight + verpixadd))
            image.fill(Qt.transparent)

            painter = QPainter()
            painter.begin(image)

            if txtobj.includeBox:
                painter.setBrush(QColor(txtobj.backgroundColor.red(), txtobj.backgroundColor.green(),
                                  txtobj.backgroundColor.blue()))
                painter.drawRect(QRect(-10, -10, image.size().width()+20, image.size().height()+20))

            painter.setPen(txtobj.color)
            painter.setFont(txtobj.font)

            align = Qt.AlignLeft
            if txtobj.justify == 'left':
                align = Qt.AlignLeft
            elif txtobj.justify == 'center':
                align = Qt.AlignCenter
            elif txtobj.justify == 'right':
                align = Qt.AlignRight

            if txtobj.justify == 'center':
                painter.translate(horpixadd // 2, 0)
            else:
                painter.translate(horpixadd//2, verpixadd//2)

            painter.drawText(QRect(0, 0, maxAdvance, numlines * fontheight + verpixadd), txtobj.text, align)

            painter.end()
            finalimage = image.toImage()

            if txtobj.includeBox and txtobj.borderWidth > 0:
                width = txtobj.borderWidth
                col = txtobj.borderColor
                sz = finalimage.size()
                newimg = QPixmap(QSize(sz.width() + 2 * width, sz.height() + 2 * width))
                painter = QPainter()
                painter.begin(newimg)
                painter.setBrush(col)
                painter.drawRect(-2, -2, sz.width() + 2 * width + 4, sz.height() + 2 * width + 4)
                painter.drawImage(width, width, finalimage)
                painter.end()
                finalimage = newimg.toImage()

            return finalimage
        except:
            print("Could not convert text to image.")

    def mirror_image_horizontally(self, img):
        """ Flips the image horizontally. """
        transform = QTransform(-1, 0, 0, 1, img.width(), 0)
        return img.transformed(transform)

    def mirror_image_vertically(self, img):
        """ Flips the image vertically. """
        transform = QTransform(1, 0, 0, -1, 0, img.height())
        return img.transformed(transform)

    def createImageWithAnnotations(self):
        """
        Creates an image from the initial image and the currently input annotations.

        :return: An image that is the initial image with the annotations inserted.
        """
        if self.OriginalImage is None:
            return

        FinalImage = self.OriginalImage

        sz = FinalImage.size()
        newimg = QPixmap(QSize(sz.width(), sz.height()))
        painter = QPainter()
        painter.begin(newimg)
        painter.drawImage(0, 0, FinalImage)
        painter.setRenderHint(QPainter.Antialiasing)

        # Drawing objects bottom to top.

        for obj in self.Annotations:
            if obj.show:
                if isinstance(obj, ImageObject):
                    painter.setRenderHint(QPainter.SmoothPixmapTransform)
                    scaled_image = obj.image.smoothScaled(obj.image.size().width() * obj.scale * obj.aspectratio,
                                                          obj.image.size().height() * obj.scale / obj.aspectratio)

                    if obj.FlipHorizontal:
                        scaled_image = self.mirror_image_horizontally(scaled_image)

                    if obj.FlipVertical:
                        scaled_image = self.mirror_image_vertically(scaled_image)

                    if obj.includeBox:
                        image = QPixmap(QSize(scaled_image.width(), scaled_image.height()))
                        if obj.xPadding > 0 or obj.yPadding > 0:
                            image = QPixmap(QSize(scaled_image.width() + 2*obj.xPadding,
                                                  scaled_image.height() + 2*obj.yPadding))

                            image.fill(obj.backgroundColor)

                            pixpainter = QPainter()
                            pixpainter.begin(image)
                            pixpainter.drawImage(obj.xPadding, obj.yPadding, scaled_image)
                            pixpainter.end()
                            scaled_image = image.toImage()

                        if obj.borderWidth > 0:
                            image = QPixmap(QSize(scaled_image.width() + 2 * obj.borderWidth,
                                                  scaled_image.height() + 2 * obj.borderWidth))

                            image.fill(obj.borderColor)

                            pixpainter = QPainter()
                            pixpainter.begin(image)
                            pixpainter.drawImage(obj.borderWidth, obj.borderWidth, scaled_image)
                            pixpainter.end()
                            scaled_image = image.toImage()

                    if obj.rotation != 0:
                        rottransform = QTransform()
                        rottransform.rotate(obj.rotation)
                        scaled_image = scaled_image.transformed(rottransform)

                    if obj.useTransparentColor:
                        transImage = QPixmap.fromImage(scaled_image)
                        msk = transImage.createMaskFromColor(obj.transparentColor, Qt.MaskInColor)
                        transImage.setMask(msk)
                        scaled_image = transImage.toImage()

                    painter.setOpacity(1 - obj.transparency)
                    painter.drawImage(obj.xpos, obj.ypos, scaled_image)
                    painter.setOpacity(1)

        for obj in self.Annotations:
            if obj.show:
                if isinstance(obj, ArrowObject):
                    painter.setPen(QPen(obj.color, obj.width))
                    arrowSize = obj.arrowSize
                    arrowAngle = obj.arrowAngle * pi / 180
                    line = QLineF(QPointF(obj.endxpos, obj.endypos), QPointF(obj.startxpos, obj.startypos))
                    angle = atan2(-line.dy(), line.dx()) + pi/2
                    arrowP1 = line.p1() + QPointF(sin(angle + arrowAngle) * arrowSize,
                                                  cos(angle + arrowAngle) * arrowSize)
                    arrowP2 = line.p1() + QPointF(sin(angle - arrowAngle) * arrowSize,
                                                  cos(angle - arrowAngle) * arrowSize)

                    arrowAdd = line.p1() - QPointF((line.p1().x() + arrowP1.x() + arrowP2.x())/3,
                                       (line.p1().y() + arrowP1.y() + arrowP2.y())/3)

                    arrowHead = QPolygonF([line.p1() + arrowAdd, arrowP1 + arrowAdd, arrowP2 + arrowAdd])
                    painter.drawLine(line)
                    painter.setPen(QPen(obj.color, 1))
                    path = QPainterPath()
                    path.addPolygon(arrowHead)
                    painter.fillPath(path, obj.color)
                    painter.drawPath(path)

        for obj in self.Annotations:
            if obj.show:
                if isinstance(obj, LineObject):
                    painter.setPen(QPen(obj.color, obj.width))
                    painter.drawLine(obj.startxpos, obj.startypos, obj.endxpos, obj.endypos)

        for obj in self.Annotations:
            if obj.show:
                if isinstance(obj, EllipseObject):
                    path = QPainterPath()
                    path.addEllipse(obj.xpos, obj.ypos, obj.width, obj.height)
                    painter.setPen(QPen(obj.color, obj.linewidth))
                    if obj.fill:
                        painter.fillPath(path, obj.fillcolor)
                    painter.drawPath(path)

        for obj in self.Annotations:
            if obj.show:
                if isinstance(obj, RectangleObject):
                    path = QPainterPath()
                    path.addRoundedRect(QRectF(obj.xpos, obj.ypos, obj.width, obj.height), obj.cornerrad, obj.cornerrad)
                    painter.setPen(QPen(obj.color, obj.linewidth))
                    if obj.fill:
                        painter.fillPath(path, obj.fillcolor)
                    painter.drawPath(path)

        for obj in self.Annotations:
            if obj.show:
                if isinstance(obj, TextObject):
                    txtimg = self.TextToImage(obj)

                    if obj.rotation != 0:
                        rottransform = QTransform()
                        rottransform.rotate(obj.rotation)
                        txtimg = txtimg.transformed(rottransform)

                    painter.setOpacity(1 - obj.transparency)
                    painter.drawImage(obj.xpos, obj.ypos, txtimg)
                    painter.setOpacity(1)

        painter.end()
        FinalImage = newimg.toImage()

        if self.IncludeBorder:
            width = self.borderwidth.value()
            col = self.BorderColor.color
            sz = FinalImage.size()
            newimg = QPixmap(QSize(sz.width()+2*width, sz.height()+2*width))
            painter = QPainter()
            painter.begin(newimg)
            painter.setBrush(col)
            painter.drawRect(-2, -2, sz.width()+2*width+4, sz.height()+2*width+4)
            painter.drawImage(width, width, FinalImage)
            painter.end()
            FinalImage = newimg.toImage()

        return FinalImage

    def changeMade(self):
        """
        Sets the UI when changes are made.

        :return: None
        """
        self.UpdateImage()

        r = self.ItemListDisplay.currentRow()
        if r >= 0:
            desc = self.Annotations[r].toDisplayString()
            desc = desc.replace('\n', ' ')
            desc = desc.replace('\t', ' ')
            self.ItemListDisplay.item(r).setText(desc)
            DescAndTypeText = 'Properties: ' + desc
            self.itemDescAndType.setText(DescAndTypeText)
            self.itemDescAndType.setCursorPosition(0)

    def UpdateImage(self):
        """
        updates the canvas with the new image.

        :return: None
        """
        self.imageCanvas.setImage(self.createImageWithAnnotations())
        self.imageCanvas.repaint()

    def resource_path(self, relative_path):
        """
        Creates a system path that is relative to the position of the running application.

        :param relative_path: The relative path of the file from the base position of the running application.
        :return: The full OS path.
        """
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

    def createToolBar(self):
        """
        Creates the application toolbar and menu bar.

        :return: Menu bar and toolbar objects.
        """
        graph_OpenProject_act = QAction(QIcon(self.resource_path('icons/FileOpen.png')), "Open Project...", self)
        graph_OpenProject_act.setStatusTip('Open an annotation project file.')
        # graph_OpenProject_act.setShortcut('Ctrl+O')
        graph_OpenProject_act.triggered.connect(self.openProject)

        graph_saveProject_act = QAction(QIcon(self.resource_path('icons/FileSave.png')), "Save Project As...", self)
        graph_saveProject_act.setStatusTip('Save to an annotation project file.')
        # graph_saveProject_act.setShortcut('Ctrl+S')
        graph_saveProject_act.triggered.connect(self.saveProject)

        graph_OpenImage_act = QAction(QIcon(self.resource_path('icons/Merge.png')), "Open Base Image...", self)
        graph_OpenImage_act.setStatusTip('Open an image file for the base image.')
        # graph_OpenImage_act.setShortcut('Ctrl+O')
        graph_OpenImage_act.triggered.connect(self.openImage)

        graph_PasteImage_act = QAction(QIcon(self.resource_path('icons/paste.png')), "Paste Base Image...", self)
        graph_PasteImage_act.setStatusTip('Paste in an image from the clipboard as the base image.')
        graph_PasteImage_act.setShortcut('Ctrl+V')
        graph_PasteImage_act.triggered.connect(self.pasteImage)

        graph_NewImage_act = QAction(QIcon(self.resource_path('icons/newgraph.png')), "New Blank Base Image...", self)
        graph_NewImage_act.setStatusTip('Create a new blank image for the base image.')
        # graph_NewImage_act.setShortcut('Ctrl+N')
        graph_NewImage_act.triggered.connect(self.newImage)

        graph_saveImage_act = QAction(QIcon(self.resource_path('icons/SaveImage.png')), "Save Image As...", self)
        graph_saveImage_act.setStatusTip('Save to an image file.')
        graph_saveImage_act.setShortcut('Ctrl+S')
        graph_saveImage_act.triggered.connect(self.saveImageFileAs)

        graph_printImage_act = QAction(QIcon(self.resource_path('icons/print.png')), "Print...", self)
        graph_printImage_act.setStatusTip('Print the image.')
        graph_printImage_act.setShortcut('Ctrl+P')
        graph_printImage_act.triggered.connect(self.printImageFile)

        graph_printPreviewImage_act = QAction(QIcon(self.resource_path('icons/preview.png')), "Print Preview...", self)
        graph_printPreviewImage_act.setStatusTip('Print preview of the image.')
        graph_printPreviewImage_act.triggered.connect(self.PrintPreviewImage)

        graph_copyImage_act = QAction(QIcon(self.resource_path('icons/CopyImage.png')), "Copy Image", self)
        graph_copyImage_act.setStatusTip('Copy image to the clipboard.')
        graph_copyImage_act.setShortcut('Ctrl+C')
        graph_copyImage_act.triggered.connect(self.copyImage)

        graph_toggleBorder_act = QAction(QIcon(self.resource_path('icons/BoundBox.png')), "Toggle Border", self)
        graph_toggleBorder_act.setStatusTip('Toggle the border.')
        graph_toggleBorder_act.triggered.connect(self.toggleBorder)

        insertTextAct =  QAction(QIcon(self.resource_path('icons/text.png')), "Insert Text", self)
        insertTextAct.setStatusTip('Insert a text box.')
        insertTextAct.triggered.connect(self.insertTextBox)

        insertLineAct =  QAction(QIcon(self.resource_path('icons/linetool.png')), "Insert Line", self)
        insertLineAct.setStatusTip('Insert a line.')
        insertLineAct.triggered.connect(self.insertLine)

        insertRectangleAct =  QAction(QIcon(self.resource_path('icons/BoundBox.png')), "Insert Rectangle", self)
        insertRectangleAct.setStatusTip('Insert a rounded rectangle.')
        insertRectangleAct.triggered.connect(self.insertRectangle)

        insertEllipseAct =  QAction(QIcon(self.resource_path('icons/ellipse.png')), "Insert Ellipse", self)
        insertEllipseAct.setStatusTip('Insert an ellipse.')
        insertEllipseAct.triggered.connect(self.insertEllipse)

        insertArrowAct =  QAction(QIcon(self.resource_path('icons/arrowtool.png')), "Insert Arrow", self)
        insertArrowAct.setStatusTip('Insert an arrow.')
        insertArrowAct.triggered.connect(self.insertArrow)

        insertImageAct =  QAction(QIcon(self.resource_path('icons/CopyImage2.png')), "Insert Image", self)
        insertImageAct.setStatusTip('Insert an image.')
        insertImageAct.triggered.connect(self.insertImage)

        deleteAct =  QAction("Delete Annotation...", self)
        deleteAct.setShortcut('Del')
        deleteAct.setStatusTip('Delete currently selected annotation.')
        deleteAct.triggered.connect(self.deleteAnnotation)

        clearAnnotationsAct =  QAction("Clear Annotation List...", self)
        clearAnnotationsAct.setStatusTip('Clear the annotation list.')
        clearAnnotationsAct.triggered.connect(self.clearAnnotations)

        help_about_act = QAction(QIcon(self.resource_path('icons/About.png')), "About...", self)
        help_about_act.setStatusTip('About ' + self.program_title)
        help_about_act.triggered.connect(self.aboutDialog)

        help_help_act = QAction(QIcon(self.resource_path('icons/Help2.png')), "Help...", self)
        help_help_act.setShortcut('F1')
        help_help_act.setStatusTip('Help with ' + self.program_title + " Version " + self.version + "...")
        help_help_act.triggered.connect(self.onHelp)

        graph_Exit_act = QAction("Exit", self)
        graph_Exit_act.setStatusTip('Close viewer.')
        graph_Exit_act.triggered.connect(self.close)

        tool_bar = QToolBar("Graph Tools Toolbar")
        tool_bar.setIconSize(QSize(18, 18))
        tool_bar.setMovable(False)
        tool_bar.addAction(graph_OpenProject_act)
        tool_bar.addAction(graph_saveProject_act)
        tool_bar.addSeparator()
        tool_bar.addAction(graph_NewImage_act)
        tool_bar.addAction(graph_OpenImage_act)
        tool_bar.addAction(graph_PasteImage_act)
        tool_bar.addSeparator()
        tool_bar.addAction(graph_copyImage_act)
        tool_bar.addAction(graph_saveImage_act)
        tool_bar.addSeparator()
        tool_bar.addAction(graph_printImage_act)
        tool_bar.addAction(graph_printPreviewImage_act)
        tool_bar.addSeparator()
        tool_bar.addAction(insertTextAct)
        tool_bar.addAction(insertRectangleAct)
        tool_bar.addAction(insertEllipseAct)
        tool_bar.addAction(insertLineAct)
        tool_bar.addAction(insertArrowAct)
        tool_bar.addAction(insertImageAct)
        tool_bar.addSeparator()
        tool_bar.addAction(graph_toggleBorder_act)

        spinwidth = 75
        self.borderwidth = QSpinBox()
        self.borderwidth.setMinimumWidth(spinwidth)
        self.borderwidth.setMaximumWidth(spinwidth)
        self.borderwidth.setMinimum(1)
        self.borderwidth.setMaximum(100)
        self.borderwidth.setValue(1)
        self.borderwidth.valueChanged.connect(self.UpdateImage)

        self.BorderColor = ColorSelectButtonBox(Parent=self, maxwidth=50)
        self.BorderColor.colorChange.connect(self.UpdateImage)

        tool_bar.addWidget(QLabel('   '))
        tool_bar.addWidget(self.borderwidth)
        tool_bar.addWidget(QLabel('   '))
        tool_bar.addWidget(self.BorderColor)

        menu_bar = QMenuBar()
        FileMenu = menu_bar.addMenu('File')
        FileMenu.addAction(graph_OpenProject_act)
        FileMenu.addAction(graph_saveProject_act)
        FileMenu.addSeparator()
        FileMenu.addAction(graph_NewImage_act)
        FileMenu.addAction(graph_OpenImage_act)
        FileMenu.addAction(graph_PasteImage_act)
        FileMenu.addSeparator()
        FileMenu.addAction(graph_copyImage_act)
        FileMenu.addAction(graph_saveImage_act)
        FileMenu.addSeparator()
        FileMenu.addAction(graph_printImage_act)
        FileMenu.addAction(graph_printPreviewImage_act)
        FileMenu.addSeparator()
        FileMenu.addAction(graph_Exit_act)

        edit_menu = menu_bar.addMenu('Edit')
        edit_menu.addAction(graph_toggleBorder_act)
        edit_menu.addSeparator()
        edit_menu.addAction(insertTextAct)
        edit_menu.addAction(insertRectangleAct)
        edit_menu.addAction(insertEllipseAct)
        edit_menu.addAction(insertLineAct)
        edit_menu.addAction(insertArrowAct)
        edit_menu.addAction(insertImageAct)
        edit_menu.addSeparator()
        edit_menu.addAction(deleteAct)
        edit_menu.addAction(clearAnnotationsAct)

        help_menu = menu_bar.addMenu('Help')
        help_menu.addAction(help_help_act)
        help_menu.addSeparator()
        help_menu.addAction(help_about_act)

        return menu_bar, tool_bar

    def openProject(self):
        """
        Opens an annotation project file and loads the original image and the annotations.

        :return: None
        """
        if self.OriginalImage is not None or len(self.Annotations) > 0:
            message = "This will replace the base image and annotation list with the selected project.  "
            message += "This operation cannot be undone.  "
            message += "Do you wish to load a project?"
            res = QMessageBox.question(self, "Replace Project", message, QMessageBox.Yes | QMessageBox.No)

            if res == QMessageBox.No:
                return

        file_name, _ = QFileDialog.getOpenFileName(self, "Open Project", "",
                                                   "Image Annotation Files (*.ian);;All Files (*.*)")

        try:
            if file_name:
                with open(file_name, "rb") as f:
                    loaded_data = pickle.load(f)

                    restored_image = QImage.fromData(
                        loaded_data[0]["data"],
                        "PNG"
                    )

                    self.setImage(restored_image)
                    progoptions = loaded_data[1]
                    self.IncludeBorder = progoptions[0]
                    self.borderwidth.setValue(progoptions[1])
                    bordercol = QColor()
                    bordercol.setRgba(progoptions[2])
                    self.BorderColor.setColor(bordercol)

                    self.Annotations = []
                    self.ItemListDisplay.clear()

                    for i in range(2, len(loaded_data)):
                        aobjdata = loaded_data[i]
                        typestr = aobjdata[0]
                        skipupdate = False
                        if typestr == 'TextObject':
                            self.insertTextBox()
                        elif typestr == 'LineObject':
                            self.insertLine()
                        elif typestr == 'ArrowObject':
                            self.insertArrow()
                        elif typestr == 'RectangleObject':
                            self.insertRectangle()
                        elif typestr == 'EllipseObject':
                            self.insertEllipse()
                        elif typestr == 'ImageObject':
                            self.insertImage()
                        else:
                            skipupdate = True

                        if not skipupdate:
                            self.Annotations[-1].fromList(aobjdata)

                    for r in range(len(self.Annotations)):
                        desc = self.Annotations[r].toDisplayString()
                        desc = desc.replace('\n', ' ')
                        desc = desc.replace('\t', ' ')
                        self.ItemListDisplay.item(r).setText(desc)

                    if self.ItemListDisplay.count() > 0:
                        self.ItemListDisplay.setCurrentRow(0)
                    self.AnnotationItemChanged()
        except:
            traceback.print_exc()
            QMessageBox.warning(self, "File Not Opened", "The file " + file_name + " could not be opened.",
                                QMessageBox.Ok)

    def saveProject(self):
        """
        Saves an annotation project, the base image as well as the annotations.

        :return: None
        """
        if len(self.Annotations) == 0 or self.OriginalImage is None:
            return

        dialog = QFileDialog(self)
        dialog.setFilter(dialog.filter() | QDir.Hidden)
        dialog.setDefaultSuffix('ian')
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setNameFilters(['Image Annotator Files (*.ian)','All Files (*.*)'])
        dialog.setWindowTitle('Save Project As')

        if dialog.exec() == QDialog.Accepted:
            filelist = dialog.selectedFiles()
            if len(filelist) > 0:
                filename = filelist[0]
                try:
                    buffer = QBuffer()
                    buffer.open(QIODeviceBase.OpenModeFlag.WriteOnly)
                    self.OriginalImage.save(buffer, "PNG")
                    raw_image_bytes = buffer.data()

                    image_data = {
                        "width": self.OriginalImage.width(),
                        "height": self.OriginalImage.height(),
                        "format": self.OriginalImage.format(),
                        "data": bytes(raw_image_bytes),
                    }

                    filelist = []
                    filelist.append(image_data)
                    filelist.append([self.IncludeBorder, self.borderwidth.value(), self.BorderColor.color.rgba()])

                    for aobj in self.Annotations:
                        try:
                            filelist.append(aobj.toList())
                        except:
                            pass

                    with open(filename, "wb") as f:
                        pickle.dump(filelist, f)
                except:
                    traceback.print_exc()
                    QMessageBox.warning(self, "File Not Saved", "The file " + filename + " could not be saved.",
                                        QMessageBox.Ok)

    def openImage(self):
        """
        Opens an image to be loaded and displayed.

        :return: None
        """

        if self.OriginalImage is not None:
            message = "This will replace the base image with the selected image.  This operation cannot be undone.  "
            message += "Do you wish to change the base image?"
            res = QMessageBox.question(self, "Replace Base Image", message, QMessageBox.Yes | QMessageBox.No)

            if res == QMessageBox.No:
                return

        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "",
                                                   "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*.*)")

        try:
            if file_name:
                t = QImage()
                t.load(file_name)
                self.setImage(t)
                self.showImage = True
                self.AnnotationItemChanged()
        except:
            QMessageBox.warning(self, "File Not Opened", "The file " + file_name + " could not be opened.",
                                QMessageBox.Ok)

    def pasteImage(self):
        """
        Pastes an image to be loaded and displayed.

        :return: None
        """

        try:
            img = self.clipboard.image()
            if img is None or (img.height() == 0 and img.width() == 0):
                return

            if self.OriginalImage is not None:
                message = "This will replace the base image with the clipboard image.  This operation cannot be undone.  "
                message += "Do you wish to change the base image?"
                res = QMessageBox.question(self, "Replace Base Image", message, QMessageBox.Yes | QMessageBox.No)

                if res == QMessageBox.No:
                    return

            self.setImage(img)
            self.showImage = True
            self.AnnotationItemChanged()
        except:
            pass

    def newImage(self):
        """
        Creates a new blank base image for the annotator.

        :return: None
        """
        try:
            if self.OriginalImage is not None:
                message = "This will replace the base image with a new blank image.  This operation cannot be undone.  "
                message += "Do you wish to change the base image?"
                res = QMessageBox.question(self, "Replace Base Image", message, QMessageBox.Yes | QMessageBox.No)

                if res == QMessageBox.No:
                    return

            dialog = StringsNumbersInputDialog(self, title='Input Image Size',
                                               message='Input the width and height of the new blank image.',
                                               numMessages=['Width: ', 'Height: '],
                                               numRanges=[[10, 10000, 800], [10, 10000, 600]],
                                               spinwidth=100)

            if dialog.exec():
                w = dialog.getVal(0)
                h = dialog.getVal(1)
                img = QImage(QSize(w, h), QImage.Format.Format_ARGB32)
                img.fill(QColor(255,255,255,255))
                self.setImage(img)
                self.showImage = True
                self.AnnotationItemChanged()
        except:
            # traceback.print_exc()
            pass

    def saveImageFileAs(self):
        """
        Saves the current image to a file.

        :return: None
        """
        if self.OriginalImage is None:
            return

        dialog = QFileDialog(self)
        dialog.setFilter(dialog.filter() | QDir.Hidden)
        dialog.setDefaultSuffix('png')
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setNameFilters(['Image Files (*.png *.jpg *.jpeg *.bmp)','All Files (*.*)'])
        dialog.setWindowTitle('Save Image to File')

        if dialog.exec() == QDialog.Accepted:
            filelist = dialog.selectedFiles()
            if len(filelist) > 0:
                filename = filelist[0]
                try:
                    self.imageCanvas.image.save(filename)
                except:
                    QMessageBox.warning(self, "File Not Saved", "The file " + filename + " could not be saved.",
                                        QMessageBox.Ok)

    def printPreviewDoc(self, printer):
        """
        Creates the print preview image to be displayed in the print preview dialog.

        :param printer: Printer object.
        :return: None
        """
        if self.OriginalImage is None:
            return

        painter = QPainter()
        painter.begin(printer)
        rect = QRect(painter.viewport())
        img = self.imageCanvas.image

        size = QSize(img.size())
        if rect.width() < img.width() or rect.height() < img.height():
            size.scale(rect.size(), Qt.KeepAspectRatio)
        painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
        painter.setWindow(img.rect())
        painter.drawImage(0, 0, img)
        painter.end()

    def PrintPreviewImage(self):
        """
        Opens a print preview dialog with the current image loaded.

        :return: None
        """
        if self.OriginalImage is None:
            return

        try:
            printer = QPrinter()
            dialog = QPrintPreviewDialog(printer, self)
            printer.setDocName("CLAE Image Print")
            printer.setOutputFormat(QPrinter.NativeFormat)
            dialog.paintRequested.connect(self.printPreviewDoc)
            dialog.exec()
        except:
            QMessageBox.warning(self, "Print Preview Error", 'The current image cannot be previewed.',
                                QMessageBox.Ok)

    def printImageFile(self):
        """
        Prints the current image.

        :return: None
        """
        if self.OriginalImage is None:
            return

        try:
            printer = QPrinter()
            printer.setDocName('CLAE Image Print')
            printer.setOutputFormat(QPrinter.NativeFormat)

            print_dialog = QPrintDialog(printer, self)

            if (print_dialog.exec() == QPrintDialog.Accepted):
                painter = QPainter()
                painter.begin(printer)
                rect = QRect(painter.viewport())

                img = self.imageCanvas.image
                size = QSize(img.size())

                if rect.width() < img.width() or rect.height() < img.height():
                    size.scale(rect.size(), Qt.KeepAspectRatio)

                painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
                painter.setWindow(img.rect())
                painter.drawImage(0, 0, img)
                painter.end()
        except:
            QMessageBox.warning(self, "Print Error", 'The current image cannot be printed.',
                                QMessageBox.Ok)

    def copyImage(self):
        """
        Copies the current image to the clipboard.

        :return: None
        """
        if self.OriginalImage is None:
            return

        img = self.imageCanvas.image
        self.clipboard.setImage(img)

    def toggleBorder(self):
        """
        Toggles the display from the original image to the one with a border.

        :return: None
        """
        if self.OriginalImage is None:
            return

        self.IncludeBorder = not self.IncludeBorder
        self.UpdateImage()

    def insertTextBox(self):
        """
        Adds a text box object to the annotation list.

        :return: None
        """
        if self.OriginalImage is None:
            return

        self.Annotations.append(TextObject())
        self.ItemListDisplay.addItem(self.Annotations[-1].toDisplayString())
        self.ItemListDisplay.setCurrentRow(self.ItemListDisplay.count()-1)
        self.changeMade()

    def insertLine(self):
        """
        Adds a line object to the annotation list.

        :return: None
        """
        if self.OriginalImage is None:
            return

        self.Annotations.append(LineObject())
        self.ItemListDisplay.addItem(self.Annotations[-1].toDisplayString())
        self.ItemListDisplay.setCurrentRow(self.ItemListDisplay.count()-1)
        self.changeMade()

    def insertArrow(self):
        """
        Adds an arrow object to the annotation list.

        :return: None
        """
        if self.OriginalImage is None:
            return

        self.Annotations.append(ArrowObject())
        self.ItemListDisplay.addItem(self.Annotations[-1].toDisplayString())
        self.ItemListDisplay.setCurrentRow(self.ItemListDisplay.count()-1)
        self.changeMade()

    def insertRectangle(self):
        """
        Adds a rectangle object to the annotation list.

        :return: None
        """
        if self.OriginalImage is None:
            return

        self.Annotations.append(RectangleObject())
        self.ItemListDisplay.addItem(self.Annotations[-1].toDisplayString())
        self.ItemListDisplay.setCurrentRow(self.ItemListDisplay.count()-1)
        self.changeMade()

    def insertEllipse(self):
        """
        Adds an ellipse object to the annotation list.

        :return: None
        """
        if self.OriginalImage is None:
            return

        self.Annotations.append(EllipseObject())
        self.ItemListDisplay.addItem(self.Annotations[-1].toDisplayString())
        self.ItemListDisplay.setCurrentRow(self.ItemListDisplay.count()-1)
        self.changeMade()

    def insertImage(self):
        """
        Adds an image object to the annotation list.

        :return: None
        """
        if self.OriginalImage is None:
            return

        self.Annotations.append(ImageObject())
        self.ItemListDisplay.addItem(self.Annotations[-1].toDisplayString())
        self.ItemListDisplay.setCurrentRow(self.ItemListDisplay.count()-1)
        self.changeMade()

    def deleteAnnotation(self):
        """
        Removes the currently selected annotation.

        :return: None
        """
        r = self.ItemListDisplay.currentRow()
        if r >= 0:
            ans = QMessageBox.warning(self, "Delete Annotation",
                                "Deleting an annotation cannot be undone, are you sure you wish to delete the selected annotation.",
                                QMessageBox.Yes | QMessageBox.No)

            if ans == QMessageBox.Yes:
                try:
                    self.Annotations.pop(r)
                    self.ItemListDisplay.takeItem(r)

                    if self.ItemListDisplay.count() == 0:
                        pass
                    elif r < self.ItemListDisplay.count():
                        self.ItemListDisplay.setCurrentRow(r)
                    else:
                        self.ItemListDisplay.setCurrentRow(self.ItemListDisplay.count() - 1)

                    self.AnnotationItemChanged()
                    self.changeMade()
                except:
                    pass

    def clearAnnotations(self):
        """
        Clears the annotation list.

        :return: None
        """
        if len(self.Annotations) > 0:
            ans = QMessageBox.warning(self, "Clear Annotation List",
                                "Clearing the annotation cannot be undone, are you sure you wish to clear the annotation list.",
                                QMessageBox.Yes | QMessageBox.No)

            if ans == QMessageBox.Yes:
                try:
                    self.Annotations = []
                    self.ItemListDisplay.clear()
                    self.AnnotationItemChanged()
                    self.changeMade()
                except:
                    pass

    def aboutDialog(self):
        """
        UI for the about dialog box.
        """
        QMessageBox.about(self, self.program_title + "  Version " + self.version,
                          self.authors + "\nVersion " + self.version +
                          "\nCopyright " + self.copyright +
                          "\nDeveloped in Python using the PySide6 GUI package.\n" +
                          self.licence
                          )

    # Open the help system in the systems default browser.
    def onHelp(self):
        """
        UI for the help system.
        """
        try:
            self.url_home_string = "file://" + self.resource_path("Help/index.html")
            webbrowser.open_new(self.url_home_string)
        except:
            QMessageBox.warning(self, "Help System Error",
                                "The help system could not be opened in the system's default browser.")

    def closeEvent(self, event):
        """
        Close event override.

        :param event: Close event.
        """
        if len(self.Annotations) > 0:
            close = QMessageBox.warning(self, "Close Image Annotator",
                                        "Closing the image annotator will lose all the current annotations and settings. " + \
                                        "Are you sure want to close the program?",
                                        QMessageBox.Yes | QMessageBox.No)

            if close == QMessageBox.No:
                event.ignore()

############################################
##  Main
############################################

if __name__ == '__main__':
    """
    Initiate the program.
    """
    app = QApplication(sys.argv)
    window = ImageViewer(app)
    progcss = appcss()
    app.setStyleSheet(progcss.getCSS())
    sys.exit(app.exec())
