# -*- coding: utf-8 -*-

from collective.sidebar.testing import COLLECTIVE_SIDEBAR_INTEGRATION_TESTING
from plone import api

import unittest


class TestSidebarUtilsFunctional(unittest.TestCase):

    layer = COLLECTIVE_SIDEBAR_INTEGRATION_TESTING

    def test_crop(self):
        from collective.sidebar.utils import crop
        self.assertEqual(crop(u'just text', 6), u'just...')
        self.assertEqual(crop(u'just text', 100), u'just text')
        self.assertEqual(crop(u'.sonderzeichen:,;', 15), u'sonderzeichen...')
        self.assertEqual(crop(u'.sonderzeichen:,;', 18), u'.sonderzeichen:,;')
        self.assertEqual(crop(u'12345678910', 5), u'12345...')
        self.assertEqual(crop(u'This should be:cropping', 20), u'This should be...')  # noqa

    def test_get_icon(self):
        from collective.sidebar.utils import get_icon
        self.assertEqual(get_icon('__prefix__'), 'glyphicon')
        self.assertEqual(get_icon('_unknown_icon_'), 'glyphicon _unknown_icon_')  # noqa
        self.assertEqual(get_icon('cut'), 'glyphicon glyphicon-scissors')

        api.portal.set_registry_record(name='collective.sidebar.icon_font', value='Fontello')  # noqa
        self.assertEqual(get_icon('__prefix__'), 'icon')
        self.assertEqual(get_icon('_unknown_icon_'), 'icon _unknown_icon_')
        self.assertEqual(get_icon('cut'), 'icon cut')

        api.portal.set_registry_record(name='collective.sidebar.icon_font', value='Font Awesome')  # noqa
        self.assertEqual(get_icon('__prefix__'), 'fas')
        self.assertEqual(get_icon('_unknown_icon_'), 'fas _unknown_icon_')
        self.assertEqual(get_icon('cut'), 'fas fa-cut')
        self.assertEqual(get_icon('paste'), 'far fa-clipboard')

        api.portal.set_registry_record(name='collective.sidebar.icon_font', value='Font Awesome Pro')  # noqa
        self.assertEqual(get_icon('__prefix__'), 'far')
        self.assertEqual(get_icon('_unknown_icon_'), 'far _unknown_icon_')
        self.assertEqual(get_icon('cut'), 'far fa-cut')

        api.portal.set_registry_record(name='collective.sidebar.icon_font', value='Font Awesome Light')  # noqa
        self.assertEqual(get_icon('__prefix__'), 'fal')
        self.assertEqual(get_icon('_unknown_icon_'), 'fal _unknown_icon_')
        self.assertEqual(get_icon('cut'), 'fal fa-cut')

        api.portal.set_registry_record(name='collective.sidebar.icon_font', value='Font Awesome Duotone')  # noqa
        self.assertEqual(get_icon('__prefix__'), 'fad')
        self.assertEqual(get_icon('_unknown_icon_'), 'fad _unknown_icon_')
        self.assertEqual(get_icon('cut'), 'fad fa-cut')
