import pandas
import numpy as numpy

from openfisca_core.simulation_builder import SimulationBuilder    
from openfisca_country_template import CountryTaxBenefitSystem

tax_benefit_system = CountryTaxBenefitSystem()

# READ DATA

data_persons = pandas.read_csv('./data_persons.csv')
data_households = pandas.read_csv('./data_households.csv')

# SIMULATION BUILDER

sb = SimulationBuilder()
sb.create_entities(tax_benefit_system)

persons_ids = data_persons.person_id
sb.declare_person_entity('person', persons_ids)

# Instanciate the household entity:
households_ids = data_households.household_id
household_instance = sb.declare_entity('household', households_ids)
    
# Join households data on persons:
persons_households = data_persons.household_id
persons_households_roles = data_persons.person_role_in_household
sb.join_with_persons(household_instance, persons_households, persons_households_roles)

# SIMULATION

simulation = sb.build(tax_benefit_system)

period = '2019-03'
simulation.set_input('salary', period, data_persons.person_salary)

total_taxes = simulation.calculate('total_taxes', period)
print("total_taxes", total_taxes)
