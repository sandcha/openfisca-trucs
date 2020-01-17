from copy import deepcopy
import pprint

from openfisca_france import FranceTaxBenefitSystem
from tests.test_entities import TEST_CASE_AGES


tbs = FranceTaxBenefitSystem()
period = '2020'

test_case = deepcopy(TEST_CASE_AGES)
test_case['period'] = period
# pprint.pprint(test_case)
simulation = tbs.new_scenario().init_from_dict(test_case).new_simulation()
print(simulation.calculate('revenu_disponible', period))
