from openfisca_core.simulation_builder import SimulationBuilder
from openfisca_france import FranceTaxBenefitSystem
# from openfisca_core.model_api import ADD

tbs = FranceTaxBenefitSystem()

nombre_entites = 3
sb = SimulationBuilder()
simulation = sb.build_default_simulation(tbs, count=nombre_entites)
