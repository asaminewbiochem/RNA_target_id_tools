Sure, here's a simple README file based on the provided code:

```
# Monte Carlo Reweight Dihedral Force Constant

This Python script performs Monte Carlo reweighting of dihedral force constants using RMSD with NMR J-coupling as a target function. It is designed to optimize parameters in molecular dynamics simulations.

## Usage

1. **Run the Script**: Execute the script using Python (version 2 or 3) with appropriate command-line arguments.
   
   ```bash
   python monte_carlo_reweight.py
   ```

2. **Input Files**: The script requires input files containing information about dihedral angles, parameters, NMR data, and phi/psi angles. These files should be provided interactively during script execution.

3. **Parameters**: Set the number of Monte Carlo steps (`nstep`) and the temperature (`tempr0`) in the script file.

4. **Output**: The script generates parameter files (`reweight.<run>.str`) and energy files (`reweight.<run>.ene`) in the specified directory.

## Dependencies

- Python 2 or 3
- Standard Python libraries (math, random, string, sys, copy)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

This README provides a brief overview of the script, instructions on usage, dependencies, and licensing information. Feel free to expand or customize it further based on your needs.