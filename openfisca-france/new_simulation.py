from openfisca_core.simulation_builder import SimulationBuilder
from openfisca_france import FranceTaxBenefitSystem


tbs = FranceTaxBenefitSystem()

sb = SimulationBuilder()
simulation = sb.build_default_simulation(tbs, count=3)

period = '2021-10'
smic_proratise = simulation.calculate('smic_proratise', period)
print("smic_proratise :", smic_proratise)  # 1554.6174
