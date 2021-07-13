import numpy

from openfisca_core.simulation_builder import SimulationBuilder
from openfisca_country_template import CountryTaxBenefitSystem


tax_benefit_system = CountryTaxBenefitSystem()

# see parameters
print("All CountryTaxBenefitSystem parameters:")
print(tax_benefit_system.parameters)
print("-------")

# parameters and periods
print("One parameter named benefits.housing_allowance:")
print(tax_benefit_system.parameters.benefits.housing_allowance)
print("And what is benefits.housing_allowance value in 2015?")
print(tax_benefit_system.parameters(2015).benefits.housing_allowance)
print("-------")

# parameters in simulation
nb_persons = 3
simulation_builder = SimulationBuilder()
simulation = simulation_builder.build_default_simulation(tax_benefit_system, count=nb_persons)

# before december 2016, the housing allowance amonts are > 0 when the rent is > 0
simulation.set_input("rent", "2011-01", numpy.array([0, 500, 1000]))  # 3 rents for 3 persons
housing_allowance = simulation.calculate("housing_allowance", "2011-01")
print("housing_allowance for active benefits.housing_allowance", housing_allowance)

# from # before december 2016, the housing allowance amonts are 0
housing_allowance_ended_parameter = simulation.calculate("housing_allowance", "2016-12")
print("housing_allowance_ended_parameter", housing_allowance_ended_parameter)
