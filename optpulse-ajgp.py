import sys
import numpy as np
# AJGP: better to use specific imports
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
print("Propagator:\n", qtrlresult.evo_full_final)


# Calculate the evolution of up state under the above amps
tlist = qtrlresult.time
print("tlist:", tlist)
print("qtrl_amps:", qtrl_amps)
finetimes = np.arange(0, evo_time, 0.1)


amps = np.append(qtrl_amps, 10)
for t in finetimes:
    print("t: {}, amps: {}".format(t, get_amp(t, amps, tlist)))

#amps = np.insert(qtrl_amps, 0, qtrl_amps[0])
H = [H_d, [H_c[0], amps]]
result = mesolve(H, basis(2,0), tlist, options=Options(store_final_state=True))
plus_state = (basis(2,0)+ basis(2,1)).unit()

print("Num states: ", len(result.states))
print("Fidellity from mesolve:", fidelity(result.final_state, plus_state))

sys.exit()

# Calculate the evolution of up state under the above amps
tlist = qtrlresult.time[:-1]
amps = qtrl_amps
H = [H_d, [H_c[0], amps]]
result = mesolve(H, basis(2,0), tlist)
plus_state = (basis(2,0)+ basis(2,1)).unit()
print("Fidellity from mesolve:", fidelity(result.states[-1], plus_state))

# Now I refine the pulse sequence: eg
# tlist = [0, 1, 2] -> tlist = [0, 0.5, 1.0, 1.5 ... 2.5]
# amps = [0.5, 0.3, 0.4] -> amps = [0.5, 0.5, 0.3, 0.3, 0.4, 0.4]
dt = 0.01  # change dt
# dt = 1
tlist = np.arange(0, evo_time, dt)
# AJGP: no spaces when using kwarg=value
amps = np.repeat(qtrl_amps, 1/dt, axis=0)
H = [H_d, [H_c[0], amps]]
result = mesolve(H, basis(2,0), tlist)
plus_state = (basis(2,0)+ basis(2,1)).unit()
print("Fidellity from mesolve with refined pulse sequence:",
    fidelity(result.states[-1], plus_state))