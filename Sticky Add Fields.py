#-*- coding: utf-8 -*-

"""
DESCRIPTION:
Adds checkboxes to each field in the Add Items dialog so that they are
not cleared after clicking add.

I personally use this for adding a few sentences from the same place,
to avoid having to type/paste the same URL or title into my "Source"
field multiple times.

See http://sartak.org/misc/anki-add.png for this plugin and
"Add Suspended" in action.

AUTHOR:
Shawn M Moore (sartak@gmail.com)
"""

from ankiqt.ui.addcards import AddCards
from ankiqt.ui.facteditor import FactEditor
from anki.hooks import wrap
from anki.utils import tidyHTML
from PyQt4.QtGui import *
from PyQt4.QtCore import *

# for AddCards:
def initializeNewFact(self, old_fact, **kw):
    f = kw['_old'](self, old_fact)

    editor = self.editor

    for field_name, checkbox in editor.checkboxes.items():
        if checkbox.isChecked():
            f[field_name] = old_fact[field_name]
            editor.sticky_value[field_name] = f[field_name]
        elif field_name in editor.sticky_value:
            del editor.sticky_value[field_name]

    return f

# for FactEditor:
def addAdditionalAttrs(self, field, n):
    self.checkboxes = {}
    self.sticky_value = {}

def addCheckBox(self, field, n):
    if self.addMode:
        c = QCheckBox()
        c.setToolTip(_("Sticky: keep this value between successive Adds"))
        self.checkboxes[field.name] = c
        self.fieldsGrid.addWidget(c, n, 2)

def fieldsAreBlank(self):
    for (field, widget) in self.fields.values():
        value = tidyHTML(unicode(widget.toHtml()))
        if (self.addMode and value != self.sticky_value.get(field.name, '')):
            if value:
                return False
    return True

#Setup our hooks
if __name__ != '__main__':
    AddCards.initializeNewFact = wrap(AddCards.initializeNewFact, initializeNewFact, "around")
    FactEditor.drawFields = wrap(FactEditor.drawFields, addAdditionalAttrs, "before")
    FactEditor.drawField = wrap(FactEditor.drawField, addCheckBox, "after")
    FactEditor.fieldsAreBlank = fieldsAreBlank

