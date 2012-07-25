"""Parse ISI journal abbreviations website."""
# Copyright (c) 2012 Andrew Dawson
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
try:
    from html.parser import HTMLParser
except ImportError:
    from HTMLParser import HTMLParser


class ISIJournalParser(HTMLParser):
    """Parser for ISI Web of Knowledge journal abbreviation pages.
    
    **Note:**
        Due to the ISI pages containing malformed html one must call
        the :py:meth:`ISIJournalParser.finalize` method once
        parsing is complete to ensure all entries are read correctly.
    
    """

    def __init__(self):
        HTMLParser.__init__(self)
        self.journal_names = []
        self.journal_abbreviations = []
        self.parser_state = None
        self.data_entities = None

    def handle_starttag(self, tag, attrs):
        if tag not in ('dd', 'dt'):
            return
        self._storedata()
        self.parser_state = tag
        self.data_entities = []

    def handle_data(self, data):
        if self.parser_state in ('dd', 'dt'):
            self.data_entities.append(data)

    def _storedata(self):
        if self.data_entities and self.parser_state:
            if self.parser_state == 'dt':
                self.journal_names.append(''.join(self.data_entities).strip())
            elif self.parser_state == 'dd':
                self.journal_abbreviations.append(''.join(self.data_entities).strip())

    def finalize(self):
        """Ensures all data is stored.

        This method must be called when parsing is complete.

        """
        self._storedata()

