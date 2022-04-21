from flow.flow_abc import Flow


class FlowCold(Flow):

    cold_flows_total_number = 0

    def __init__(self):
        super().__init__()
        self.index = FlowCold.cold_flows_total_number
        FlowCold.cold_flows_total_number += 1

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
        super().initiate(flow_fluid, flow_input_data, n_cs)
        # cold flow moves towards the hot one. it means that inlet port has index n:
        # 0  <-  1   <-  2   <-  3  <- ... <- n: inlet port
        self.t_k.reverse()
        self.t_k_iter.reverse()
        self.p_kpa.reverse()
        self.h_jmol.reverse()

    def _set_t_initial(self):
        # i:    0  --  1   --  2   --  3   ... n, where n = number of hex's C-sections
        super()._set_t_initial()

    def _set_p(self):
        # i:    0  --  1   --  2   --  3   ... n, where n = number of hex's C-sections
        # p:  p_in -> p[1] -> p[2] -> p[3] ... p[n] = p_in - dp_friction;  linear dependence
        super()._set_p()

    def _set_h_initial(self):
        # i:    0  --  1   --  2   --  3   ... n, where n = number of hex's C-sections
        super()._set_h_initial()

    def set_t_linear(self):
        # i:    0  --  1   --  2   --  3   ... n, where n = number of hex's C-sections
        # t:  t_in -> t=a*i+b -> t_out
        # both self.t_k[0] and self.t_k[n] should be already known
        super().set_t_linear()

    def set_t_k_iter(self):
        super().set_t_k_iter()

    def calc_h_jmol(self, index):

        if index == self.n_cs and self.h_jmol[index] is not None:
            return self.h_jmol[index]

        super().calc_h_jmol(index)

    def calc_dq_w_along_flow(self, index_in=None, index_out=None):
        # for cold flow dq_w_along_flow < 0    (for hot flow dq > 0)
        super().calc_dq_w_along_flow(index_in=None, index_out=None)

    def calc_tout_knowing_dq_w_along_flow(self, index_in=None, index_out=None, dq_w_along_flow=None):
        # NOTE: for cold flow dq_w_along_flow < 0    (for hot flow dq > 0)
        super().calc_tout_knowing_dq_w_along_flow(index_in=None, index_out=None, dq_w_along_flow=None)
