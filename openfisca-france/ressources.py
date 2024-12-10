from new_simulation import simulation


# CHECK VALUES


def affiche_smic(simulation, annee, mois):
    period = str(annee) + '-' + str(mois)
    print(f"# SMIC {period}")

    smic_proratise = simulation.calculate('smic_proratise', period)
    print("smic_proratise :", smic_proratise)  

    smic_proratise_annuel = simulation.calculate_add('smic_proratise', annee)
    print("smic_proratise_annuel :", smic_proratise_annuel)  # 2021  = 1554.6174 * 12


affiche_smic(simulation, 2021, 10)  # TODO vérifier - 2021-10 = 1554.6174 noté mais 1589.5015 observé en 12.2024
affiche_smic(simulation, 2022, '04')  # 1603.1519 observé en 12.2024
# TODO openfisca : accepter 4 en int en input en le convertissant en '04' ?


# CHECK WARNINGS


def affiche_livret_epargne_populaire(simulation, annee, mois):
    period = str(annee) + '-' + str(mois)
    print(f"# LIVRET EPARGNE POPULAIRE {period}")

    livret_epargne_populaire_taux = simulation.calculate("livret_epargne_populaire_taux", period)
    print("livret_epargne_populaire_taux", livret_epargne_populaire_taux)


affiche_livret_epargne_populaire(simulation, 2022, 10)
# /Users/sch/.local/share/virtualenvs/truc-py3-11/lib/python3.11/site-packages/openfisca_france
# /model/prelevements_obligatoires/prelevements_sociaux/cotisations_sociales/travail_non_salarie.py:199:
# RuntimeWarning: divide by zero encountered in divide
#   - (0.007 * (assiette_pss > 5) * ((assiette_pss - 5) / assiette_pss))
# /Users/sch/.local/share/virtualenvs/truc-py3-11/lib/python3.11/site-packages/openfisca_france
# /model/prelevements_obligatoires/prelevements_sociaux/cotisations_sociales/travail_non_salarie.py:199:
# RuntimeWarning: invalid value encountered in multiply
#   - (0.007 * (assiette_pss > 5) * ((assiette_pss - 5) / assiette_pss))
# livret_epargne_populaire_taux [4.6 4.6 4.6]
