
def generate_report(tag_counts, port_protocol_counts, output_file_path):
    """
    Generates a report based on the tag counts and port/protocol counts, and writes it to a plain text (ASCII) file.
    """
    with open(output_file_path, 'w') as file:
        file.write("Tag Counts:\n")
        file.write("dstport,protocol,tag\n")
        for tag, count in tag_counts.items():
            file.write(f"{tag},{count}\n")

        file.write("\nPort/Protocol Combination Counts:\n")
        file.write("Tag,Count \n")
        for (dstport, protocol), count in port_protocol_counts.items():
            file.write(f"{dstport},{protocol},{count}\n")