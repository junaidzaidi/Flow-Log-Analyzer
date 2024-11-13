
from flow_log_parser import read_lookup_table, process_logs
from flow_log_analyzer import generate_report
import os

def run_flow_log_analysis(flow_log_file, lookup_table_file, output_file):
    """
    Function that orchestrates reading the lookup table, processing the flow log, and generating the report.
    """
    # Read lookup table into a dictionary
    lookup_table = read_lookup_table(lookup_table_file)
    
    # Process flow logs line by line and generate counts
    tag_counts, port_protocol_counts = process_logs(flow_log_file, lookup_table)
    
    # Generate and write the report to a file
    generate_report(tag_counts, port_protocol_counts, output_file)

# Example usage
if __name__ == '__main__':
    # Path to files inside the data folder
    # print("PATH", os.path.join('data', 'lookup_table.csv'))
    flow_log_file = os.path.join('data', 'sample_flow_logs.txt')
    lookup_table_file = os.path.join('data', 'lookup_table.csv')
    output_file = os.path.join('data', 'flow_log_report.txt')
    # data/lookup_table.csv

    # Run the analysis
    run_flow_log_analysis(flow_log_file, lookup_table_file, output_file)
