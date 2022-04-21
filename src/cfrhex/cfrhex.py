import math
import converters as conv

from flow.flow_cold import FlowCold
from flow.flow_hot import FlowHot


class CfRHex2Flows:  # Counter flow Recuperative Heat exchanger with 2 counter flows

    def __init__(self, eps=1.0, dt=10.0):
        """
          eps - hex's efficiency; eps E ]0..1]
          dt - temperature interval along the flow, to calculate number of cross-sections
        """
        self.flow_hot = FlowHot()
        self.flow_cold = FlowCold()
        self.eps = eps
        self.dt_along_flow = dt
        self.n_cs = None  # number of cross-sections =f(dt); flow indexing: 0--1--2--...--n_cs

    def _initiate_hex_flows(self, flow_hot, flow_cold):
        # flow_hot = [fluid, data]
        # data = {
        #         'm': {'value': None, 'units': 'kgs'},
        #         't_in': {'value': None, 'units': None},
        #         'p_in': {'value': None, 'units': None},
        #         'dp_friction': {'value': None, 'units': None}
        #        }
        # n_cs = number of hex's cross-sections; n_cs = index_max: i=0, 1, 2, 3, ... , n_sc

        # calculate number of hex's cross-sections: f(t_hot_in, t_cold_in, self.dt_along_flow)
        if flow_hot[1]['t_in']['units'] == flow_cold[1]['t_in']['units']:
            self.n_cs = self._calc_number_of_cross_sections(t_hot_in=flow_hot[1]['t_in']['value'],
                                                            t_cold_in=flow_cold[1]['t_in']['value'])
        else:
            t_hot_in_k = conv.convert_arg_to_internal_units(flow_hot[1]['t_in']['value'],
                                                            flow_hot[1]['t_in']['units'])
            t_cold_in_k = conv.convert_arg_to_internal_units(flow_cold[1]['t_in']['value'],
                                                             flow_cold[1]['t_in']['units'])
            self.n_cs = self._calc_number_of_cross_sections(t_hot_in=t_hot_in_k,
                                                            t_cold_in=t_cold_in_k)

        # set initial parameters of flows: fluid, m, t_in, p_in, dp, n_cs
        self.flow_hot.initiate(flow_hot[0], flow_hot[1], self.n_cs)
        self.flow_cold.initiate(flow_cold[0], flow_cold[1], self.n_cs)

    def _calc_number_of_cross_sections(self, t_hot_in=None, t_cold_in=None):
        return math.ceil((t_hot_in - t_cold_in) / self.dt_along_flow)

    def calc_qt_diagram(self, flow_hot, flow_cold):
        """
        flow_hot = [fluid, data]
        fluid = fluid -> RP10Fluid
        data = {
                'm': {'value': None, 'units': 'kgs'},
                't_in': {'value': None, 'units': None},
                'p_in': {'value': None, 'units': None},
                'dp_friction': {'value': None, 'units': None}
               }
        """
        self._initiate_hex_flows(flow_hot, flow_cold)
