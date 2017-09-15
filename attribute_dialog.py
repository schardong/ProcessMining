#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Implements the classes to create an attribute selection dialog.
"""

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QDialog, QDialogButtonBox, QStyleFactory, QWidget)


class AttributeDialog(QDialog):
    """
    """

    def __init__(self):
        super(QDialog, self).__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)
        self._title = 'Attribute Selection'

        # UI elements.
        self._build_ui()

    def set_attributes(self, attr_list):
        pass

    def _build_ui(self):
        btn_box = QDialogButtonBox(
            QDialogButtonBox.Ok + QDialogButtonBox.Cancel, parent=self)


def main():
    QApplication.setStyle(QStyleFactory.create('Fusion'))
    app = QApplication(sys.argv)
    dlg = AttributeDialog()
    dlg.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
