# Flow Log Analyzer

This Python program processes flow logs (version 2 format), parses the log data, and maps each flow log entry to a tag based on a lookup table. The program then generates a summary report that includes tag counts and port/protocol combination counts.

## Requirements

- Python 3.x
- No external libraries are required (uses only standard Python libraries).

## Assumptions

- The program **only supports the default log format (version 2)** of Flow Logs.
- The **lookup table** must contain **`dstport`**, **`protocol`**, and **`tag`** columns for matching the flow logs.
- The **protocol number** is mapped to its corresponding name using a predefined dictionary, which **only supports standard protocol numbers** as defined by [IANA Protocol Numbers](https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml).

## Folder Structure

project_folder/
│
├── src/ # Source code for the program
│ ├── **init**.py # Make the src folder a package
│ ├── protocol_map.py # Dictionary mapping protocol numbers to protocol names
│ ├── flow_log_parser.py # Logic for parsing flow logs and processing the lookup table
│ ├── flow_log_analyzer.py # Logic for generating reports from processed data
│ ├── run.py # Main entry point to run the program
│
├── data/ # Folder for input/output data
│ ├── sample_flow_logs.txt # Sample flow logs (input)
│ ├── lookup_table.csv # Lookup table CSV file (input)
│ ├── flow_log_report.txt # Output file where the report is saved
│
├── README.md # Project overview and instructions on how to run the program

## How to Run

1. Clone or download this repository to your local machine. [git clone <>]
2. Navigate to the project folder.
3. Ensure that the `data/` folder contains the necessary input files:
   - `sample_flow_logs.txt`: Your flow log data in the correct format (Flow Log, version 2).
   - `lookup_table.csv`: The lookup table CSV file that maps `dstport` and `protocol` to `tag`.
4. Run **`python3 src/run.py`**
5. The report will be generated in `data/flow_log_report.txt`.

## How the Program Works

1. Mappings
   - Creates a `protocol_map` to map `protocol_code -> protocol_name`.
   - Creates a `lookup_table ((dstport, protocol) -> tag)` by reading `lookup_table.csv`.
2. Processing the Flow Logs:
   - The program reads each line from the flow log file, extracts the `dstport` and `protocol`, and uses the lookup table to assign a tag.
   - If no match is found for a particular `dstport` and `protocol` combination, the tag `Untagged` is assigned.
3. Generating the Report:
   - The program counts how many times each `tag` appears and how many times each `(dstport, protocol)` combination is found in the flow logs.
   - The results are written to a text file: `(flow_log_report.txt)`.

## Runtime Complexity

The program operates with the following time and space complexities:

- **Time Complexity**:

  - **Processing the Flow Logs**: `O(m)` where `m` is the number of flow log entries.
  - **Reading the Lookup Table**: `O(n)` where `n` is the number of rows in the lookup table.
  - **Generating the Report**: `O(m + n)` where `m` is the number of flow log entries and `n` is the number of unique `(dstport, protocol)` combinations.

  **Overall Time Complexity**: `O(m + n)`.

- **Space Complexity**:
  - **Space Complexity**: `O(n + m)` where:
    - `n` is the number of entries in the lookup table (stored as `(dstport, protocol)` keys and their corresponding tags).
    - `m` is the number of unique tag and port/protocol combinations found in the flow logs (stored in the respective count dictionaries).

These complexities are linear, meaning the program should scale reasonably well with large datasets.
