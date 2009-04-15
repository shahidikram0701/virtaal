#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2009 Zuza Software Foundation
#
# This file is part of Virtaal.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

import gtk
from translate.storage.placeables import base, StringElem


class StringElemGUI(object):
    """
    A convenient container for all GUI properties of a L{StringElem}.
    """

    # MEMBERS #
    fg = '#000000'
    """The current foreground colour."""
    bg = '#ffffff'
    """The current background colour."""

    cursor_allowed = True
    """Whether the cursor is allowed to enter this element."""


    # INITIALIZERS #
    def __init__(self, elem, textbox, **kwargs):
        if not isinstance(elem, StringElem):
            raise ValueError('"elem" parameter must be a StringElem.')
        self.elem = elem
        self.textbox = textbox
        self.marks = {}

        attribs = ('fg', 'bg', 'cursor_allowed')
        for kw in kwargs:
            if kw in attribs:
                setattr(self, kw, kwargs[kw])

    # METHODS #
    def create_tags(self):
        tag = gtk.TextTag()
        if self.fg:
            tag.props.foreground = self.fg

        if self.bg:
            tag.props.background = self.bg

        return [(tag, None, None)]

    def create_widget(self):
        return None

    def copy(self):
        return self.__class__(
            elem=self.elem, textbox=self.textbox,
            fg=self.fg, bg=self.bg,
            cursor_allowed=self.cursor_allowed
        )

    def get_prefix(self):
        return ''

    def get_postfix(self):
        return ''

    def render(self, elem):
        assert elem is self.elem
        childstr = u''
        for sub in self.elem.sub:
            childstr += unicode(sub)
        return u'%s%s%s' % (self.get_prefix(), childstr, self.get_postfix())


class PhGUI(StringElemGUI):
    fg = 'darkred'
    bg = '#f7f7f7'


class GPlaceableGUI(StringElemGUI):
    fg = '#f7f7f7'
    bg = 'darkred'

    def create_tags(self):
        metatag = gtk.TextTag()
        metatag.props.foreground = self.fg
        metatag.props.background = self.bg

        ttag = gtk.TextTag()
        ttag.props.foreground = StringElemGUI.fg
        ttag.props.background = 'yellow'

        prefixlen = len(self.get_prefix())
        return [
            (metatag, 0, -1),
            (ttag, prefixlen, -2),
        ]

    def get_prefix(self):
        return u'%s{' % (self.elem.id)

    def get_postfix(self):
        return u'}'


element_gui_map = [
    (base.Ph, PhGUI),
    (base.G, GPlaceableGUI),
]