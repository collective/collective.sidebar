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


fonts = [
    SimpleTerm(value=u'Bootstrap', title=u'Bootstrap'),
    SimpleTerm(value=u'Glyphicons', title=u'Glyphicons'),
    SimpleTerm(value=u'Fontello', title=u'Fontello'),
    SimpleTerm(value=u'Font Awesome', title=u'Font Awesome'),
    SimpleTerm(value=u'Font Awesome Pro', title=u'Font Awesome Pro'),
    SimpleTerm(value=u'Font Awesome Light', title=u'Font Awesome Light'),
    SimpleTerm(value=u'Font Awesome Duotone', title=u'Font Awesome Duotone'),
]

IconFontVocabulary = SimpleVocabulary(fonts)
