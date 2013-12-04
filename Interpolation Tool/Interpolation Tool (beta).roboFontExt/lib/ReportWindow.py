#Embedded file name: /Users/alexander/Documents/WORKS/typedev/RoboFont/dev/OutputWindow.py
"""
RoboFont Script
ReportWindow.py

Created by Alexander Lubovenko on 2013-10-24.
http://github.com/typedev
"""
from vanilla import *
from AppKit import *
# import codecs
from time import asctime
import sys, subprocess

class ReportWindow(object):

    def __init__(self, titleReport = 'Report'):
        global _bufferTxT
        self.w = FloatingWindow((900, 500), title = titleReport, minSize=(360, 270))
        self.w.textBox = TextEditor((0, 0, 0, -50), '')
        self.w.textBox.getNSTextView().setRichText_(False)
        self.w.textBox.getNSTextView().setUsesFontPanel_(False)
        color = NSColor.colorWithCalibratedRed_green_blue_alpha_(20.0 / 255.0, 20.0 / 255.0, 20.0 / 255.0, 1)
        self.w.textBox.getNSTextView().setBackgroundColor_(color)
        self.w.textBox.getNSTextView().setTextColor_(NSColor.whiteColor())
        self.w.textBox.getNSTextView().setFont_(NSFont.fontWithName_size_('Menlo', 14))
        self.w.btnClose = Button((-80, -40, 65, 22), 'Close', callback=self.btnCloseCallback)
        self.w.center()
        self.report = []

    def btnCloseCallback(self, sender):
        self.w.hide()

    def showReport(self):
        text = '\n'.join(self.report)
        self.w.textBox.set(text)
        self.w.textBox.getNSTextView().scrollRangeToVisible_((len(text), 0))
        self.w.center()
        self.w.show()

    def addToReport(self, txt = ''):
        self.report.append(txt)


if __name__ == '__main__':
    report = ReportWindow(titleReport = 'Test ReportWindow')
    for i in range(10):
        report.addToReport(str(i) +'. Test Report Window. '+asctime())
        # report.addToReport('Test Report Window 2'+asctime())
    report.showReport()