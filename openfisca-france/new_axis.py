# This script needs
# pip install matplotlib
# pip install openfisca-france

import matplotlib.pyplot as plt

from openfisca_france import FranceTaxBenefitSystem
from openfisca_france.scenarios import init_single_entity


# Quel point de sortie pour la réduction des cotisations d’allocations familiales ?

tax_benefit_system = FranceTaxBenefitSystem()
current_period = 2021

scenario = init_single_entity(
    tax_benefit_system.new_scenario(),
    
    # Axe declaration
    axes = [[
        dict(                       #  in a dictionary
            count = 100,            # 'count' : indicates the number of step
            min = 0,
            max = 100000,
            name = 'salaire_de_base', # the variable you want to make evolve
            ),
        ]],
    
    period = current_period,
    parent1 = dict(
        date_naissance = '1980-01-01',
    )
)

simulation = scenario.new_simulation()

salaire_de_base = simulation.calculate_add('salaire_de_base', current_period)
# allegement_annuel = simulation.calculate_add("allegement_cotisation_allocations_familiales", current_period)
# print("allegement_annuel : ", allegement_annuel)
# tests : https://github.com/openfisca/openfisca-france/blob/28db1b7dff971f755047aad451f5107b7399de08/tests/formulas/allegement_cotisation_allocations_familiales.yaml

ppa = simulation.calculate_add("ppa", current_period)
print("ppa : ", ppa)

smic_proratise_annuel = simulation.calculate_add("smic_proratise", current_period)
print("smic_proratise_annuel : ", smic_proratise_annuel)

# plt.plot(salaire_de_base, allegement_annuel)
plt.plot(salaire_de_base, ppa)
plt.xlabel("Salaire de base")
# plt.ylabel("Allègement de cotisation d'allocations familiales")
plt.ylabel("PPA")

plt.axvline(x=18655.408, color="g", label="1 SMIC")
plt.axvline(x=18655.408 * 1.5, color="g", label="1.5 SMIC")
plt.axvline(x=18655.408 * 3.5, color="r", label="3.5 SMICs")
plt.legend()
plt.show()
