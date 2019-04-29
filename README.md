# Heat engine gym

A collection of heat engines, based on the OpenAI Gym environment framework for use with reinforcement learning applications.  If you use this gym, please cite

```bibtex
@article{beeler2019optimizing,
  title={Optimizing thermodynamic trajectories using evolutionary reinforcement learning},
  author={Beeler, Chris and Yahorau, Uladzimir and Coles, Rory and Mills, Kyle and Whitelam, Stephen and Tamblyn, Isaac},
  journal={arXiv preprint arXiv:1903.08543},
  year={2019}
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
Carnot-v2 | Heat engine environment with full action space and variable dV actions.
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



