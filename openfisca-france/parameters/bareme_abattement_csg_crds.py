
from numpy import array, where

from openfisca_core.simulation_builder import SimulationBuilder

from openfisca_france import FranceTaxBenefitSystem



tbs = FranceTaxBenefitSystem()
period = 2022

# [i] La CSG imposable n'existe pas dans la loi :
# https://github.com/openfisca/openfisca-france/pull/2342#discussion_r1704986278

# BAREME

pss = tbs.parameters(period).prelevements_sociaux.pss.plafond_securite_sociale_mensuel

# csg_chomage = tbs.parameters(period).prelevements_sociaux.contributions_sociales.csg.remplacement.allocations_chomage
# csg_chomage_abattement = csg_chomage.imposable.abattement  # à l'assiette de CSG chômage
# abattement restructuré par https://github.com/openfisca/openfisca-france/pull/2331 (v.168.0.0)
csg_chomage_abattement = tbs.parameters(period).prelevements_sociaux.contributions_sociales.csg.activite.abattement


# BUG ? 
# print(csg_chomage_abattement) n'affiche pas le 2ème threshold.
# assert csg_chomage_abattement.thresholds[1] == 4 => IndexError: list index out of range
# 
# brackets:
# - threshold:
#     1998-01-01:
#       value: 0
#   rate:
#     1991-02-01:
#       value: 0.05
#     2005-01-01:
#       value: 0.03
#     2012-01-01:
#       value: 0.0175
# - threshold:
#     2011-01-01:
#       value: 4
#   rate:
#     2011-01-01:
#       value: null

taux_abattement_assiette_sous_4_pss = 0.0175
assert csg_chomage_abattement.rates[0] == taux_abattement_assiette_sous_4_pss

print("# 1 PSS")
assiette_avec_abattement = array([pss])
print("attendu :", taux_abattement_assiette_sous_4_pss * assiette_avec_abattement)
assiette_abattue_1_pss = csg_chomage_abattement.calc(assiette_avec_abattement)
print("obtenu :", assiette_abattue_1_pss)

print("# 4 PSS")
assiette_last_chance_abattement = array([4*pss])
print("attendu :", taux_abattement_assiette_sous_4_pss * assiette_last_chance_abattement)
assiette_abattue_4_pss = csg_chomage_abattement.calc(assiette_last_chance_abattement)
print("obtenu :", assiette_abattue_4_pss)

print("# 10 PSS")
assiette_hors_seuil_abattement = array([10*pss])
print("attendu :", (taux_abattement_assiette_sous_4_pss * 4 * pss) + (1 * 6 * pss))
assiette_abattue_10_pss = csg_chomage_abattement.calc(assiette_hors_seuil_abattement)
print("obtenu :", assiette_abattue_10_pss)
print("mais surpriiiise, le null a fait disparaître le seuil à 4 PSS", taux_abattement_assiette_sous_4_pss * 10 * pss)


calc_avec_facteur = csg_chomage_abattement.calc(
    assiette_hors_seuil_abattement,
    factor = pss,
    round_base_decimals = 2,
    )
print("et avec l'autre syntaxe ? :", calc_avec_facteur)

print("Mais est-ce l'assiette qu'il faut donner ou un nombre de PSS ?")
# le facteur est multiplié par l'array en premier argument
# src : https://github.com/openfisca/openfisca-core/blob/bee45222babbd8d9727feace04448264fdb89685/openfisca_core/taxscales/marginal_rate_tax_scale.py#L60
print("> 1 PSS")
print(csg_chomage_abattement.calc([1], factor = pss))
print("> 4 PSS")
print(csg_chomage_abattement.calc([4], factor = pss))
print("> 10 PSS")
print(csg_chomage_abattement.calc([10], factor = pss))
print("Mais ça multiplie le taux * nombre indiqué : 4 PSS  = 4 * 1.75% :-(")

print(csg_chomage_abattement.calc([1, 4]))

# !!! fausse interprétation : c'est bien barème à taux marginal sur l'assiette. 
# Il applique le rate suivant sur le delta par rapport au seuil.

# FORMULE

simulation_builder = SimulationBuilder()
simulation = simulation_builder.build_default_simulation(tbs, count=1)

simulation.set_input('salaire_de_base', '2022-01', array([1200]))
simulation.set_input('complement_are_brut', '2022-01', array([15259]))

csg = simulation.calculate_divide('csg', '2022-01')

print("CSG calculée", csg)
print("CSG attendue", 1459*0.9825*0.062)

chomage_brut = simulation.calculate('chomage_brut', '2022-01')
print("chomage_brut", chomage_brut, 259)

csg_deductible_chomage = simulation.calculate('csg_deductible_chomage', '2022-01')
print("csg_deductible_chomage", csg_deductible_chomage, 1459*0.9825*0.038)

csg_imposable_chomage = simulation.calculate('csg_imposable_chomage', '2022-01')
print("csg_imposable_chomage", csg_imposable_chomage, 1459*0.9825*0.024)

# HELPER
# from openfisca_france.model.base import not_
# from openfisca_france.model.prelevements_obligatoires.prelevements_sociaux.contributions_sociales.base import (
#     montant_csg_crds
#     )
# 
# baremes_csg = tbs.parameters(period).prelevements_sociaux.contributions_sociales.csg
# csg_taux_plein_individus = chomage_brut > 0
# montant_csg_crds_calcule = montant_csg_crds(
#     base_avec_abattement = chomage_brut,
#     indicatrice_taux_plein = csg_taux_plein_individus,
#     indicatrice_taux_reduit = not_(csg_taux_plein_individus),
#     law_node = baremes_csg.remplacement.allocations_chomage.imposable,  # le helper attend un répertoire de taux mais devrait être le taux_global
#     plafond_securite_sociale = pss  # temps plein
#     )
# print("montant_csg_crds_calcule", montant_csg_crds_calcule)


nombre_pss = chomage_brut / pss
print("nombre_pss", nombre_pss)
pallier_abattement_contributions = where(nombre_pss <= 4, 1, 4)
print("pallier_abattement_contributions", pallier_abattement_contributions)

# abattement restructuré en openfisca-france v168.0.0
# abattement = tbs.parameters(period).prelevements_sociaux.contributions_sociales.csg.remplacement.allocations_chomage.imposable.abattement.calc(pallier_abattement_contributions)
abattement = tbs.parameters(period).prelevements_sociaux.contributions_sociales.csg.activite.abattement.calc(pallier_abattement_contributions)
print("abattement", abattement)

# CRDS ?

# abattement restructuré en openfisca-france v168.0.0
# bareme_crds_activite = tbs.parameters(period).prelevements_sociaux.contributions_sociales.crds.activite.abattement
bareme_crds_activite = tbs.parameters(period).prelevements_sociaux.contributions_sociales.csg.activite.abattement

print(bareme_crds_activite.calc([1]), 1 * 0.0175)
print(bareme_crds_activite.calc([4]), 4 * 0.0175)
print(bareme_crds_activite.calc([5]), 4 * 0.0175 + 0 * 1)
print(bareme_crds_activite.calc([100]), 4 * 0.0175 + 0 * 96)

print("abattement crds 1 pss", bareme_crds_activite.calc([pss], factor = pss), 1 * pss * 0.0175)
print("abattement crds 5 pss", bareme_crds_activite.calc([5 * pss], factor = pss), 4 * pss * 0.0175 + 0 * 1 * pss)

# CSG où la 2ème tranche contient un null (pas un 0 comme la CRDS)
print("abattement csg 1 pss", csg_chomage_abattement.calc([pss], factor = pss), 1 * pss * 0.0175)
# erreur pour la csg au-delà de 4 PSS
print("abattement csg 5 pss", csg_chomage_abattement.calc([5 * pss], factor = pss), 4 * pss * 0.0175 + 0 * 1 * pss, 5 * pss * 0.0175)
