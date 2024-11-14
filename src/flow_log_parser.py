import csv
from protocol_map import protocol_map

def read_lookup_table(lookup_table_file_path):
    """
    Reads the lookup table (CSV file) and returns the dictionary mapping (dstport,protocol) to tag
    """

    lookup_table = {}
    with open(lookup_table_file_path, 'r') as file:
        reader = csv.reader(file)
        # Skip the header row
        header = next(reader, None)

        if header is None:  # In case the file is empty
            return lookup_table

        for row in reader:
            dstport, protocol, tag = row[0], row[1], row[2]
            lookup_table[(dstport, protocol.lower())] = tag
    
    return lookup_table

def process_logs(flow_log_file_path, lookup_table):
    '''
    Parses the flow log file and returns a list of flow log entries as tuple
    '''
    tag_counts = {}
    port_protocol_counts = {}
    logs_count = 0
    with open(flow_log_file_path, 'r') as file:
        for line in file:
            parts = line.split()
            dstport = parts[6]
            protocol_num = int(parts[7]) 
            protocol = protocol_map.get(protocol_num, 'unknown')  # Convert protocol number to string

            # Match protocol with lookup table
            tag = lookup_table.get((dstport, protocol), 'Untagged')

            # Count tags
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

            # Count port/protocol combinations
            port_protocol_counts[(dstport, protocol)] = port_protocol_counts.get((dstport, protocol), 0) + 1
            logs_count += 1

    return tag_counts, port_protocol_counts, logs_count