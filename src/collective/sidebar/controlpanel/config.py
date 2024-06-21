# -*- coding: utf-8 -*-

from collective.sidebar import _
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


positionTerms = [
    SimpleTerm(
        value=u'start',
        title=_(u'left_in_ltr', default=u'Left (in LTR)'),
    ),
    SimpleTerm(
        value=u'end',
        title=_(u'right_in_ltr', default=u'Right (in LTR)'),
    ),
]

PositionVocabulary = SimpleVocabulary(positionTerms)
