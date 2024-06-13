import subprocess
import os

def run_script(script_name):
    try:
        result = subprocess.run(['python', script_name], capture_output=True, text=True, check=True)
        print(f"Output of {script_name}:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}:\n{e.stderr}")

def main():
    scripts = [
        'fetch_dividends_and_price_3.py',
        'fetch_dividends_2a_growth_rate.py',
        'fetch_dividends_2a_portfolio_value.py',
        'portfolio_growth_chart_3.py'
    ]
    
    for script in scripts:
        if os.path.exists(script):
            run_script(script)
        else:
            print(f"Script {script} not found.")

if __name__ == "__main__":
    main()
