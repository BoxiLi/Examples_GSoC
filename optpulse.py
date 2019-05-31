import numpy as np
from qutip import *
import qutip.control.pulseoptim as cpo
np.random.seed(3)

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
result = cpo.optimize_pulse_unitary(H_d, H_c, U_0, 
    U_targ, n_ts, evo_time)
print("Fidelity error from optimal pulse:", result.fid_err)
print("Propagator:\n", result.evo_full_final)
tlist = result.time[:-1]
amps = result.final_amps.T

# Calculate the evolution of up state under the above amps
H = [H_d, [H_c[0], amps[0]]]
result = mesolve(H, basis(2,0), tlist)
plus_state = (basis(2,0)+ basis(2,1)).unit()
print("Fidellity from mesolve:", fidelity(result.states[-1], plus_state))

# Now I refine the pulse sequence: eg
# tlist = [0, 1, 2] -> tlist = [0, 0.5, 1.0, 1.5 ... 2.5]
# amps = [0.5, 0.3, 0.4] -> amps = [0.5, 0.5, 0.3, 0.3, 0.4, 0.4]
dt = 0.01  # change dt 
tlist = np.arange(0, 10, dt)
amps = np.repeat(amps, 1/dt, axis = 1)
H = [H_d, [H_c[0], amps[0]]]
result = mesolve(H, basis(2,0), tlist)
plus_state = (basis(2,0)+ basis(2,1)).unit()
print("Fidellity from mesolve with refined pulse sequence:", 
    fidelity(result.states[-1], plus_state))