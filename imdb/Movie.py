"""
Movie module (imdb package).

This module provides the Movie class, used to store information about
a given movie.

Copyright 2004-2007 Davide Alberani <da@erlug.linux.it>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

from types import UnicodeType, ListType, TupleType, DictType
from copy import deepcopy

from imdb.utils import analyze_title, build_title, normalizeTitle, \
                        flatten, _Container, cmpMovies


class Movie(_Container):
    """A Movie.

    Every information about a movie can be accessed as:
        movieObject['information']
    to get a list of the kind of information stored in a
    Movie object, use the keys() method; some useful aliases
    are defined (as "casting" for the "casting director" key); see
    the keys_alias dictionary.
    """
    # The default sets of information retrieved.
    default_info = ('main', 'plot')

    # Aliases for some not-so-intuitive keys.
    keys_alias = {
                'user rating':  'rating',
                'plot summary': 'plot',
                'plot summaries': 'plot',
                'directed by':  'director',
                'created by': 'creator',
                'writing credits': 'writer',
                'produced by':  'producer',
                #'composer': 'original music',
                'original music by':    'original music',
                'non-original music by':    'non-original music',
                'music':    'original music',
                'cinematography by':    'cinematographer',
                'cinematography':   'cinematographer',
                'film editing by':  'editor',
                'film editing': 'editor',
                'editing':  'editor',
                'actors':   'cast',
                'actresses':    'cast',
                'casting by':   'casting director',
                'casting':  'casting director',
                'art direction by': 'art direction',
                #'art director': 'art direction',
                'set decoration by':    'set decoration',
                #'set decorator': 'set decoration',
                'costume design by':    'costume designer',
                'costume design':    'costume designer',
                'makeup department':    'make up',
                'makeup':    'make up',
                'make-up':    'make up',
                'production management':    'production manager',
                'second unit director or assistant director':
                                                'assistant director',
                'second unit director':   'assistant director',
                'sound department': 'sound crew',
                'costume and wardrobe department': 'costume department',
                'special effects by':   'special effects',
                'visual effects by':    'visual effects',
                'stunts':   'stunt performer',
                'other crew':   'miscellaneous crew',
                'misc crew':   'miscellaneous crew',
                'miscellaneouscrew':   'miscellaneous crew',
                'crewmembers': 'miscellaneous crew',
                'crew members': 'miscellaneous crew',
                'other companies': 'miscellaneous companies',
                'misc companies': 'miscellaneous companies',
                'aka':  'akas',
                'also known as':    'akas',
                'country':  'countries',
                'genre': 'genres',
                'runtime':  'runtimes',
                'lang': 'languages',
                'color': 'color info',
                'cover': 'cover url',
                'seasons': 'number of seasons',
                'language': 'languages',
                'certificate':  'certificates',
                'certifications':   'certificates',
                'certification':    'certificates',
                'miscellaneous links':  'misc links',
                'miscellaneous':    'misc links',
                'soundclips':   'sound clips',
                'videoclips':   'video clips',
                'photographs':  'photo sites',
                'distributor': 'distributors',
                'distribution': 'distributors',
                'distribution companies': 'distributors',
                'guest': 'guests',
                'guest appearances': 'guests',
                'tv guests': 'guests',
                'notable tv guest appearances': 'guests',
                'episodes cast': 'guests',
                'episodes number': 'number of episodes',
                'amazon review': 'amazon reviews',
                'merchandising': 'merchandising links',
                'merchandise': 'merchandising links',
                'sales': 'merchandising links',
                'faq': 'faqs',
                'parental guide': 'parents guide',
                'frequently asked questions': 'faqs'}

    keys_tomodify_list = ('plot', 'trivia', 'alternate versions', 'goofs',
                        'quotes', 'dvd', 'laserdisc', 'news', 'soundtrack',
                        'crazy credits', 'business', 'supplements',
                        'video review', 'faqs')

    cmpFunct = cmpMovies

    def _init(self, **kwds):
        """Initialize a Movie object.

        *movieID* -- the unique identifier for the movie.
        *title* -- the title of the Movie, if not in the data dictionary.
        *myTitle* -- your personal title for the movie.
        *myID* -- your personal identifier for the movie.
        *data* -- a dictionary used to initialize the object.
        *currentRole* -- a string representing the current role or duty
                        of a person in this movie.
        *notes* -- notes for the person referred in the currentRole
                    attribute; e.g.: '(voice)'.
        *accessSystem* -- a string representing the data access system used.
        *titlesRefs* -- a dictionary with references to movies.
        *namesRefs* -- a dictionary with references to persons.
        *modFunct* -- function called returning text fields.
        """
        title = kwds.get('title')
        if title and not self.data.has_key('title'):
            self.set_title(title)
        self.movieID = kwds.get('movieID', None)
        self.myTitle = kwds.get('myTitle', u'')

    def _reset(self):
        """Reset the Movie object."""
        self.movieID = None
        self.myTitle = u''

    def set_title(self, title):
        """Set the title of the movie."""
        # XXX: convert title to unicode, if it's a plain string?
        d_title = analyze_title(title, canonical=1)
        self.data.update(d_title)

    def _additional_keys(self):
        """Valid keys to append to the data.keys() list."""
        addkeys = []
        if self.data.has_key('title'):
            addkeys += ['canonical title', 'long imdb title',
                        'long imdb canonical title']
        if self.data.has_key('episode of'):
            addkeys += ['long imdb episode title', 'series title',
                        'canonical series title', 'episode title',
                        'canonical episode title']
        return addkeys

    def _getitem(self, key):
        """Handle special keys."""
        if self.data.has_key('episode of'):
            if key == 'long imdb episode title':
                return build_title(self.data, canonical=0)
            elif key == 'series title':
                ser_title = self.data['episode of'].get('canonical title') or \
                            self.data['episode of']['title']
                return normalizeTitle(ser_title)
            elif key == 'canonical series title':
                ser_title = self.data['episode of'].get('canonical title') or \
                            self.data['episode of']['title']
                return ser_title
            elif key == 'episode title':
                return normalizeTitle(self.data.get('title', u''))
            elif key == 'canonical episode title':
                return self.data.get('title', u'')
        if self.data.has_key('title'):
            if key == 'title':
                return normalizeTitle(self.data['title'])
            elif key == 'long imdb title':
                return build_title(self.data, canonical=0)
            elif key == 'canonical title':
                return self.data['title']
            elif key == 'long imdb canonical title':
                return build_title(self.data, canonical=1)
        return None

    def getID(self):
        """Return the movieID."""
        return self.movieID

    def __nonzero__(self):
        """The Movie is "false" if the self.data does not contain a title."""
        # XXX: check the title and the movieID?
        if self.data.has_key('title'): return 1
        return 0

    def isSameTitle(self, other):
        """Return true if this and the compared object have the same
        long imdb title and/or movieID.
        """
        # XXX: obsolete?
        if not isinstance(other, self.__class__): return 0
        if self.data.has_key('title') and \
                other.data.has_key('title') and \
                build_title(self.data, canonical=1) == \
                build_title(other.data, canonical=1):
            return 1
        if self.accessSystem == other.accessSystem and \
                self.movieID is not None and self.movieID == other.movieID:
            return 1
        return 0
    isSameMovie = isSameTitle # XXX: just for backward compatiblity.

    def __contains__(self, item):
        """Return true if the given Person object is listed in this Movie."""
        from Person import Person
        if not isinstance(item, Person):
            return 0
        for p in flatten(self.data, yieldDictKeys=1, scalar=Person,
                        toDescend=(ListType, DictType, TupleType, Movie)):
            if item.isSame(p):
                return 1
        return 0

    def __deepcopy__(self, memo):
        """Return a deep copy of a Movie instance."""
        m = Movie(title=u'', movieID=self.movieID, myTitle=self.myTitle,
                    myID=self.myID, data=deepcopy(self.data, memo),
                    currentRole=self.currentRole, notes=self.notes,
                    accessSystem=self.accessSystem,
                    titlesRefs=deepcopy(self.titlesRefs, memo),
                    namesRefs=deepcopy(self.namesRefs, memo))
        m.current_info = list(self.current_info)
        m.set_mod_funct(self.modFunct)
        return m

    def __repr__(self):
        """String representation of a Movie object."""
        # XXX: add also currentRole and notes, if present?
        if self.has_key('long imdb episode title'):
            title = self.get('long imdb episode title')
        else:
            title = self.get('long imdb canonical title')
        r = '<Movie id:%s[%s] title:_%s_>' % (self.movieID, self.accessSystem,
                                                title)
        if isinstance(r, UnicodeType): r = r.encode('utf_8', 'replace')
        return r

    def __str__(self):
        """Simply print the short title."""
        return self.get('title', u'').encode('utf_8', 'replace')

    def __unicode__(self):
        """Simply print the short title."""
        return self.get('title', u'')

    def summary(self):
        """Return a string with a pretty-printed summary for the movie."""
        if not self: return u''
        def _nameAndRole(personList, joiner=', '):
            """Build a pretty string with name and role."""
            nl = []
            for person in personList:
                n = person.get('name', u'')
                if person.currentRole: n += ' (%s)' % person.currentRole
                nl.append(n)
            return joiner.join(nl)
        s = 'Movie\n=====\nTitle: %s\n' % \
                    self.get('long imdb canonical title', u'')
        genres = self.get('genres')
        if genres: s += 'Genres: %s.' % ', '.join(genres)
        director = self.get('director')
        if director:
            s += 'Director: %s.\n' % _nameAndRole(director)
        writer = self.get('writer')
        if writer:
            s += 'Writer: %s.\n' % _nameAndRole(writer)
        cast = self.get('cast')
        if cast:
            cast = cast[:5]
            s += 'Cast: %s.\n' % _nameAndRole(cast)
        runtime = self.get('runtimes')
        if runtime:
            s += 'Runtime: %s.\n' % ', '.join(runtime)
        countries = self.get('countries')
        if countries:
            s += 'Country: %s.\n' % ', '.join(countries)
        lang = self.get('languages')
        if lang:
            s += 'Language: %s.\n' % ', '.join(lang)
        rating = self.get('rating')
        if rating:
            s += 'Rating: %s' % rating
            nr_votes = self.get('votes')
            if nr_votes:
                s += '(%s votes)' % nr_votes
            s += '.\n'
        plot = self.get('plot')
        if plot:
            plot = plot[0]
            i = plot.find('::')
            if i != -1:
                plot = plot[i+2:]
            s += 'Plot: %s' % plot
        return s


