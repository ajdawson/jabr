"""Get journal abbreviations from the ISI website."""
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
import urllib2

from parser import ISIJournalParser


class JournalAbbreviator(object):
    """Get journal abbreviations."""

    def __init__(self):
        self._cache = {}

    def lookup_journal(self, title):
        """Return the abbreviation for a journal title.

        Raises ValueError if the journal title is not found.

        **Argument:**
        
        *title*
            Journal title.

        """
        initial_letter = title[0].lower()
        if initial_letter in self._cache.keys():
            journals = self._cache[initial_letter]
        else:
            journals = self._retrieve_journals(initial_letter)
        try:
            abbreviation = journals[title.upper()]
        except KeyError:
            raise ValueError('journal not found: {}'.format(title))
        return abbreviation

    def _retrieve_journals(self, initial_letter):
        url = 'http://images.webofknowledge.com/WOK46/help/WOS/{}_abrvjt.html'
        f = urllib2.urlopen(url.format(initial_letter.upper()))
        html = f.read()
        f.close()
        parser = ISIJournalParser()
        parser.feed(html)
        parser.finalize()
        self._cache[initial_letter] = {}
        iterlist = zip(parser.journal_names, parser.journal_abbreviations)
        for title, abbreviation in iterlist:
            self._cache[initial_letter][title.upper()] = abbreviation.upper()
        return self._cache[initial_letter]

