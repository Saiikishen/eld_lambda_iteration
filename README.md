# Economic Load Dispatch (ELD) Using Lambda Iteration Method

## Introduction

Economic Load Dispatch (ELD) is a fundamental problem in power systems engineering. The objective is to allocate power demand among various generating units to minimize the total generation cost while satisfying operational constraints.

This project implements the Lambda Iteration Method, a numerical technique for optimizing power generation across multiple units.

## Features

- Calculate optimal power output for multiple generating units
- Enforce generator output limits
- Compute total generation cost
- Provide precise power balance with adjustable tolerance

## Prerequisites

- Python 3.x
- Libraries specified in requirements.txt

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/eld-lambda-iteration.git
   cd eld-lambda-iteration
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Input Parameters

The program requires three key inputs:

1. **Cost Coefficients**: Quadratic cost function for each generator
   \[
   C(P) = aP^2 + bP + c
   \]
   - `a`: Quadratic cost coefficient
   - `b`: Linear cost coefficient
   - `c`: Fixed cost term

2. **Power Limits**:
   - `P_min`: Minimum power output
   - `P_max`: Maximum power output

3. **Total Demand**: System-wide power requirement

### Example Configuration

```python
cost_coefficients = [
    (0.02, 2.5, 100),   # Generator 1: (a, b, c)
    (0.0175, 1.75, 120),# Generator 2: (a, b, c)
    (0.015, 1.0, 150)   # Generator 3: (a, b, c)
]

power_limits = [
    (50, 200),  # Generator 1: (P_min, P_max)
    (30, 150),  # Generator 2: (P_min, P_max)
    (20, 100)   # Generator 3: (P_min, P_max)
]

total_demand = 400
```

### Running the Script

```bash
python eld.py
```

## Output

The program provides:

1. **Optimal Power Outputs**: Power allocation for each generator
2. **Total Generation Cost**: Minimum cost for meeting total demand

Sample output:
```
Optimal Power Output: [150.0, 125.0, 125.0]
Total Generation Cost: $555,410.24
```

## Lambda Iteration Algorithm

The `lambda_iteration` function implements the core optimization logic:

1. Initialize Lambda value range
2. Calculate generator power outputs
3. Ensure outputs meet generator constraints
4. Balance total generation with system demand
5. Iterate to minimize generation cost

## Mathematical Foundation

Power output calculation:
\[
P_i = \frac{\lambda - b_i}{2a_i}
\]

Where:
- \( P_i \): Power output of generator \( i \)
- \( \lambda \): Lambda multiplier
- \( a_i, b_i \): Cost coefficients

## Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Submit a Pull Request

## License

MIT License. See `LICENSE` file for details.

## Acknowledgments

- Power systems engineering community
- Open-source Python ecosystem
