# Carnot world

## Version history:

- r0.1: working environment.

- r0.2: working gym environment.

- r0.3: working gym environment with regular and limited action spaces. Network and grid policy based GA.

- r0.4: working gym environment with regular and limited action spaces and variable dV. Network and grid policy based GA with multiprocessing. Carnot, Stirling, Otto, and Beeler cycle environments available.




## To install:
```bash
pip install -e ./
```



## Environments

- Carnot-v0: Heat engine environment with action space restricted to the required actions.

- Carnot-v1: Heat engine environment with full action space.

- Carnot-v2: Heat engine environment with full action space and variable dV actions.

- Stirling-v0: Heat engine environment with adiabatic actions unavailable.

- Stirling-v1: Heat engine environment with adiabatic actions unavailable and variable dV actions.

- Otto-v0: Heat engine environment with isothermal actions unavailable.

- Otto-v1: Heat engine environment with isothermal actions unavailable and variable dV actions.

- Beeler-v0: Heat engine environment with adiabatic actions replaced with irreversible actions.

- Beeler-v1: Heat engine environment with adiabatic actions replaced with irreversible actions and variable dV actions.


## To  run

See demo.py for an example.



