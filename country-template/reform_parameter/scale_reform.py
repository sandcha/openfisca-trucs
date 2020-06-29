import os
from openfisca_core import periods
from openfisca_core.reforms import Reform
from openfisca_core.parameters import load_parameter_file


dir_path = os.path.dirname(__file__)


def modify_scale(parameters):
    file_path = os.path.join(dir_path, 'new_scale.yaml')  # x10 on rates
    reform_parameters_subtree = load_parameter_file(file_path, name='new_scale')
    reform_period = periods.period(2020)

    # Access the wanted parameter node
    parameters.taxes.children["social_security_contribution"] = reform_parameters_subtree
    # parameters.taxes.add_child("new_social_security_contribution", reform_parameters_subtree)
    return parameters


class social_security_contribution_reform(Reform):
    name = u'Change the social security contribution marginal rate scale with another'

    def apply(self):
        self.modify_parameters(modifier_function = modify_scale)
