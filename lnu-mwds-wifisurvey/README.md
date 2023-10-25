# lnu-mwds-wifisurvey

A repo of short scripts to visualize the locations of APs scanned with [Acrylic](https://www.acrylicwifi.com/en/wifi-heatmaps/user-manual/) or [Kismet](https://www.kismetwireless.net/).

## Converting Kismet Files


````python

import kismetdb


parser = argparse.ArgumentParser(description="Kismet to CSV Log Converter")
    
    . . .

parser.add_argument("--table", action="store", dest="srctable",
                        help="Select the table to output")
results = parser.parse_args()
    
    . . .

if results.srctable == "devices":
        table_abstraction = kismetdb.Devices(results.infile)
        column_names = ["first_time", "last_time", "devkey", "phyname",
                        "devmac", "strongest_signal", "min_lat", "min_lon",
                        "max_lat", "max_lon", "avg_lat", "avg_lon",
                        "bytes_data", "type"]
   
   . . .

with open(results.outfile, csv_file_mode) as csvfile:
        csvWriter = csv.DictWriter(csvfile, delimiter="\t",
                                   extrasaction="ignore",
                                   fieldnames=column_names)
        nrows = 0
        csvWriter.writeheader()
        for row in table_abstraction.yield_meta():
            csvWriter.writerow(row)
            nrows = nrows + 1

````