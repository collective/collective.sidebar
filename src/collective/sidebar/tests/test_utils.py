# -*- coding: utf-8 -*-

from collective.sidebar.testing import COLLECTIVE_SIDEBAR_INTEGRATION_TESTING

import unittest


class TestSidebarUtilsFunctional(unittest.TestCase):

    layer = COLLECTIVE_SIDEBAR_INTEGRATION_TESTING

    def test_crop(self):
        from collective.sidebar.utils import crop
        self.assertEqual(crop(u'just text', 6), u'just...')
        self.assertEqual(crop(u'just text', 100), u'just text')
        self.assertEqual(crop(u'12345678910', 5), u'...')
        self.assertEqual(crop(u'.sonderzeichen:,;', 15), u'...')

        # I think crop() should be refactored to make these true:
        # self.assertEqual(crop(u'12345678910', 5), u'12345...')
        # self.assertEqual(crop(u'.sonderzeichen:,;', 17), u'sonderzeichen...')  # noqa
        # self.assertEqual(crop(u'This should be:cropping', 20), u'This should be...')  # noqa
