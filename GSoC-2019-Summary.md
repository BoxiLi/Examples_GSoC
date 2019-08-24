# GSoC 2019 QuTiP: Noise Models in QIP Module

This is the summary and the permanant link for the deliverables of the GSoC 2019 QuTiP project Noise Models in QIP Module.

The aim of this project is to equip the QuTiP `qip` module with a numerical simulator using the open system solver and the optimal control module . 
The final deliverables generalize this goal a little bit and establish a framework for NISQ (Noisy Intermediate-Scale Quantum) simulator, upon which models for different quantum device can be built. Two existing examples in the `qip` modules were refactored and adapted to this new framework. We expect to release these new feature in the next major version of QuTiP.

As it is a framework for simulation of quantum device, furture work includes implementing more concret and modern examples of quantum computing models such us ion trap or superconducting quantum computing.

The main deliverables containing the follwing points:

* A numerical NISQ simulator using the QuTiP opens system solver.
* Refactoring the existing `SpinChain` and `DispersiveQED` module, so that they can also use the numerical simulator.
* A noise module `CircuitNoise` that complements the simulator with a framework for noise handling.

The links to the PRs can be found at:

Main PR for the code: https://github.com/qutip/qutip/pull/1065

Documentation: https://github.com/qutip/qutip-doc/pull/85

Notebooks and examples: https://github.com/qutip/qutip-notebooks/pull/88
