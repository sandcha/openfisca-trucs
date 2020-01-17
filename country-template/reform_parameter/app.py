import numpy as np

from openfisca_core.simulation_builder import SimulationBuilder

from openfisca_country_template import CountryTaxBenefitSystem
from income_tax_rate_reform import income_tax_rate_reform


def new_simulation(tax_benefit_system):
    simulation_builder = SimulationBuilder()
    simulation = simulation_builder.build_default_simulation(tax_benefit_system, count=3)
    simulation.set_input('salary', '2020-01', np.array([1500, 2500, 3500]))

    return simulation

period = '2020-01'

tax_benefit_system = CountryTaxBenefitSystem()

simulation_1 = new_simulation(tax_benefit_system)
print("> previous income_tax_rates", tax_benefit_system.parameters.taxes.income_tax_rate)
income_tax = simulation_1.calculate('income_tax', period)
print("income_tax", income_tax)


new_legislation = income_tax_rate_reform(tax_benefit_system)

simulation_2 = new_simulation(new_legislation)
print("> new income_tax_rates", new_legislation.parameters.taxes.income_tax_rate)
income_tax = simulation_2.calculate('income_tax', period)
print("income_tax", income_tax)
