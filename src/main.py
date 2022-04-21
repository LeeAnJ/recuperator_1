from cfrhex.cfrhex import CfRHex2Flows
from fluid_class import (RP10Fluid)

# input fluid's data
butane = RP10Fluid(("butane",))
rhex = CfRHex2Flows(eps=1.0, dt=10.0)

flow_hot = [None, None]
flow_hot[0] = butane
flow_hot[1] = {
                'm': {'value': 1.0, 'units': 'kgs'},
                't_in': {'value': 28, 'units': 'c'},
                'p_in': {'value': 10.0, 'units': 'bar'},
                'dp_friction': {'value': 0.0, 'units': 'bar'}
               }

flow_cold = [None, None]
flow_cold[0] = butane
flow_cold[1] = {
                'm': {'value': 1.0, 'units': 'kgs'},
                't_in': {'value': -28, 'units': 'c'},
                'p_in': {'value': 1.0, 'units': 'bar'},
                'dp_friction': {'value': 0.0, 'units': 'bar'}
               }
rhex.calc_qt_diagram(flow_hot, flow_cold)

print(rhex.flow_hot.fluid)
print(rhex.flow_hot.t_k)
print(rhex.flow_hot.p_kpa)

rhex.flow_hot.fluid.calc_sat_state(sat_curve_flag='v', p=(100.0, 'kPa'))

if rhex.flow_hot.fluid.error.index > 0:
    rhex.flow_hot.fluid.error.print_and_terminate()
else:
    # mixture.convert_dataset_to_user_units(flag_data='dew')
    # print(mixture.state.data['dew'])
    # mixture.print_spec_state(units_tag='internal')
    # mixture.print_spec_state(units_tag='user')

    rhex.flow_hot.fluid.print_sat_state(sat_curve_symbol='v', units_tag='internal')
    # butane.print_sat_state(sat_curve_symbol='v', units_tag='user')
