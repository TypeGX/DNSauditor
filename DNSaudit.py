import subprocess

def run_sublist3r(domain):
    print(f"Running Sublist3r on {domain}...")
    result = subprocess.run(['sublist3r', '-d', domain, '-o', 'subdomains.txt'], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Sublist3r failed: {result.stderr}")
        return []
    print(f"Sublist3r completed. Results saved to subdomains.txt")
    with open('subdomains.txt', 'r') as file:
        subdomains = file.read().splitlines()
    return subdomains

def run_baddns(subdomains):
    with open('baddns_results.txt', 'w') as output_file:
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
    print("BADDNS results saved to baddns_results.txt")

def trim_baddns_output(output):
    # Extract the relevant information using regex or string manipulation
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
    subdomains = run_sublist3r(domain)
    if not subdomains:
        print("No subdomains found or Sublist3r failed.")
        return
    baddns_results = run_baddns(subdomains)
    if not baddns_results:
        print("BADDNS did not return any output.")
        return
    print("BADDNS Output:")
    for subdomain, output in baddns_results:
        print(f"Subdomain: {subdomain}")
        print(output)

if __name__ == "__main__":
    main()