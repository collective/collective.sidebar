# -*- coding: utf-8 -*-

from collective.sidebar import _
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


positionTerms = [
    SimpleTerm(value=u'left', title=_(u'choice_left', default=u'Left')),
    SimpleTerm(value=u'right', title=_(u'choice_right', default=u'Right')),
]

positionVocabulary = SimpleVocabulary(positionTerms)
