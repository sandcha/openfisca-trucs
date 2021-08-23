# pip install matplotlib
# pip install openfisca-france

import matplotlib.pyplot as plt

from openfisca_france import FranceTaxBenefitSystem
from openfisca_france.scenarios import init_single_entity


# Quel point de sortie pour la réduction des cotisations d’allocations familiales ?

tax_benefit_system = FranceTaxBenefitSystem()

scenario = init_single_entity(
    tax_benefit_system.new_scenario(),
    
    # Axe declaration
    axes = [[
        dict(                       #  in a dictionary
            count = 100,            # 'count' : indicates the number of step
            min = 0,
            max = 100000,
            name = 'salaire_net', # the variable you want to make evolve
            ),
        ]],
    
    period = 2021,
    parent1 = dict(
        date_naissance = '1980-01-01',
    )
)

simulation = scenario.new_simulation()

salaire_net = simulation.calculate_add('salaire_net', 2021)
allegement_annuel = simulation.calculate_add("allegement_cotisation_allocations_familiales", 2021)
print(allegement_annuel)

plt.plot(salaire_net, allegement_annuel)
plt.xlabel("Salaire net")
plt.ylabel("Allègement de cotisation d'allocations familiales")
plt.show()
