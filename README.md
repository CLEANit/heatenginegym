# Heat engine gym

A collection of heat engines, based on the OpenAI Gym environment framework for use with reinforcement learning applications.  If you use this gym, please cite

```bibtex
@article{beeler2021optimizing,
  title = {Optimizing thermodynamic trajectories using evolutionary and gradient-based reinforcement learning},
  author = {Beeler, Chris and Yahorau, Uladzimir and Coles, Rory and Mills, Kyle and Whitelam, Stephen and Tamblyn, Isaac},
  journal = {Phys. Rev. E},
  volume = {104},
  issue = {6},
  pages = {064128},
  numpages = {10},
  year = {2021},
  month = {Dec},
  publisher = {American Physical Society},
  doi = {10.1103/PhysRevE.104.064128},
  url = {https://link.aps.org/doi/10.1103/PhysRevE.104.064128}
}
```


## To install:
```bash
pip install ./
```

## Environments


Environment | Description
--- | ---
Carnot-v0 | Heat engine environment with action space restricted to the required actions. 
Carnot-v1 | Heat engine environment with full action space.
Carnot-v2 | Heat engine environment with full action space and discrete variable dV actions.
Carnot-v3 | Heat engine environment with full action space and continuous variable dV actions.
Carnot-v4 | Heat engine environment with full action space, W and Qin included in the state, and finite W and Qin available. Change in W after final step is used for reward.
Stirling-v0 | Heat engine environment with adiabatic actions unavailable.
Stirling-v1 | Heat engine environment with adiabatic actions unavailable and variable dV actions.
Otto-v0 | Heat engine environment with isothermal actions unavailable.
Otto-v1 | Heat engine environment with isothermal actions unavailable and variable dV actions.
Beeler-v0 | Heat engine environment with adiabatic actions replaced with irreversible actions.
Beeler-v1 | Heat engine environment with adiabatic actions replaced with irreversible actions and variable dV actions.


## Version history:

- Version 1.0 released 2018-11-11.


## To  run

See demo.py for an example.



