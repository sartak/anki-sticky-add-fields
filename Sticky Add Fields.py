#-*- coding: utf-8 -*-

"""
DESCRIPTION:
Adds checkboxes to each field in the Add Items dialog so that they are
not cleared after clicking add.

I personally use this for adding a few sentences from the same place,
to avoid having to type/paste the same URL or title into my "Source"
field multiple times.

AUTHOR:
Shawn M Moore (sartak@gmail.com)
"""

from ankiqt.ui.addcards import AddCards
from ankiqt.ui.facteditor import FactEditor
from anki.hooks import wrap
from PyQt4.QtGui import *
from PyQt4.QtCore import *

# for AddCards:
def initializeNewFact(self, old_fact, **kw):
    f = kw['_old'](self, old_fact)

    for field_name, checkbox in self.editor.checkboxes.items():
        if checkbox.isChecked():
            f[field_name] = old_fact[field_name]

    return f

# for FactEditor:
def addCheckBoxAttr(self, field, n):
    self.checkboxes = {}

def addCheckBox(self, field, n):
    if self.addMode:
        c = QCheckBox()
        c.setToolTip(_("Sticky: keep this value between successive Adds"))
        self.checkboxes[field.name] = c
        self.fieldsGrid.addWidget(c, n, 2)

#Setup our hooks
if not __name__ == "__main__":
    AddCards.initializeNewFact = wrap(AddCards.initializeNewFact, initializeNewFact, "around")
    FactEditor.drawFields = wrap(FactEditor.drawFields, addCheckBoxAttr, "before")
    FactEditor.drawField = wrap(FactEditor.drawField, addCheckBox, "after")

