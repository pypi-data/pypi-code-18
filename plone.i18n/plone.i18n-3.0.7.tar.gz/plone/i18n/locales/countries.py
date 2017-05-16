# -*- coding: UTF-8 -*-

from plone.i18n.locales.interfaces import ICountryAvailability
from zope.interface import implementer


@implementer(ICountryAvailability)
class CountryAvailability(object):
    """A list of available coutries.
    """

    def getAvailableCountries(self):
        """Return a sequence of country tags for available countries.
        """
        return _countrylist.keys()

    def getCountries(self):
        """Return a sequence of Country objects for available countries.
        """
        return _countrylist.copy()

    def getCountryListing(self):
        """Return a sequence of country code and country name tuples.
        """
        return [(code, _countrylist[code][u'name']) for code in _countrylist]

countries = CountryAvailability()

# This is a dictionary of dictonaries:
#
# 'country-code' : {u'name' : 'English name', u'flag' : u'/++resource++country-flags/*.gif'}
#
# This list follows ISO 3166-1. In addition the following reservations are
# part of the list for historical reasons: an

_countrylist = {
u'ad' : {u'name' : 'Andorra', u'flag' : u'/++resource++country-flags/ad.gif'},
u'ae' : {u'name' : 'United Arab Emirates', u'flag' : u'/++resource++country-flags/ae.gif'},
u'af' : {u'name' : 'Afghanistan', u'flag' : u'/++resource++country-flags/af.gif'},
u'ag' : {u'name' : 'Antigua and Barbuda', u'flag' : u'/++resource++country-flags/ag.gif'},
u'ai' : {u'name' : 'Anguilla', u'flag' : u'/++resource++country-flags/ai.gif'},
u'al' : {u'name' : 'Albania', u'flag' : u'/++resource++country-flags/al.gif'},
u'am' : {u'name' : 'Armenia', u'flag' : u'/++resource++country-flags/am.gif'},
u'an' : {u'name' : 'Netherlands Antilles', u'flag' : u'/++resource++country-flags/an.gif'},
u'ao' : {u'name' : 'Angola', u'flag' : u'/++resource++country-flags/ao.gif'},
u'aq' : {u'name' : 'Antarctica', u'flag' : u'/++resource++country-flags/aq.gif'},
u'ar' : {u'name' : 'Argentina', u'flag' : u'/++resource++country-flags/ar.gif'},
u'as' : {u'name' : 'American Samoa', u'flag' : u'/++resource++country-flags/as.gif'},
u'at' : {u'name' : 'Austria', u'flag' : u'/++resource++country-flags/at.gif'},
u'au' : {u'name' : 'Australia', u'flag' : u'/++resource++country-flags/au.gif'},
u'aw' : {u'name' : 'Aruba', u'flag' : u'/++resource++country-flags/aw.gif'},
u'ax' : {u'name' : 'Oland Islands', u'flag' : u'/++resource++country-flags/ax.gif'},
u'az' : {u'name' : 'Azerbaijan', u'flag' : u'/++resource++country-flags/az.gif'},
u'ba' : {u'name' : 'Bosnia and Herzegovina', u'flag' : u'/++resource++country-flags/ba.gif'},
u'bb' : {u'name' : 'Barbados', u'flag' : u'/++resource++country-flags/bb.gif'},
u'bd' : {u'name' : 'Bangladesh', u'flag' : u'/++resource++country-flags/bd.gif'},
u'be' : {u'name' : 'Belgium', u'flag' : u'/++resource++country-flags/be.gif'},
u'bf' : {u'name' : 'Burkina Faso', u'flag' : u'/++resource++country-flags/bf.gif'},
u'bg' : {u'name' : 'Bulgaria', u'flag' : u'/++resource++country-flags/bg.gif'},
u'bh' : {u'name' : 'Bahrain', u'flag' : u'/++resource++country-flags/bh.gif'},
u'bi' : {u'name' : 'Burundi', u'flag' : u'/++resource++country-flags/bi.gif'},
u'bj' : {u'name' : 'Benin', u'flag' : u'/++resource++country-flags/bj.gif'},
u'bl' : {u'name' : 'Saint Barthélemy', u'flag' : u'/++resource++country-flags/bl.gif'},
u'bm' : {u'name' : 'Bermuda', u'flag' : u'/++resource++country-flags/bm.gif'},
u'bn' : {u'name' : 'Brunei Darussalam', u'flag' : u'/++resource++country-flags/bn.gif'},
u'bo' : {u'name' : 'Bolivia', u'flag' : u'/++resource++country-flags/bo.gif'},
u'bq' : {u'name' : 'Bonaire, Sint Eustatius and Saba', u'flag' : u'/++resource++country-flags/bq.gif'},
u'br' : {u'name' : 'Brazil', u'flag' : u'/++resource++country-flags/br.gif'},
u'bs' : {u'name' : 'Bahamas', u'flag' : u'/++resource++country-flags/bs.gif'},
u'bt' : {u'name' : 'Bhutan', u'flag' : u'/++resource++country-flags/bt.gif'},
u'bv' : {u'name' : 'Bouvet Island', u'flag' : u'/++resource++country-flags/bv.gif'},
u'bw' : {u'name' : 'Botswana', u'flag' : u'/++resource++country-flags/bw.gif'},
u'by' : {u'name' : 'Belarus', u'flag' : u'/++resource++country-flags/by.gif'},
u'bz' : {u'name' : 'Belize', u'flag' : u'/++resource++country-flags/bz.gif'},
u'ca' : {u'name' : 'Canada', u'flag' : u'/++resource++country-flags/ca.gif'},
u'cc' : {u'name' : 'Cocos (Keeling) Islands', u'flag' : u'/++resource++country-flags/cc.gif'},
u'cd' : {u'name' : 'Congo The Democratic Republic of', u'flag' : u'/++resource++country-flags/cd.gif'},
u'cf' : {u'name' : 'Central African Republic', u'flag' : u'/++resource++country-flags/cf.gif'},
u'cg' : {u'name' : 'Congo', u'flag' : u'/++resource++country-flags/cg.gif'},
u'ch' : {u'name' : 'Switzerland', u'flag' : u'/++resource++country-flags/ch.gif'},
u'ci' : {u'name' : "Cote d'Ivoire", u'flag' : u'/++resource++country-flags/ci.gif'},
u'ck' : {u'name' : 'Cook Islands', u'flag' : u'/++resource++country-flags/ck.gif'},
u'cl' : {u'name' : 'Chile', u'flag' : u'/++resource++country-flags/cl.gif'},
u'cm' : {u'name' : 'Cameroon', u'flag' : u'/++resource++country-flags/cm.gif'},
u'cn' : {u'name' : 'China', u'flag' : u'/++resource++country-flags/cn.gif'},
u'co' : {u'name' : 'Colombia', u'flag' : u'/++resource++country-flags/co.gif'},
u'cr' : {u'name' : 'Costa Rica', u'flag' : u'/++resource++country-flags/cr.gif'},
u'cs' : {u'name' : 'Serbia and Montenegro', u'flag' : u'/++resource++country-flags/cs.gif'},
u'cu' : {u'name' : 'Cuba', u'flag' : u'/++resource++country-flags/cu.gif'},
u'cv' : {u'name' : 'Cape Verde', u'flag' : u'/++resource++country-flags/cv.gif'},
u'cw' : {u'name' : 'Curaçao', u'flag' : u'/++resource++country-flags/cw.png'},
u'cx' : {u'name' : 'Christmas Island', u'flag' : u'/++resource++country-flags/cx.gif'},
u'cy' : {u'name' : 'Cyprus', u'flag' : u'/++resource++country-flags/cy.gif'},
u'cz' : {u'name' : 'Czech Republic', u'flag' : u'/++resource++country-flags/cz.gif'},
u'de' : {u'name' : 'Germany', u'flag' : u'/++resource++country-flags/de.gif'},
u'dj' : {u'name' : 'Djibouti', u'flag' : u'/++resource++country-flags/dj.gif'},
u'dk' : {u'name' : 'Denmark', u'flag' : u'/++resource++country-flags/dk.gif'},
u'dm' : {u'name' : 'Dominica', u'flag' : u'/++resource++country-flags/dm.gif'},
u'do' : {u'name' : 'Dominican Republic', u'flag' : u'/++resource++country-flags/do.gif'},
u'dz' : {u'name' : 'Algeria', u'flag' : u'/++resource++country-flags/dz.gif'},
u'ec' : {u'name' : 'Ecuador', u'flag' : u'/++resource++country-flags/ec.gif'},
u'ee' : {u'name' : 'Estonia', u'flag' : u'/++resource++country-flags/ee.gif'},
u'eg' : {u'name' : 'Egypt', u'flag' : u'/++resource++country-flags/eg.gif'},
u'eh' : {u'name' : 'Western Sahara', u'flag' : u'/++resource++country-flags/eh.gif'},
u'er' : {u'name' : 'Eritrea', u'flag' : u'/++resource++country-flags/er.gif'},
u'es' : {u'name' : 'Spain', u'flag' : u'/++resource++country-flags/es.gif'},
u'et' : {u'name' : 'Ethiopia', u'flag' : u'/++resource++country-flags/et.gif'},
u'fi' : {u'name' : 'Finland', u'flag' : u'/++resource++country-flags/fi.gif'},
u'fj' : {u'name' : 'Fiji', u'flag' : u'/++resource++country-flags/fj.gif'},
u'fk' : {u'name' : 'Falkland Islands (Malvinas)', u'flag' : u'/++resource++country-flags/fk.gif'},
u'fm' : {u'name' : 'Micronesia Federated States of', u'flag' : u'/++resource++country-flags/fm.gif'},
u'fo' : {u'name' : 'Faroe Islands', u'flag' : u'/++resource++country-flags/fo.gif'},
u'fr' : {u'name' : 'France', u'flag' : u'/++resource++country-flags/fr.gif'},
u'ga' : {u'name' : 'Gabon', u'flag' : u'/++resource++country-flags/ga.gif'},
u'gb' : {u'name' : 'United Kingdom', u'flag' : u'/++resource++country-flags/gb.gif'},
u'gd' : {u'name' : 'Grenada', u'flag' : u'/++resource++country-flags/gd.gif'},
u'ge' : {u'name' : 'Georgia', u'flag' : u'/++resource++country-flags/ge.gif'},
u'gf' : {u'name' : 'French Guiana', u'flag' : u'/++resource++country-flags/gf.gif'},
u'gg' : {u'name' : 'Guernsey', u'flag' : u'/++resource++country-flags/gg.gif'},
u'gh' : {u'name' : 'Ghana', u'flag' : u'/++resource++country-flags/gh.gif'},
u'gi' : {u'name' : 'Gibraltar', u'flag' : u'/++resource++country-flags/gi.gif'},
u'gl' : {u'name' : 'Greenland', u'flag' : u'/++resource++country-flags/gl.gif'},
u'gm' : {u'name' : 'Gambia', u'flag' : u'/++resource++country-flags/gm.gif'},
u'gn' : {u'name' : 'Guinea', u'flag' : u'/++resource++country-flags/gn.gif'},
u'gp' : {u'name' : 'Guadeloupe', u'flag' : u'/++resource++country-flags/gp.gif'},
u'gq' : {u'name' : 'Equatorial Guinea', u'flag' : u'/++resource++country-flags/gq.gif'},
u'gr' : {u'name' : 'Greece', u'flag' : u'/++resource++country-flags/gr.gif'},
u'gs' : {u'name' : 'South Georgia and the South Sandwich Islands', u'flag' : u'/++resource++country-flags/gs.gif'},
u'gt' : {u'name' : 'Guatemala', u'flag' : u'/++resource++country-flags/gt.gif'},
u'gu' : {u'name' : 'Guam', u'flag' : u'/++resource++country-flags/gu.gif'},
u'gw' : {u'name' : 'Guinea-Bissau', u'flag' : u'/++resource++country-flags/gw.gif'},
u'gy' : {u'name' : 'Guyana', u'flag' : u'/++resource++country-flags/gy.gif'},
u'hk' : {u'name' : 'Hong Kong', u'flag' : u'/++resource++country-flags/hk.gif'},
u'hm' : {u'name' : 'Heard Island and McDonald Islands', u'flag' : u'/++resource++country-flags/hm.gif'},
u'hn' : {u'name' : 'Honduras', u'flag' : u'/++resource++country-flags/hn.gif'},
u'hr' : {u'name' : 'Croatia', u'flag' : u'/++resource++country-flags/hr.gif'},
u'ht' : {u'name' : 'Haiti', u'flag' : u'/++resource++country-flags/ht.gif'},
u'hu' : {u'name' : 'Hungary', u'flag' : u'/++resource++country-flags/hu.gif'},
u'id' : {u'name' : 'Indonesia', u'flag' : u'/++resource++country-flags/id.gif'},
u'ie' : {u'name' : 'Ireland', u'flag' : u'/++resource++country-flags/ie.gif'},
u'il' : {u'name' : 'Israel', u'flag' : u'/++resource++country-flags/il.gif'},
u'im' : {u'name' : 'Isle of Man', u'flag' : u'/++resource++country-flags/im.gif'},
u'in' : {u'name' : 'India', u'flag' : u'/++resource++country-flags/in.gif'},
u'io' : {u'name' : 'British Indian Ocean Territory', u'flag' : u'/++resource++country-flags/io.gif'},
u'iq' : {u'name' : 'Iraq', u'flag' : u'/++resource++country-flags/iq.gif'},
u'ir' : {u'name' : 'Iran Islamic Republic of', u'flag' : u'/++resource++country-flags/ir.gif'},
u'is' : {u'name' : 'Iceland', u'flag' : u'/++resource++country-flags/is.gif'},
u'it' : {u'name' : 'Italy', u'flag' : u'/++resource++country-flags/it.gif'},
u'je' : {u'name' : 'Jersey', u'flag' : u'/++resource++country-flags/je.gif'},
u'jm' : {u'name' : 'Jamaica', u'flag' : u'/++resource++country-flags/jm.gif'},
u'jo' : {u'name' : 'Jordan', u'flag' : u'/++resource++country-flags/jo.gif'},
u'jp' : {u'name' : 'Japan', u'flag' : u'/++resource++country-flags/jp.gif'},
u'ke' : {u'name' : 'Kenya', u'flag' : u'/++resource++country-flags/ke.gif'},
u'kg' : {u'name' : 'Kyrgyzstan', u'flag' : u'/++resource++country-flags/kg.gif'},
u'kh' : {u'name' : 'Cambodia', u'flag' : u'/++resource++country-flags/kh.gif'},
u'ki' : {u'name' : 'Kiribati', u'flag' : u'/++resource++country-flags/ki.gif'},
u'km' : {u'name' : 'Comoros', u'flag' : u'/++resource++country-flags/km.gif'},
u'kn' : {u'name' : 'Saint Kitts and Nevis', u'flag' : u'/++resource++country-flags/kn.gif'},
u'kp' : {u'name' : "Korea Democratic People's Republic of", u'flag' : u'/++resource++country-flags/kp.gif'},
u'kr' : {u'name' : 'Korea Republic of', u'flag' : u'/++resource++country-flags/kr.gif'},
u'kw' : {u'name' : 'Kuwait', u'flag' : u'/++resource++country-flags/kw.gif'},
u'ky' : {u'name' : 'Cayman Islands', u'flag' : u'/++resource++country-flags/ky.gif'},
u'kz' : {u'name' : 'Kazakhstan', u'flag' : u'/++resource++country-flags/kz.gif'},
u'la' : {u'name' : "Lao People's Democratic Republic", u'flag' : u'/++resource++country-flags/la.gif'},
u'lb' : {u'name' : 'Lebanon', u'flag' : u'/++resource++country-flags/lb.gif'},
u'lc' : {u'name' : 'Saint Lucia', u'flag' : u'/++resource++country-flags/lc.gif'},
u'li' : {u'name' : 'Liechtenstein', u'flag' : u'/++resource++country-flags/li.gif'},
u'lk' : {u'name' : 'Sri Lanka', u'flag' : u'/++resource++country-flags/lk.gif'},
u'lr' : {u'name' : 'Liberia', u'flag' : u'/++resource++country-flags/lr.gif'},
u'ls' : {u'name' : 'Lesotho', u'flag' : u'/++resource++country-flags/ls.gif'},
u'lt' : {u'name' : 'Lithuania', u'flag' : u'/++resource++country-flags/lt.gif'},
u'lu' : {u'name' : 'Luxembourg', u'flag' : u'/++resource++country-flags/lu.gif'},
u'lv' : {u'name' : 'Latvia', u'flag' : u'/++resource++country-flags/lv.gif'},
u'ly' : {u'name' : 'Libyan Arab Jamahiriya', u'flag' : u'/++resource++country-flags/ly.gif'},
u'ma' : {u'name' : 'Morocco', u'flag' : u'/++resource++country-flags/ma.gif'},
u'mc' : {u'name' : 'Monaco', u'flag' : u'/++resource++country-flags/mc.gif'},
u'md' : {u'name' : 'Moldova Republic of', u'flag' : u'/++resource++country-flags/md.gif'},
u'me' : {u'name' : 'Montenegro', u'flag' : u'/++resource++country-flags/me.gif'},
u'mf' : {u'name' : 'Saint Martin (French part)', u'flag' : u'/++resource++country-flags/mf.png'},
u'mg' : {u'name' : 'Madagascar', u'flag' : u'/++resource++country-flags/mg.gif'},
u'mh' : {u'name' : 'Marshall Islands', u'flag' : u'/++resource++country-flags/mh.gif'},
u'mk' : {u'name' : 'Macedonia the former Yugoslavian Republic of', u'flag' : u'/++resource++country-flags/mk.gif'},
u'ml' : {u'name' : 'Mali', u'flag' : u'/++resource++country-flags/ml.gif'},
u'mm' : {u'name' : 'Myanmar', u'flag' : u'/++resource++country-flags/mm.gif'},
u'mn' : {u'name' : 'Mongolia', u'flag' : u'/++resource++country-flags/mn.gif'},
u'mo' : {u'name' : 'Macao', u'flag' : u'/++resource++country-flags/mo.gif'},
u'mp' : {u'name' : 'Northern Mariana Islands', u'flag' : u'/++resource++country-flags/mp.gif'},
u'mq' : {u'name' : 'Martinique', u'flag' : u'/++resource++country-flags/mq.gif'},
u'mr' : {u'name' : 'Mauritania', u'flag' : u'/++resource++country-flags/mr.gif'},
u'ms' : {u'name' : 'Montserrat', u'flag' : u'/++resource++country-flags/ms.gif'},
u'mt' : {u'name' : 'Malta', u'flag' : u'/++resource++country-flags/mt.gif'},
u'mu' : {u'name' : 'Mauritius', u'flag' : u'/++resource++country-flags/mu.gif'},
u'mv' : {u'name' : 'Maldives', u'flag' : u'/++resource++country-flags/mv.gif'},
u'mw' : {u'name' : 'Malawi', u'flag' : u'/++resource++country-flags/mw.gif'},
u'mx' : {u'name' : 'Mexico', u'flag' : u'/++resource++country-flags/mx.gif'},
u'my' : {u'name' : 'Malaysia', u'flag' : u'/++resource++country-flags/my.gif'},
u'mz' : {u'name' : 'Mozambique', u'flag' : u'/++resource++country-flags/mz.gif'},
u'na' : {u'name' : 'Namibia', u'flag' : u'/++resource++country-flags/na.gif'},
u'nc' : {u'name' : 'New Caledonia', u'flag' : u'/++resource++country-flags/nc.gif'},
u'ne' : {u'name' : 'Niger', u'flag' : u'/++resource++country-flags/ne.gif'},
u'nf' : {u'name' : 'Norfolk Island', u'flag' : u'/++resource++country-flags/nf.gif'},
u'ng' : {u'name' : 'Nigeria', u'flag' : u'/++resource++country-flags/ng.gif'},
u'ni' : {u'name' : 'Nicaragua', u'flag' : u'/++resource++country-flags/ni.gif'},
u'nl' : {u'name' : 'Netherlands', u'flag' : u'/++resource++country-flags/nl.gif'},
u'no' : {u'name' : 'Norway', u'flag' : u'/++resource++country-flags/no.gif'},
u'np' : {u'name' : 'Nepal', u'flag' : u'/++resource++country-flags/np.gif'},
u'nr' : {u'name' : 'Nauru', u'flag' : u'/++resource++country-flags/nr.gif'},
u'nu' : {u'name' : 'Niue', u'flag' : u'/++resource++country-flags/nu.gif'},
u'nz' : {u'name' : 'New Zealand', u'flag' : u'/++resource++country-flags/nz.gif'},
u'om' : {u'name' : 'Oman', u'flag' : u'/++resource++country-flags/om.gif'},
u'pa' : {u'name' : 'Panama', u'flag' : u'/++resource++country-flags/pa.gif'},
u'pe' : {u'name' : 'Peru', u'flag' : u'/++resource++country-flags/pe.gif'},
u'pf' : {u'name' : 'French Polynesia', u'flag' : u'/++resource++country-flags/pf.gif'},
u'pg' : {u'name' : 'Papua New Guinea', u'flag' : u'/++resource++country-flags/pg.gif'},
u'ph' : {u'name' : 'Philippines', u'flag' : u'/++resource++country-flags/ph.gif'},
u'pk' : {u'name' : 'Pakistan', u'flag' : u'/++resource++country-flags/pk.gif'},
u'pl' : {u'name' : 'Poland', u'flag' : u'/++resource++country-flags/pl.gif'},
u'pm' : {u'name' : 'Saint Pierre and Miquelon', u'flag' : u'/++resource++country-flags/pm.gif'},
u'pn' : {u'name' : 'Pitcairn', u'flag' : u'/++resource++country-flags/pn.gif'},
u'pr' : {u'name' : 'Puerto Rico', u'flag' : u'/++resource++country-flags/pr.gif'},
u'ps' : {u'name' : 'Palestinian Territory occupied', u'flag' : u'/++resource++country-flags/ps.gif'},
u'pt' : {u'name' : 'Portugal', u'flag' : u'/++resource++country-flags/pt.gif'},
u'pw' : {u'name' : 'Palau', u'flag' : u'/++resource++country-flags/pw.gif'},
u'py' : {u'name' : 'Paraguay', u'flag' : u'/++resource++country-flags/py.gif'},
u'qa' : {u'name' : 'Qatar', u'flag' : u'/++resource++country-flags/qa.gif'},
u're' : {u'name' : 'Reunion', u'flag' : u'/++resource++country-flags/re.gif'},
u'ro' : {u'name' : 'Romania', u'flag' : u'/++resource++country-flags/ro.gif'},
u'rs' : {u'name' : 'Serbia', u'flag' : u'/++resource++country-flags/rs.gif'},
u'ru' : {u'name' : 'Russian Federation', u'flag' : u'/++resource++country-flags/ru.gif'},
u'rw' : {u'name' : 'Rwanda', u'flag' : u'/++resource++country-flags/rw.gif'},
u'sa' : {u'name' : 'Saudi Arabia', u'flag' : u'/++resource++country-flags/sa.gif'},
u'sb' : {u'name' : 'Solomon Islands', u'flag' : u'/++resource++country-flags/sb.gif'},
u'sc' : {u'name' : 'Seychelles', u'flag' : u'/++resource++country-flags/sc.gif'},
u'sd' : {u'name' : 'Sudan', u'flag' : u'/++resource++country-flags/sd.gif'},
u'se' : {u'name' : 'Sweden', u'flag' : u'/++resource++country-flags/se.gif'},
u'sg' : {u'name' : 'Singapore', u'flag' : u'/++resource++country-flags/sg.gif'},
u'sh' : {u'name' : 'Saint Helena', u'flag' : u'/++resource++country-flags/sh.gif'},
u'si' : {u'name' : 'Slovenia', u'flag' : u'/++resource++country-flags/si.gif'},
u'sj' : {u'name' : 'Svalbard and Jan Mayen', u'flag' : u'/++resource++country-flags/sj.gif'},
u'sk' : {u'name' : 'Slovakia', u'flag' : u'/++resource++country-flags/sk.gif'},
u'sl' : {u'name' : 'Sierra Leone', u'flag' : u'/++resource++country-flags/sl.gif'},
u'sm' : {u'name' : 'San Marino', u'flag' : u'/++resource++country-flags/sm.gif'},
u'sn' : {u'name' : 'Senegal', u'flag' : u'/++resource++country-flags/sn.gif'},
u'so' : {u'name' : 'Somalia', u'flag' : u'/++resource++country-flags/so.gif'},
u'sr' : {u'name' : 'Suriname', u'flag' : u'/++resource++country-flags/sr.gif'},
u'ss' : {u'name' : 'South Sudan', u'flag' : u'/++resource++country-flags/ss.png'},
u'st' : {u'name' : 'Sao Tome and Principe', u'flag' : u'/++resource++country-flags/st.gif'},
u'sv' : {u'name' : 'El Salvador', u'flag' : u'/++resource++country-flags/sv.gif'},
u'sx' : {u'name' : 'Sint Maarten (Dutch part)', u'flag' : u'/++resource++country-flags/sx.png'},
u'sy' : {u'name' : 'Syrian Arab Republic', u'flag' : u'/++resource++country-flags/sy.gif'},
u'sz' : {u'name' : 'Swaziland', u'flag' : u'/++resource++country-flags/sz.gif'},
u'tc' : {u'name' : 'Turks and Caicos Islands', u'flag' : u'/++resource++country-flags/tc.gif'},
u'td' : {u'name' : 'Chad', u'flag' : u'/++resource++country-flags/td.gif'},
u'tf' : {u'name' : 'French Southern Territories', u'flag' : u'/++resource++country-flags/tf.gif'},
u'tg' : {u'name' : 'Togo', u'flag' : u'/++resource++country-flags/tg.gif'},
u'th' : {u'name' : 'Thailand', u'flag' : u'/++resource++country-flags/th.gif'},
u'tj' : {u'name' : 'Tajikistan', u'flag' : u'/++resource++country-flags/tj.gif'},
u'tk' : {u'name' : 'Tokelau', u'flag' : u'/++resource++country-flags/tk.gif'},
u'tl' : {u'name' : 'Timor-Leste', u'flag' : u'/++resource++country-flags/tl.gif'},
u'tm' : {u'name' : 'Turkmenistan', u'flag' : u'/++resource++country-flags/tm.gif'},
u'tn' : {u'name' : 'Tunisia', u'flag' : u'/++resource++country-flags/tn.gif'},
u'to' : {u'name' : 'Tonga', u'flag' : u'/++resource++country-flags/to.gif'},
u'tr' : {u'name' : 'Turkey', u'flag' : u'/++resource++country-flags/tr.gif'},
u'tt' : {u'name' : 'Trinidad and Tobago', u'flag' : u'/++resource++country-flags/tt.gif'},
u'tv' : {u'name' : 'Tuvalu', u'flag' : u'/++resource++country-flags/tv.gif'},
u'tw' : {u'name' : 'Taiwan', u'flag' : u'/++resource++country-flags/tw.gif'},
u'tz' : {u'name' : 'Tanzania United Republic of', u'flag' : u'/++resource++country-flags/tz.gif'},
u'ua' : {u'name' : 'Ukraine', u'flag' : u'/++resource++country-flags/ua.gif'},
u'ug' : {u'name' : 'Uganda', u'flag' : u'/++resource++country-flags/ug.gif'},
u'um' : {u'name' : 'United States Minor Outlying Islands', u'flag' : u'/++resource++country-flags/um.gif'},
u'us' : {u'name' : 'United States', u'flag' : u'/++resource++country-flags/us.gif'},
u'uy' : {u'name' : 'Uruguay', u'flag' : u'/++resource++country-flags/uy.gif'},
u'uz' : {u'name' : 'Uzbekistan', u'flag' : u'/++resource++country-flags/uz.gif'},
u'va' : {u'name' : 'Holy See (Vatican City State)', u'flag' : u'/++resource++country-flags/va.gif'},
u'vc' : {u'name' : 'Saint Vincent and the Grenadines', u'flag' : u'/++resource++country-flags/vc.gif'},
u've' : {u'name' : 'Venezuela', u'flag' : u'/++resource++country-flags/ve.gif'},
u'vg' : {u'name' : 'Virgin Islands British', u'flag' : u'/++resource++country-flags/vg.gif'},
u'vi' : {u'name' : 'Virgin Islands U.S.', u'flag' : u'/++resource++country-flags/vi.gif'},
u'vn' : {u'name' : 'Viet Nam', u'flag' : u'/++resource++country-flags/vn.gif'},
u'vu' : {u'name' : 'Vanuatu', u'flag' : u'/++resource++country-flags/vu.gif'},
u'wf' : {u'name' : 'Wallis and Futuna', u'flag' : u'/++resource++country-flags/wf.gif'},
u'ws' : {u'name' : 'Samoa', u'flag' : u'/++resource++country-flags/ws.gif'},
u'ye' : {u'name' : 'Yemen', u'flag' : u'/++resource++country-flags/ye.gif'},
u'yt' : {u'name' : 'Mayotte', u'flag' : u'/++resource++country-flags/yt.gif'},
u'za' : {u'name' : 'South Africa', u'flag' : u'/++resource++country-flags/za.gif'},
u'zm' : {u'name' : 'Zambia', u'flag' : u'/++resource++country-flags/zm.gif'},
u'zw' : {u'name' : 'Zimbabwe', u'flag' : u'/++resource++country-flags/zw.gif'},
u'xk' : {u'name' : 'Kosovo', u'flag' : u'/++resource++country-flags/xk.gif'},
}

# convert the utf-8 encoded values to unicode
for code in _countrylist:
    value = _countrylist[code]
    if u'name' in value:
        value[u'name'] = unicode(value[u'name'], 'utf-8')
