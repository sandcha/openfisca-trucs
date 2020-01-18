import numpy as np

from openfisca_core.simulation_builder import SimulationBuilder

from openfisca_country_template import CountryTaxBenefitSystem
from income_tax_rate_editable_reform import income_tax_rate_editable_reform


def new_simulation(tax_benefit_system):
    simulation_builder = SimulationBuilder()
    simulation = simulation_builder.build_default_simulation(tax_benefit_system, count=3)
    simulation.set_input('salary', '2020-01', np.array([1500, 2500, 3500]))

    return simulation

tax_benefit_system = CountryTaxBenefitSystem()
period = '2020-01'

simulation_1 = new_simulation(tax_benefit_system)
print("> previous income_tax_rates", tax_benefit_system.parameters.taxes.income_tax_rate)
income_tax = simulation_1.calculate('income_tax', period)
print("income_tax", income_tax)

for i in range(1, 5):
    income_tax_rate = i/10
    print("income_tax_rate", income_tax_rate)
    specific_legislation = income_tax_rate_editable_reform(tax_benefit_system, income_tax_rate)

    simulation_3 = new_simulation(specific_legislation)
    print("> new income_tax_rates", specific_legislation.parameters.taxes.income_tax_rate)
    income_tax = simulation_3.calculate('income_tax', period)
    print("income_tax", income_tax)
