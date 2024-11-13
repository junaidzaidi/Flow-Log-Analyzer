import unittest
from src.flow_log_parser import read_lookup_table, process_logs
from unittest.mock import mock_open, patch

class TestFlowLogParser(unittest.TestCase):

    # Test the reading of the lookup table
    @patch("builtins.open", new_callable=mock_open, read_data="dstport,protocol,tag\n443,tcp,sv_P2\n80,tcp,sv_P1\n")
    def test_read_lookup_table(self, mock_file):
        lookup_table = read_lookup_table("mock_lookup_table.csv")
        self.assertEqual(lookup_table[("443", "tcp")], "sv_P2")
        self.assertEqual(lookup_table[("80", "tcp")], "sv_P1")
        mock_file.assert_called_with("mock_lookup_table.csv", "r")

    # Test the processing of flow logs
    @patch("builtins.open", new_callable=mock_open, read_data="2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 49153 6 25 20000 1620140761 1620140821 ACCEPT OK\n")
    def test_process_logs(self, mock_file):
        # Prepare a mock lookup table
        lookup_table = {
            ("49153", "tcp"): "sv_P2",
            ("80", "tcp"): "sv_P1"
        }
        tag_counts, port_protocol_counts = process_logs("mock_flow_log.txt", lookup_table)
        self.assertEqual(tag_counts["sv_P2"], 1)
        self.assertEqual(port_protocol_counts[("49153", "tcp")], 1)
        mock_file.assert_called_with("mock_flow_log.txt", "r")

    # Test when no matching entry is found in the lookup table (Untagged tag)
    @patch("builtins.open", new_callable=mock_open, read_data="2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 9999 49153 6 25 20000 1620140761 1620140821 ACCEPT OK\n")
    def test_process_logs_no_match(self, mock_file):
        # Prepare a mock lookup table
        lookup_table = {
            ("443", "tcp"): "sv_P2",
            ("80", "tcp"): "sv_P1"
        }
        tag_counts, port_protocol_counts = process_logs("mock_flow_log.txt", lookup_table)
        self.assertEqual(tag_counts["Untagged"], 1)
        self.assertEqual(port_protocol_counts[("49153", "tcp")], 1)
        mock_file.assert_called_with("mock_flow_log.txt", "r")

if __name__ == "__main__":
    unittest.main()
