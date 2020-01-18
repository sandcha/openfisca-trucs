import numpy as np
import pandas

from openfisca_core.simulation_builder import SimulationBuilder

from openfisca_country_template import CountryTaxBenefitSystem
from income_tax_rate_editable_reform import income_tax_rate_editable_reform

tax_benefit_system = CountryTaxBenefitSystem()
period = '2020-01'
salaries = np.array([1500, 2500, 3500])


simulation_builder = SimulationBuilder()
simulation_1 = simulation_builder.build_default_simulation(tax_benefit_system, count=3)
simulation_1.set_input('salary', '2020-01', salaries)

print("> current income_tax_rate", tax_benefit_system.parameters(period).taxes.income_tax_rate)
income_tax = simulation_1.calculate('income_tax', period)
print("income_tax", income_tax)


csv_data = pandas.read_csv('./income_tax_rates.csv')
for income_tax_rate in csv_data.income_tax_rate:
    print("> income_tax_rate", income_tax_rate)
    specific_legislation = income_tax_rate_editable_reform(tax_benefit_system, income_tax_rate)

    simulation_builder = SimulationBuilder()
    simulation_2 = simulation_builder.build_default_simulation(specific_legislation, count=3)
    simulation_2.set_input('salary', '2020-01', salaries)

    income_tax = simulation_2.calculate('income_tax', period)
    print("income_tax", income_tax)


