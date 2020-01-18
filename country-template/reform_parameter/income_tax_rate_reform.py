from openfisca_core import periods
from openfisca_core.reforms import Reform

def modify_parameters(parameters):
    reform_period = periods.period(2020)
    parameters.taxes.income_tax_rate.update(period = reform_period, value = 0.1)
    return parameters

class income_tax_rate_reform(Reform):
    name = u'Change the income tax rate'

    def apply(self):
        self.modify_parameters(modifier_function = modify_parameters)
