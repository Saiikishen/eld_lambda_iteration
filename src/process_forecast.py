import pandas as pd
from eld import economic_load_dispatch

def process_load_forecast(forecast_file_path, gen_limits, cost_coeffs):
    # Read the forecast data
    forecast_data = pd.read_csv(forecast_file_path, parse_dates=['Timestamp'])
    
    results = []
    
    for _, row in forecast_data.iterrows():
        timestamp = row['Timestamp']
        load_demand = row['Predicted Load (kW)']
        
        try:
            # The load is already in kW, so we just need to convert to MW
            # Changed from load_demand / 1000 to just the direct conversion
            load_mw = load_demand  # Values are already in correct range
            
            generation, total_cost = economic_load_dispatch(load_mw, gen_limits, cost_coeffs)
            
            results.append({
                'Timestamp': timestamp,
                'Load_Demand_MW': load_mw,
                'Gen1_MW': generation[0],
                'Gen2_MW': generation[1],
                'Gen3_MW': generation[2],
                'Gen4_MW': generation[3],
                'Total_Cost': total_cost
            })
            
        except (ValueError, RuntimeError) as e:
            print(f"Error processing timestamp {timestamp}: {str(e)}")
            results.append({
                'Timestamp': timestamp,
                'Load_Demand_MW': load_mw,
                'Gen1_MW': None,
                'Gen2_MW': None,
                'Gen3_MW': None,
                'Gen4_MW': None,
                'Total_Cost': None
            })
    
    results_df = pd.DataFrame(results)
    return results_df

def main():
    # Generator limits and cost coefficients
    gen_limits = [(500, 2500), (1000, 3500), (500, 1500), (100, 1500)]
    cost_coeffs = [(50, 20, 0.002), (40, 18, 0.0015), (60, 22, 0.0025), (30, 15, 0.001)]
    
    # Process the forecast
    results = process_load_forecast('/home/saiikishen/development/projects/ldc/outputs/forecast_results.csv', gen_limits, cost_coeffs)
    
    # Save results
    results.to_csv('/home/saiikishen/development/projects/ldc/outputs/eld_results.csv', index=False)
    
    # Print summary statistics
    print("\nSummary Statistics:")
    print(f"Average Total Cost: ${results['Total_Cost'].mean():.2f}")
    print("\nGeneration Statistics (MW):")
    for gen in range(1, 5):
        gen_col = f'Gen{gen}_MW'
        print(f"Generator {gen}:")
        print(f"  Average: {results[gen_col].mean():.2f}")
        print(f"  Maximum: {results[gen_col].max():.2f}")
        print(f"  Minimum: {results[gen_col].min():.2f}")

if __name__ == "__main__":
    main()