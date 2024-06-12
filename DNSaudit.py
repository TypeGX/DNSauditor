import subprocess
import os

def run_sublist3r(domain, subdomains_output_file):
    print(f"Running Sublist3r on {domain}...")
    result = subprocess.run(['sublist3r', '-d', domain, '-o', subdomains_output_file], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Sublist3r failed: {result.stderr}")
        return []
    if not os.path.exists(subdomains_output_file):
        print(f"Sublist3r did not create the output file: {subdomains_output_file}")
        return []
    print(f"Sublist3r completed. Results saved to {subdomains_output_file}")
    with open(subdomains_output_file, 'r') as file:
        subdomains = file.read().splitlines()
    return subdomains

def run_baddns(subdomains, baddns_output_file):
    with open(baddns_output_file, 'w') as output_file:
        for subdomain in subdomains:
            print(f"Running BADDNS on {subdomain}...")
            result = subprocess.run(['baddns', '-d', subdomain], capture_output=True, text=True)
            if result.returncode != 0:
                print(f"BADDNS failed for {subdomain}: {result.stderr}")
                continue
            trimmed_output = trim_baddns_output(result.stdout)
            output_file.write(f"Subdomain: {subdomain}\n")
            output_file.write(f"{trimmed_output}\n\n")
            print(f"BADDNS completed for {subdomain}. Results saved.")
    print(f"BADDNS results saved to {baddns_output_file}")

def trim_baddns_output(output):
    trimmed_output = ""
    lines = output.splitlines()
    for line in lines:
        if "Vulnerable!" in line or "Subdomain:" in line:
            trimmed_output += line + "\n"
        elif line.startswith("{") and line.endswith("}"):
            trimmed_output += line + "\n"
    return trimmed_output

def main():
    domain = input("Enter the root domain: ")
    subdomains_output_file = input("Enter the filename for subdomains output: ")
    baddns_output_file = input("Enter the filename for BADDNS results output: ")
    
    subdomains = run_sublist3r(domain, subdomains_output_file)
    if not subdomains:
        print("No subdomains found or Sublist3r failed.")
        return
    run_baddns(subdomains, baddns_output_file)

if __name__ == "__main__":
    main()
