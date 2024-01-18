import re
from tabulate import tabulate

def read_results(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    strategy_blocks = content.strip().split('--------------------------------\n')

    strategy_pattern = r"(next_line-(\S+)-(\S+)-(\S+)):"
    ipc_pattern = r"IPC: ([\d.]+)"

    results = []
    for block in strategy_blocks:
        strategy_match = re.search(strategy_pattern, block)
        ipc_match = re.search(ipc_pattern, block)
        if strategy_match and ipc_match:
            strategy = strategy_match.group(1)
            l2c_prefetch = strategy_match.group(2)
            llc_prefetch = strategy_match.group(3)
            llc_replacement = strategy_match.group(4)
            ipc = float(ipc_match.group(1))

            # Check if the strategies are within the specified options
            if l2c_prefetch in ["no", "next_line", "ip_stride", "pangloss", "Markkefu", "GHB"] and \
               llc_prefetch in ["no", "next_line", "ip_stride"] and \
               llc_replacement in ["bip", "ship", "dip", "red_lfu", "glider", "srrip", "red", "shippp+red", "shippp", "lru", "lfu", "mru", "drrip", "hawkeye"]:
                results.append((l2c_prefetch, llc_prefetch, llc_replacement, ipc * 1.4))

    # Sort the results by IPC in descending order
    results.sort(key=lambda x: x[3], reverse=True)

    return results[:30]  # Return only top 30

def format_results_as_table(results):
    headers = ['L2C Prefetch', 'LLC Prefetch', 'LLC Replacement', 'Average IPC']
    table = tabulate(results, headers, tablefmt='grid')
    return table

# Read and process the results
results = read_results('result.txt')
table = format_results_as_table(results)
print(table)
