# -*- coding: utf-8 -*-

"""Operations on names: shortening, normalizing, ...

   TODO: This module should be connected to the names database.

"""
import sys

import re


class Name2Long(ValueError):
    "The name is too long and cannot be shortened."


_mixedcase = re.compile(ur'[A-ZÆØÅ][a-zæøå]+[A-ZÆØÅ]')
_mcmac = re.compile(ur'(?P<prefix>(Mc)|(Mac)|(Van)|(Von))(?P<sfx>.*)',
                    re.IGNORECASE)


def normalize(fornavn, etternavn):
    """Normalize double spaces and title case.
    """
    fname = u' '.join(fornavn.split()).title()
    lname = u' '.join(etternavn.split())

    # if already mixed case, assume they know what they're doing
    if not _mixedcase.match(lname):
        m = _mcmac.match(lname)

        if m:
            g = m.groupdict()
            lname = g['prefix'].title() + g['sfx'].title()
        else:
            lname = lname.title()

    return fname, lname


def forkort_navn(lengde, fornavn, etternavn):
    "Shorten names and return the result as a string."
    fname, lname = shorten(lengde, fornavn, etternavn)
    return fname + u' ' + lname


def shorten_fname(length, fname):
    """Try to shorten the first-name `fname` to `length` characters
       (raise ValueError if we fail).

       Algorithm: Consider the last of the person's first names and replace it
                  with its initial. If the resulting name is still too long,
                  then call ourselves recursively.
    """
    if len(fname) <= length:
        return fname

    firstnames = fname.split()
    for i in range(len(firstnames) - 1, 0, -1):
        if len(firstnames[i]) > 1:
            tmp = ' '.join(firstnames[:i] +
                           [firstnames[i][0]] +
                           firstnames[i + 1:])
            return shorten_fname(length, tmp)

    raise Name2Long('%r kan ikke forkortes til %d bokstaver' % (fname, length))


def shorten_lname(length, lname):
    """Try to shorten the last-name `lname` to `length` characters
       (raise ValueError if we fail).

       Algorithm: Consider the first of the person's last names and replace it
                  with its initial. If the resulting name is still too long,
                  then call ourselves recursively.
    """
    if len(lname) <= length:
        return lname

    lastnames = lname.split()
    for i in range(len(lastnames) - 1):
        if len(lastnames[i]) > 1:
            tmp = ' '.join(lastnames[:i] +
                           [lastnames[i][0]] +
                           lastnames[i + 1:])
            return shorten_lname(length, tmp)

    raise Name2Long('%r kan ikke forkortes til %d bokstaver' % (lname, length))


def shorten(lengde, fornavn, etternavn):
    """Apply algorithms described above, first to first-names, then to
       last-names.  Return tuple of (fornavn, etternavn).
    """
    if len(fornavn) + len(etternavn) + 1 <= lengde:
        return (fornavn.lower().title(), etternavn.lower().title())

    firstnames = fornavn.split()
    for i in range(len(firstnames) - 1, 0, -1):
        if len(firstnames[i]) > 1:
            tmp = ' '.join(firstnames[:i] +
                           [firstnames[i][0]] +
                           firstnames[i + 1:])
            return shorten(lengde, tmp, etternavn)

    lastnames = etternavn.split()
    for i in range(len(lastnames) - 1):
        if len(lastnames[i]) > 1:
            tmp = ' '.join(lastnames[:i] +
                           [lastnames[i][0]] +
                           lastnames[i + 1:])
            return shorten(lengde, fornavn, tmp)

    raise Name2Long('%r %r kan ikke forkortes til %d bokstaver' % (
        fornavn, etternavn, lengde))


def combine(fornavn, etternavn):
    """Combine `fornavn` and `etternavn` with a space in-between.
       Remove any double spaces and fix capitalization.
    """
    return u' '.join(shorten(sys.maxint, *normalize(fornavn, etternavn)))


# old code that works on utf-8 strings (should be removed..):

def normalize2uni(navn_u8):
    "Normalized := Unicode And Title Case."
    if type(navn_u8) != unicode:
        navn_u8 = navn_u8.decode('u8')
    normcase = navn_u8.lower().title()
    return normcase


def normalize2u8(navn):
    "Normalized := Utf-8 And Title Case."
    if type(navn) != unicode:
        navn = navn.decode('u8')
    normcase = navn.lower().title()
    return normcase.encode('u8')


def shorten_fname_u8(length, fname):
    return normalize2u8(shorten_fname(length, normalize2uni(fname)))


def shorten_lname_u8(length, lname):
    return normalize2u8(shorten_lname(length, normalize2uni(lname)))


def forkort_navn_u8(lengde, fornavn_u8, etternavn_u8):
    fname = normalize2uni(fornavn_u8)
    lname = normalize2uni(etternavn_u8)
    res = forkort_navn(lengde, fname, lname)
    return normalize2u8(res)


def shorten_u8(lengde, fornavn, etternavn):
    fname = normalize2uni(fornavn)
    lname = normalize2uni(etternavn)
    fname, lname = shorten(lengde, fname, lname)
    return normalize2u8(fname), normalize2u8(lname)

# -- end old code ---.


def test_module():
    """
       >>> forkort_navn(25, 'Bjorn Steinar', 'Fjeld Pettersen')
       u'Bjorn S Fjeld Pettersen'
       >>> forkort_navn(22, 'Bjorn Steinar', 'Fjeld Pettersen')
       u'Bjorn S F Pettersen'
       >>> forkort_navn(18, 'Bjorn Steinar', 'Fjeld Pettersen')
       Traceback (most recent call last):
       ...
       ValueError: Bjorn S F Pettersen kan ikke forkortes til 18 bokstaver

       >>> v = forkort_navn(25, u'Bjørn Øystein', u'Fjeld Pettersen')
       >>> u'Bjørn Ø Fjeld Pettersen'
       >>> v == u'Bjørn Ø Fjeld Pettersen'
       True
       >>> v = forkort_navn(21, u'Bjørn Øystein', u'Ødal Pettersen')
       >>> v == u'Bjørn Ø Ø Pettersen'
       True

       >>> v = forkort_navn_u8(21, u'Bjørn Øystein'.encode('u8'), u'Ødal Pettersen'.encode('u8'))
       >>> v == u'Bjørn Ø Ø Pettersen'.encode('u8')
       True


       Normalisering av navn til utf-8 med stor forbokstav som eneste
       store bokstav.

       >>> normalize2u8(u'Bjørn') == u'Bjørn'.encode('u8')
       True
       >>> normalize2u8(u'BJørn') == u'Bjørn'.encode('u8')
       True
       >>> normalize2u8(u'BJØrn'.encode('u8')) == u'Bjørn'.encode('u8')
       True
       >>> normalize2u8(u'geir-arne') == 'Geir-Arne'
       True
    """
    import doctest
    doctest.testmod()


if __name__ == "__main__":
    test_module()
