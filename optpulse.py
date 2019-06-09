import sys
from collections import Counter
import numpy as np
from qutip import *
import qutip.control.pulseoptim as cpo
np.random.seed(3)

def get_amp(t, amps, times):
    """
    This is the func as it is implemented in
    `qutip.rhs_generrate._td_wrap_array_str`
    """
    n_t = len(times)
    t_f = times[-1]
    if t > t_f:
        return 0.0
    else:
        return amps[int(round((n_t-1)*t/t_f))]

# Setup
N = 1
H_d = sigmaz()
H_c = [sigmax()]

qc = QubitCircuit(N)
qc.add_gate("SNOT", 0)
hadamard = qc.propagators()[0]

U_targ = hadamard
U_0 = identity(U_targ.dims[0])
n_ts = 10
evo_time = 10

# Calculate amps with pulseoptim
qtrlresult = cpo.optimize_pulse_unitary(H_d, H_c, U_0,
    U_targ, n_ts, evo_time)
qtrl_amps = qtrlresult.final_amps[:, 0]

print("Fidelity error from optimal pulse:", qtrlresult.fid_err)

# My way of solving the in consistensy in get_amp:
# Modify time and amps a bit, so that it becomes 
# new_tlist = [ 0, 1, 2, 3, 4, 5, 6...,10,11] 
# new_amps =  [ 0,a0,a1,a2,a3,a4,a5...,a9, 0]
tau = int(evo_time/n_ts)
# Add a 1.0e-10 to conpensate the unstable round(x.5)
new_tlist = np.hstack([qtrlresult.time, [qtrlresult.time[-1] + tau]]) + 1.0e-10
new_amps = np.hstack([[0.], qtrl_amps, [0.]])

# calculate the refined time and amplitude with get_amp
dt = 0.001
finetimes = np.arange(0, evo_time+1, dt)
fineamps = [get_amp(t, new_amps, new_tlist) for t in finetimes]
# count the number of each amplitude in the refined
count_res = Counter(fineamps)
print("The count for each amps in new_amps: ")
for key in count_res:
    print(key, count_res[key])
# There is 10 non-zero amps, all have the same counts, as long as dt>1.0e-10
# if mesolve follows the get_amp defined above, 
# the new_tlist and new_amps should solve the mimatch

H = [H_d, [H_c[0], new_amps]]
result = mesolve(H, basis(2,0), new_tlist, options=Options(store_final_state=True))
plus_state = (basis(2,0)+ basis(2,1)).unit()
print("Fidellity from mesolve:", fidelity(result.final_state, plus_state))
# The fidellity increase only a bit but far from being perfect