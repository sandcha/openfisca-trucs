# This script needs
# pip install matplotlib
# pip install seaborn==0.11.2
# pip install openfisca-france

import matplotlib.pyplot as plt
import seaborn as sns

from openfisca_france import FranceTaxBenefitSystem
from openfisca_france.scenarios import init_single_entity


# Quel point de sortie pour la réduction des cotisations d’allocations familiales ?

tax_benefit_system = FranceTaxBenefitSystem()
current_period = 2021

scenario = init_single_entity(
    tax_benefit_system.new_scenario(),
    
    # Axe declaration
    axes = [[
        dict(                      #  in a dictionary
            count = 100,           # 'count' indicates the number of steps
            min = 0,
            max = 100000,
            name = 'salaire_net',  # the variable that will evolve 'count' times between 'min' and 'max' values
            ),
        ]],
    
    period = current_period,
    parent1 = dict(
        date_naissance = '1980-01-01',
    )
)

simulation = scenario.new_simulation()

salaire_net = simulation.calculate_add('salaire_net', current_period)
ppa = simulation.calculate_add("ppa", current_period)
print("ppa : ", ppa)

sns.set_theme(style="darkgrid")
sns.lineplot(x=salaire_net, y=ppa)

plt.axvline(x=18655.408, color="y", label="1 SMIC")
plt.axvline(x=18655.408 * 1.5, color="g", label="1.5 SMIC")

plt.xlabel("Salaire net")
plt.ylabel("PPA")
plt.legend()

plt.show()
