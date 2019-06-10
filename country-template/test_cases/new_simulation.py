from openfisca_core import periods
from openfisca_core.simulation_builder import SimulationBuilder
from openfisca_country_template import CountryTaxBenefitSystem


TEST_CASE = {
    'persons': {
        'Ari': {
            'salary': {'2011-01': 1000}
        }, 
        'Paul': {}, 
        'Leila': {}, 
        'Javier': {}
    },
    'households': {
        'h1': {
            'children': ['Leila'], 
            'parents': ['Ari', 'Paul'],
            'rent': {'2011-01': 300}
        },
        'h2': {'parents': ['Javier']}
    },
}

tax_benefit_system = CountryTaxBenefitSystem()

simulation_builder = SimulationBuilder()
simulation = simulation_builder.build_from_entities(tax_benefit_system, TEST_CASE)
simulation.trace = True

housing_allowance = simulation.calculate('housing_allowance', '2011-01')
print("housing_allowance", housing_allowance)
