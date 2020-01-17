from openfisca_core import periods
from openfisca_core.reforms import Reform


class income_tax_rate_editable_reform(Reform):
    name = u'Change the income tax rate according to a'


    def __init__(self, tax_benefit_system, income_tax_rate=0.16):
        self.income_tax_rate = income_tax_rate
        super(income_tax_rate_editable_reform, self).__init__(tax_benefit_system)


    def modify_income_tax_rate(self, parameters):
        reform_year = 2020
        reform_period = periods.period(reform_year)
        
        parameters.taxes.income_tax_rate.update(period = reform_period, value = self.income_tax_rate)
        return parameters


    def apply(self):
        self.modify_parameters(modifier_function = self.modify_income_tax_rate)

