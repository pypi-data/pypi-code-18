# -*- coding: utf-8 -*-

from __future__ import division

from numpy import int32, logical_or as or_

from openfisca_france.model.base import *  # noqa analysis:ignore

class autonomie_financiere(Variable):
    column = BoolCol
    entity = Individu
    label = u"Indicatrice d'autonomie financière vis-à-vis des prestations familiales"
    definition_period = MONTH

    def function(individu, period, legislation):
        salaire_net = individu('salaire_net', period.start.period('month', 6).offset(-6), options = [ADD])
        _P = legislation(period)

        nbh_travaillees = 169
        smic_mensuel_brut = _P.cotsoc.gen.smic_h_b * nbh_travaillees

        # Oui on compare du salaire net avec un bout du SMIC brut ...
        return salaire_net / 6 >= (_P.prestations.prestations_familiales.af.seuil_rev_taux * smic_mensuel_brut)


class prestations_familiales_enfant_a_charge(Variable):
    column = BoolCol
    entity = Individu
    label = u"Enfant considéré à charge au sens des prestations familiales"
    definition_period = MONTH

    def function(individu, period, legislation):
        est_enfant_dans_famille = individu('est_enfant_dans_famille', period)
        autonomie_financiere = individu('autonomie_financiere', period)
        age = individu('age', period)
        rempli_obligation_scolaire = individu('rempli_obligation_scolaire', period)

        pfam = legislation(period).prestations.prestations_familiales

        condition_enfant = ((age >= pfam.enfants.age_minimal) * (age < pfam.enfants.age_intermediaire) *
            rempli_obligation_scolaire)
        condition_jeune = (age >= pfam.enfants.age_intermediaire) * (age < pfam.enfants.age_limite) * not_(autonomie_financiere)

        return or_(condition_enfant, condition_jeune) * est_enfant_dans_famille


class prestations_familiales_base_ressources_individu(Variable):
    column = FloatCol
    entity = Individu
    label = u"Base ressource individuelle des prestations familiales"
    definition_period = MONTH

    def function(individu, period):
        annee_fiscale_n_2 = period.n_2

        traitements_salaires_pensions_rentes = individu('traitements_salaires_pensions_rentes', annee_fiscale_n_2)
        hsup = individu('hsup', annee_fiscale_n_2, options = [ADD])
        rpns = individu('rpns', annee_fiscale_n_2)
        glo = individu('glo', annee_fiscale_n_2)
        div = individu('div', annee_fiscale_n_2)

        return traitements_salaires_pensions_rentes + hsup + rpns + glo + div


class biactivite(Variable):
    column = BoolCol
    entity = Famille
    label = u"Indicatrice de biactivité"
    definition_period = MONTH

    def function(famille, period, legislation):
        annee_fiscale_n_2 = period.n_2

        pfam = legislation(annee_fiscale_n_2).prestations.prestations_familiales
        seuil_rev = 12 * pfam.af.bmaf

        condition_ressource = famille.members('prestations_familiales_base_ressources_individu', period) >= seuil_rev
        deux_parents = famille.nb_persons(role = famille.PARENT) == 2

        return deux_parents * famille.all(condition_ressource, role = famille.PARENT)


class div(Variable):
    column = FloatCol
    entity = Individu
    label = u"Dividendes imposés"
    definition_period = YEAR

    def function(individu, period):
        rpns_pvce = individu('rpns_pvce', period)
        rpns_pvct = individu('rpns_pvct', period)
        rpns_mvct = individu('rpns_mvct', period)
        rpns_mvlt = individu('rpns_mvlt', period)
        f3vc = individu.foyer_fiscal('f3vc', period)
        f3ve = individu.foyer_fiscal('f3ve', period)
        f3vg = individu.foyer_fiscal('f3vg', period)
        f3vh = individu.foyer_fiscal('f3vh', period)
        f3vl = individu.foyer_fiscal('f3vl', period)
        f3vm = individu.foyer_fiscal('f3vm', period)
        f3vt = individu.foyer_fiscal('f3vt', period)

        # Revenus du foyer fiscal, projetés seulement sur la première personne
        revenus_foyer_fiscal = (f3vc + f3ve + f3vg - f3vh + f3vl + f3vm + f3vt) * individu.has_role(FoyerFiscal.DECLARANT_PRINCIPAL)

        return  revenus_foyer_fiscal + rpns_pvce + rpns_pvct - rpns_mvct - rpns_mvlt


class rev_coll(Variable):
    column = FloatCol
    entity = FoyerFiscal
    label = u"Revenus perçus par le foyer fiscal à prendre en compte dans la base ressource des prestations familiales"
    definition_period = YEAR

    def function(foyer_fiscal, period):
        # Quand rev_coll est calculé sur une année glissante, retraite_titre_onereux_net et pensions_alimentaires_versees sont calculés sur l'année légale correspondante.
        retraite_titre_onereux_net = foyer_fiscal('retraite_titre_onereux_net', period.offset('first-of'))
        pensions_alimentaires_versees = foyer_fiscal('pensions_alimentaires_versees', period.offset('first-of'))
        rev_cap_lib = foyer_fiscal('rev_cap_lib', period, options = [ADD])
        rev_cat_rvcm = foyer_fiscal('rev_cat_rvcm', period)
        abat_spe = foyer_fiscal('abat_spe', period)
        fon = foyer_fiscal('fon', period)
        f7ga = foyer_fiscal('f7ga', period)
        f7gb = foyer_fiscal('f7gb', period)
        f7gc = foyer_fiscal('f7gc', period)
        rev_cat_pv = foyer_fiscal('rev_cat_pv', period)

        # TODO: ajouter les revenus de l'étranger etr*0.9
        # pensions_alimentaires_versees is negative since it is paid by the declaree
        return (retraite_titre_onereux_net + rev_cap_lib + rev_cat_rvcm + fon + pensions_alimentaires_versees - f7ga - f7gb - f7gc - abat_spe + rev_cat_pv)


class prestations_familiales_base_ressources(Variable):
    column = FloatCol
    entity = Famille
    label = u"Base ressource des prestations familiales"
    definition_period = MONTH

    def function(famille, period):
        '''
        Base ressource des prestations familiales de la famille
        'fam'
        '''
        # period_legacy = period.start.offset('first-of', 'month').period('year')
        annee_fiscale_n_2 = period.n_2

        base_ressources_i = famille.members('prestations_familiales_base_ressources_individu', period)
        enfant_i = famille.members('est_enfant_dans_famille', period)
        enfant_a_charge_i = famille.members('prestations_familiales_enfant_a_charge', period)
        ressources_i = (not_(enfant_i) + enfant_a_charge_i) * base_ressources_i
        base_ressources_i_total = famille.sum(ressources_i)

        # Revenus du foyer fiscal
        rev_coll = famille.demandeur.foyer_fiscal('rev_coll', annee_fiscale_n_2)

        base_ressources = base_ressources_i_total + rev_coll
        return base_ressources


############################################################################
# Helper functions
############################################################################


def nb_enf(famille, period, age_min, age_max):
    """
    Renvoie le nombre d'enfant au sens des allocations familiales dont l'âge est compris entre ag1 et ag2
    """

    assert period.unit == u'month'
    assert period.size == 1

    age = famille.members('age', period)
    autonomie_financiere = famille.members('autonomie_financiere', period)

#        Les allocations sont dues à compter du mois civil qui suit la naissance
#        ag1==0 ou suivant les anniversaires ag1>0.
#        Un enfant est reconnu à charge pour le versement des prestations
#        jusqu'au mois précédant son age limite supérieur (ag2 + 1) mais
#        le versement à lieu en début de mois suivant
    condition = (age >= age_min) * (age <= age_max) * not_(autonomie_financiere)

    return famille.sum(condition, role = Famille.ENFANT)
