import pandas as pd


def economic_load_dispatch(load_demand, gen_limits, cost_coeffs, tolerance=1e-3, max_iterations=5000):

    total_min = sum([limits[0] for limits in gen_limits])
    total_max = sum([limits[1] for limits in gen_limits])

    if not (total_min <= load_demand <= total_max):
        raise ValueError(f"Load demand {load_demand} is out of feasible range ({total_min} to {total_max})!")

    lambda_min = min((cost_coeffs[i][1] + 2 * cost_coeffs[i][2] * gen_limits[i][0]) 
                    for i in range(len(gen_limits)))
    lambda_max = max((cost_coeffs[i][1] + 2 * cost_coeffs[i][2] * gen_limits[i][1]) 
                    for i in range(len(gen_limits)))
    
    lambda_curr = (lambda_min + lambda_max) / 2
    step_size = (lambda_max - lambda_min) / 4 

    for iteration in range(max_iterations):
     
        P = []
        for (Pmin, Pmax), (_, b, c) in zip(gen_limits, cost_coeffs):
         
            P_unconstrained = (lambda_curr - b) / (2 * c)
          
            P_constrained = min(max(P_unconstrained, Pmin), Pmax)
            P.append(P_constrained)

        total_power = sum(P)
        power_mismatch = total_power - load_demand

        
        if abs(power_mismatch) <= tolerance:
            total_cost = sum(a + b * Pi + c * Pi ** 2 
                           for Pi, (a, b, c) in zip(P, cost_coeffs))
            return P, total_cost

        
        step_size = step_size * 0.95 if iteration > 10 else step_size
        
        
        lambda_change = -power_mismatch * step_size / sum(1 / (2 * c) 
                        for _, _, c in cost_coeffs)
        lambda_curr += lambda_change

        
        lambda_curr = min(max(lambda_curr, lambda_min * 0.5), lambda_max * 1.5)

    raise RuntimeError(f"Lambda iteration did not converge after {max_iterations} iterations. "
                      f"Final power mismatch: {power_mismatch:.2f} MW")

def run_eld_forecast(forecast_filepath, gen_limits, cost_coeffs, datetime_col="ds", 
                    tolerance=1e-3, max_iterations=20000):
  
    
    forecast_data = pd.read_csv(forecast_filepath)

    if datetime_col not in forecast_data.columns:
        raise KeyError(f"Column '{datetime_col}' not found in forecast file. "
                      f"Available columns: {forecast_data.columns}")

    results = []
    for index, row in forecast_data.iterrows():
        load_demand = row["yhat"]  
        try:
            P, total_cost = economic_load_dispatch(load_demand, gen_limits, cost_coeffs, 
                                                 tolerance, max_iterations)
            results.append({
                datetime_col: row[datetime_col],
                "load_demand": load_demand,
                "generation": P,
                "total_cost": total_cost,
            })
        except (RuntimeError, ValueError) as e:
            print(f"Error at {row[datetime_col]}: {e}")
            results.append({
                datetime_col: row[datetime_col],
                "load_demand": load_demand,
                "generation": None,
                "total_cost": None,
            })

    return pd.DataFrame(results)



gen_limits = [(500, 2500), (1000, 3500), (500, 1500), (100, 1500)]
cost_coeffs = [(50, 20, 0.002), (40, 18, 0.0015), (60, 22, 0.0025), (30, 15, 0.001)]
load_demand = 5711.158 

try:
    P, total_cost = economic_load_dispatch(load_demand, gen_limits, cost_coeffs)
    print(f"Generator outputs: {[f'{p:.2f}' for p in P]}")
    print(f"Total cost: {total_cost:.2f}")
except (RuntimeError, ValueError) as e:
    print(f"Error: {e}")