import unittest
from unittest.mock import mock_open, patch
from src.flow_log_analyzer import generate_report

class TestFlowLogAnalyzer(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open)
    def test_generate_report(self, mock_file):
        # Mock tag counts and port/protocol combination counts
        tag_counts = {
            "sv_P2": 1,
            "sv_P1": 2,
            "Untagged": 3
        }

        port_protocol_counts = {
            ("443", "tcp"): 1,
            ("80", "tcp"): 2,
            ("9999", "tcp"): 3
        }

        # Generate the report
        generate_report(tag_counts, port_protocol_counts, "mock_report.txt")

        # Check if the file was opened in write mode
        mock_file.assert_called_with("mock_report.txt", "w")

        # Check if the correct content was written to the file
        handle = mock_file()
        handle.write.assert_any_call("Tag Counts:\n")
        handle.write.assert_any_call("sv_P2,1\n")
        handle.write.assert_any_call("sv_P1,2\n")
        handle.write.assert_any_call("Untagged,3\n")

        handle.write.assert_any_call("\nPort/Protocol Combination Counts:\n")
        handle.write.assert_any_call("443,tcp,1\n")
        handle.write.assert_any_call("80,tcp,2\n")
        handle.write.assert_any_call("9999,tcp,3\n")

if __name__ == "__main__":
    unittest.main()
