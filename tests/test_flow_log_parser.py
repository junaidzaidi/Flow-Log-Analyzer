import unittest
from src.flow_log_parser import read_lookup_table, process_logs
from unittest.mock import mock_open, patch

class TestFlowLogParser(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data="dstport,protocol,tag\n443,tcp,sv_P2\n80,tcp,sv_P1\n")
    def test_read_lookup_table(self, mock_file):
        print('Test Case: Should return a lookup table with correct mappings from the file.')
        lookup_table = read_lookup_table("mock_lookup_table.csv")
        self.assertEqual(lookup_table[("443", "tcp")], "sv_P2")
        self.assertEqual(lookup_table[("80", "tcp")], "sv_P1")
        mock_file.assert_called_with("mock_lookup_table.csv", "r")
        print("\u2714 Test Passed")

    @patch("builtins.open", new_callable=mock_open, read_data="2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 49153 6 25 20000 1620140761 1620140821 ACCEPT OK\n")
    def test_process_logs(self, mock_file):
        print('Test Case: Should return the correct tag counts and port/protocol counts when processing the flow log.')
        lookup_table = {
            ("49153", "tcp"): "sv_P2",
            ("80", "tcp"): "sv_P1"
        }
        tag_counts, port_protocol_counts, logs_count = process_logs("mock_flow_log.txt", lookup_table)
        self.assertEqual(tag_counts["sv_P2"], 1)
        self.assertEqual(port_protocol_counts[("49153", "tcp")], 1)
        self.assertEqual(logs_count, 1)
        mock_file.assert_called_with("mock_flow_log.txt", "r")
        print("\u2714 Test Passed")

    @patch("builtins.open", new_callable=mock_open, read_data="2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 9999 49153 6 25 20000 1620140761 1620140821 ACCEPT OK\n")
    def test_process_logs_no_match(self, mock_file):
        print('Test Case: Should return "Untagged" for logs where no matching entry is found in the lookup table.')
        lookup_table = {
            ("443", "tcp"): "sv_P2",
            ("80", "tcp"): "sv_P1"
        }
        tag_counts, port_protocol_counts, logs_count = process_logs("mock_flow_log.txt", lookup_table)
        self.assertEqual(tag_counts["Untagged"], 1)
        self.assertEqual(port_protocol_counts[("49153", "tcp")], 1)
        self.assertEqual(logs_count, 1)
        mock_file.assert_called_with("mock_flow_log.txt", "r")
        print("\u2714 Test Passed")

    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_empty_lookup_file(self, mock_file):
        print('Test Case: Should return an empty dictionary when the lookup file is empty.')
        lookup_table = read_lookup_table("empty_lookup_table.csv")
        self.assertEqual(lookup_table, {})  # Should return an empty dictionary
        mock_file.assert_called_with("empty_lookup_table.csv", "r")
        print("\u2714 Test Passed")

    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_empty_flow_log_file(self, mock_file):
        print('Test Case: Should return empty counts when the flow log file is empty.')
        lookup_table = {
            ("443", "tcp"): "sv_P2",
            ("80", "tcp"): "sv_P1"
        }
        tag_counts, port_protocol_counts, logs_count = process_logs("empty_flow_log.txt", lookup_table)

        self.assertEqual(tag_counts, {})  # Should return empty tag counts
        self.assertEqual(port_protocol_counts, {})  # Should return empty port/protocol counts
        self.assertEqual(logs_count, 0)  # Should return 0 logs processed

        mock_file.assert_called_with("empty_flow_log.txt", "r")
        print("\u2714 Test Passed")

if __name__ == "__main__":
    unittest.main()
