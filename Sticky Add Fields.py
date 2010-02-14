#-*- coding: utf-8 -*-

"""
DESCRIPTION:
Adds checkboxes to each field in the Add Items dialog so that they are
not cleared after clicking add.

I personally use this for adding a few sentences from the same place,
to avoid having to type/paste the same URL or title multiple times.

AUTHOR:
Shawn M Moore (sartak@gmail.com)
"""

from ankiqt.ui.addcards import AddCards
from anki.hooks import wrap
from PyQt4.QtGui import *
from PyQt4.QtCore import *

def initializeNewFact(self, old_fact):
    f = self.parent.deck.newFact()
    f.tags = self.parent.deck.lastTags
    return f

def clearOldFact(self, old_fact):
    f = self.initializeNewFact(old_fact)
    self.editor.setFact(f, check=True, scroll=True)
    # let completer know our extra tags
    self.editor.tags.addTags(parseTags(self.parent.deck.lastTags))
    return f

from anki.utils import stripHTML, parseTags
from anki.sound import clearAudioQueue
def addCards(self):
    # make sure updated
    self.editor.saveFieldsNow()
    fact = self.editor.fact
    n = _("Add")
    self.parent.deck.setUndoStart(n)
    try:
        fact = self.parent.deck.addFact(fact)
    except FactInvalidError:
        ui.utils.showInfo(_(
            "Some fields are missing or not unique."),
                            parent=self, help="AddItems#AddError")
        return
    if not fact:
        ui.utils.showWarning(_("""\
The input you have provided would make an empty
question or answer on all cards."""), parent=self)
        return
    self.dialog.status.append(
        _("Added %(num)d card(s) for <a href=\"%(id)d\">"
            "%(str)s</a>.") % {
        "num": len(fact.cards),
        "id": fact.id,
        # we're guaranteed that all fields will exist now
        "str": stripHTML(fact[fact.fields[0].name]),
        })

    # stop anything playing
    clearAudioQueue()

    self.parent.deck.setUndoEnd(n)
    self.parent.deck.checkDue()
    self.parent.updateTitleBar()
    self.parent.statusView.redraw()

    # start a new fact
    self.clearOldFact(fact)

    self.maybeSave()

#Setup our hook
if not __name__ == "__main__":
    AddCards.clearOldFact = clearOldFact
    AddCards.addCards = addCards

