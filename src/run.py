
from flow_log_parser import read_lookup_table, process_logs
from flow_log_analyzer import generate_report
import os

def run_flow_log_analysis(flow_log_file, lookup_table_file, output_file):
    """
    Function that orchestrates reading the lookup table, processing the flow log, and generating the report.
    """
    print("Running flow log analysis:")
    
    # print(f"Reading from the lookup table file: {lookup_table_file}")
    lookup_table = read_lookup_table(lookup_table_file)
    print(f"Read {len(lookup_table)} records from the lookup table file: {lookup_table_file}")
    
    # print(f"\nProcessing flow logs file: {flow_log_file}")
    tag_counts, port_protocol_counts, count = process_logs(flow_log_file, lookup_table)
    print(f"Processed {count} logs from flow logs file: {flow_log_file}")
    
    generate_report(tag_counts, port_protocol_counts, output_file)
    print(f"Wrote flow log report to file: {output_file}")

if __name__ == '__main__':
    
    flow_log_file = os.path.join('data', 'sample_flow_logs.txt')
    lookup_table_file = os.path.join('data', 'lookup_table.csv')

    # Maximum File Sizes
    # flow_log_file = os.path.join('data', 'sample_flow_logs_10MB.txt')
    # lookup_table_file = os.path.join('data', 'lookup_table_10K.csv')

    # Empty Files
    # flow_log_file = os.path.join('data', 'sample_flow_logs_empty.txt')
    # lookup_table_file = os.path.join('data', 'lookup_table_empty.csv')

    output_file = os.path.join('output', 'flow_log_report.txt')
    
    run_flow_log_analysis(flow_log_file, lookup_table_file, output_file)
