# THE currentRole ATTRIBUTE AND THE Character CLASS

Since version 3.3, IMDbPY supports the character pages of the IMDb
database; this required some substantial changes to how actors'
and acresses' roles were handled.
Starting with release 3.4, "sql" data access system is supported,
too - but it works a bit differently from "http".
See "SQL" below.

The currentRole instance attribute can be found in every instance
of Person, Movie and Character classes, even if actually the Character
never uses it.

The currentRole of a Person object is set to a Character instance,
inside a list of person who acted in a given movie.
The currentRole of a Movie object is set to a Character instance,
inside a list of movies played be given person.
The currentRole of a Movie object is set to a Person instance,
inside a list of movies in which a given character was portrayed.

Schema:
  movie['cast'][0].currentRole -> a Character object.
                |
                +-> a Person object.

  person['actor'][0].currentRole -> a Character object.
                  |
                  +-> a Movie object.

  character['filmography'][0].currentRole -> a Person object.
                           |
                           +-> a Movie object.

The roleID attribute can be used to access/set the characterID
or personID instance attribute of the current currentRole.
Building Movie or Person objects, you can pass the currentRole
parameter and the roleID parameter (to set the ID).
The currentRole parameter can be an object (Character or Person),
an unicode string (in which case a Character or Person object is
automatically instanced) or a list of objects or strings (to
handle multiple characters played by the same actor/actress in
a movie, or character played by more then a single actor/actress
in the same movie).

Anyway, currentRole objects (Character or Person instances) can
be pretty-printed easily: calling unicode(CharacterOrPersonObject)
will return a good-old-unicode string, like expected in the previous
version of IMDbPY.


# SQL

Fetching data from the web, only characters with an active page
on the web site will have their characterID; we don't have these
information accessing "sql", so _every_ character will have an
associated characterID.
This way, every character with the same name will share the same
characterID, even if - in fact - they may not be portraying the
same character.


# GOODIES

To help getting the required information from Movie, Person and
Character objects, in the "helpers" module there's a new factory
function, makeObject2Txt, which can be used to create your
pretty-printing function.
It takes some optional parameters: movieTxt, personTxt, characterTxt
and companyTxt; in these strings %(value)s items are replaced with
object['value'] or with obj.value (if the first is not present).

E.g.:
  import imdb
  myPrint = imdb.helpers.makeObject2Txt(personTxt=u'%(name)s ... %(currentRole)s')
  i = imdb.IMDb()
  m = i.get_movie('0057012')
  ps = m['cast'][0]
  print(myPrint(ps))
  # The output will be something like:
  Peter Sellers ... Group Captain Lionel Mandrake / President Merkin Muffley / Dr. Strangelove


Portions of the formatting string can be stripped conditionally: if
the specified condition is false, they will be cancelled.

E.g.:
  myPrint = imdb.helpers.makeObject2Txt(personTxt='<if personID><a href=/person/%(personID)s></if personID>%(long imdb name)s<if personID></a></if personID><if currentRole> ... %(currentRole)s<if notes> %(notes)s</if notes></if currentRole>'


Another useful argument is 'applyToValues': if set to a function,
it will be applied to every value before the substitution; it can
be useful to format strings for html output.

