from abc import ABC, abstractmethod
import converters as conv
import sys


class Flow(ABC):
    @abstractmethod
    def __init__(self):
        self.n_cs = None
        self.fluid = None
        self.m_mols = None
        self.t_in_k = None
        self.p_in_kpa = None
        self.dp_friction_kpa = None
        self.t_k = list()
        self.t_k_iter = list()
        self.p_kpa = list()
        self.h_jmol = list()

    @abstractmethod
    def initiate(self, flow_fluid, flow_input_data, n_cs):
        # flow_fluid = fluid -> RP10Fluid
        # flow_input_data = {
        #                    'm': {'value': None, 'units': 'kgs'},
        #                    't_in': {'value': None, 'units': None},
        #                    'p_in': {'value': None, 'units': None},
        #                    'dp_friction': {'value': None, 'units': None}
        #                    }
        # n_cs = number of cross-sections, is equal to the max index:
        # i:    0  ->  1   ->  2   ->  3   ...  n, where n = n_cs
        self.n_cs = n_cs
        self.fluid = flow_fluid
        # set input data: m, t, p and dp into internal units and save as self. ...
        self._set_flow_input_data_to_internal_units(flow_input_data)
        self._set_t_initial()  # t_k[i]=self.t_in_k, i E[0..n]
        self._set_p()  # p_kpa=a*i+b /linear func/; for cold flow p_kpa.reverse() in FlowCold
        self._set_h_initial()  # calc h_jmol[0] = f(p,t), all the rest=None

    def _set_flow_input_data_to_internal_units(self, flow_input_data):

        # mass rate:
        if flow_input_data['m']['units'] == 'mols':
            self.m_mols = flow_input_data['m']['value']
        elif flow_input_data['m']['units'] == 'kgs':
            self.m_mols = conv.convert_mass_rate_to_internal_units(flow_input_data['m']['value'],
                                                                   flow_input_data['m']['units'],
                                                                   self.fluid.mm_g_mol)
        else:
            sys.exit('mass rate units != mols or kgs in func. initiate flow. Program terminated')

        # temperature at the inlet port:
        if flow_input_data['t_in']['units'] == 'k':
            self.t_in_k = flow_input_data['t_in']['value']
        elif flow_input_data['t_in']['units'] == 'c':
            self.t_in_k = conv.convert_arg_to_internal_units(flow_input_data['t_in']['value'],
                                                             flow_input_data['t_in']['units'])
        else:
            sys.exit('t_in units != k or c in func. initiate flow. Program terminated')

        # pressure at the inlet port:
        if flow_input_data['p_in']['units'] == 'kpa':
            self.p_in_kpa = flow_input_data['p_in']['value']
        elif flow_input_data['p_in']['units'] == 'bar':
            self.p_in_kpa = conv.convert_arg_to_internal_units(flow_input_data['p_in']['value'],
                                                               flow_input_data['p_in']['units'])
        else:
            sys.exit('p_in units != kpa or bar in func. initiate flow. Program terminated')

        # pressure losses with friction along the flow:
        if flow_input_data['dp_friction']['units'] == 'kpa':
            self.dp_friction_kpa = flow_input_data['dp_friction']['value']
        elif flow_input_data['dp_friction']['units'] == 'bar':
            self.dp_friction_kpa = conv.convert_arg_to_internal_units(flow_input_data['dp_friction']['value'],
                                                                      flow_input_data['dp_friction']['units'])
        else:
            sys.exit('dp_friction units != kpa or bar in func. initiate flow. Program terminated')

    @abstractmethod
    def _set_t_initial(self):
        # i:    0  --  1   --  2   --  3   ... n_cs, where n_cs = number of hex's C-sections
        self.t_k = [self.t_in_k] * self.n_cs
        self.t_k_iter = [None] * self.n_cs

    @abstractmethod
    def _set_p(self):
        # i:    0  --  1   --  2   --  3   ... n, where n = number of hex's C-sections
        # p:  p_in -> p[1] -> p[2] -> p[3] ... p[n] = p_in - dp_friction;  linear dependence
        for i in range(self.n_cs + 1):
            self.p_kpa.append(self.p_in_kpa - self.dp_friction_kpa / self.n_cs * i)

    @abstractmethod
    def _set_h_initial(self):
        # i:    0  --  1   --  2   --  3   ... n, where n = number of hex's C-sections
        self.h_jmol = [None] * self.n_cs
        inlet_index = 0
        self.h_jmol[inlet_index] = self.calc_h_jmol(inlet_index)

    @abstractmethod
    def set_t_linear(self):
        # i:    0  --  1   --  2   --  3   ... n, where n = number of hex's C-sections
        # t:  t_in -> t=a*i+b -> t_out
        # both self.t_k[0] and self.t_k[n] should be already known
        for i in range(self.n_cs + 1):
            self.t_k.append(self.t_k[0] - (self.t_k[0] - self.t_k[self.n_cs]) / self.n_cs * i)

    @abstractmethod
    def set_t_k_iter(self):
        self.t_k_iter = self.t_k[:]

    @abstractmethod
    def calc_h_jmol(self, index):

        t_k = self.t_k[index]
        p_kpa = self.p_kpa[index]

        self.fluid.calc_spec_state(t=(t_k, 'k'), p=(p_kpa, 'kpa'))

        if self.fluid.error.index > 0:
            self.fluid.error.print_and_terminate()
        else:
            self.h_jmol[index] = self.fluid.state.get_data(flag='blk', x_symbol='h', x_units='jmol')

        return self.h_jmol[index]

    @abstractmethod
    def calc_dq_w_along_flow(self, index_in=None, index_out=None):
        _h_in_jmol = self.calc_h_jmol(index_in)
        _h_out_jmol = self.calc_h_jmol(index_out)
        return (_h_in_jmol - _h_out_jmol) * self.m_mols

    @abstractmethod
    def calc_tout_knowing_dq_w_along_flow(self, index_in=None, index_out=None, dq_w_along_flow=None):
        #

        self.h_jmol[index_out] = self.h_jmol[index_in] - dq_w_along_flow / self.m_mols

        self.fluid.calc_spec_state(h=(self.h_jmol[index_out], 'jmol'),
                                   p=(self.p_kpa[index_out], 'kpa'))

        if self.fluid.error.index > 0:
            self.fluid.error.print_and_terminate()
        else:
            self.t_k[index_out] = self.fluid.state.get_data(flag='blk', x_symbol='t', x_units='k')

        return self.t_k[index_out]
