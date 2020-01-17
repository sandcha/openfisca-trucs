from openfisca_core.simulation_builder import SimulationBuilder
from openfisca_france import FranceTaxBenefitSystem


tbs = FranceTaxBenefitSystem()

sb = SimulationBuilder()
simulation = sb.build_default_simulation(tbs, count=3)

period = '2020-01'
print(simulation.calculate('smic_proratise', period))
