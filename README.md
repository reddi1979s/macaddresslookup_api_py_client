# MAC Address Vendor lookup CLI

This simple python script can be used to query [https://macaddress.io/](https://macaddress.io/) to get vendor related information about a device MAC Address

## Getting Started

This scripting utility has be written using the standard library included in python 3.x All you need to get started is sign up for an account [here](https://macaddress.io/signup) and obtain your API key.

### Prerequisites

You need a standard installation of Python3 that can be obtained [here](https://www.python.org/downloads/)

### Usage

Export the API key as an environment variable `MACADDRESSIO_API_KEY` before running the script

On linux and MacOS

Example:

```bash
export MACADDRESSIO_API_KEY=at_VKIvhPfcPffhywNDMx61r0E1gAhKW
```

Note the above string is a randomly generated value and if you copy paste this exactly it will result in `"error": "Access restricted. Enter the correct API key."`

And then simply run

```bash
./mac_vendor.py -m "E8404079C860"
```

This should give output of the company name. For the above example it would show:

```bash
Cisco Systems, Inc
```

You can control the output format and values to fetch. By default it only fetches the name of vendor. You can check the usage for more details.

**NOTE** The script does partial matches of the query value as well. So, if the JSON object key is companyName a shorthand unique string name for query should also return a match. If it's not unique the program would return the first match found. And if none found it would return None.

```text
usage: mac_vendor.py [-h] [-o OUTPUT] [-q QUERY] [-r] [-v] macaddr

Query macaddress.io and fetch the vendor information associated with the mac address

positional arguments:
  macaddr               MAC Address of the device

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output format control, accepted values are json, csv,minimal
  -q QUERY, --query QUERY
                        query fields, one or multiple comma seperated eg. name,transmission,valid,blockfound
  -r, --rawjson         return raw json from the server that can be piped to jq for other fields
  -v, --verbose         make output more verbose sets to DEBUG
```

### Examples

`./mac_vendor.py E8:40:40:79:C8:60 -r`

Output:

```json
{"vendorDetails":{"oui":"E84040","isPrivate":false,"companyName":"Cisco Systems, Inc","companyAddress":"80 West Tasman Drive San Jose CA 94568 US","countryCode":"US"},"blockDetails":{"blockFound":true,"borderLeft":"E84040000000","borderRight":"E84040FFFFFF","blockSize":16777216,"assignmentBlockSize":"MA-L","dateCreated":"2011-03-17","dateUpdated":"2015-09-27"},"macAddressDetails":{"searchTerm":"E8:40:40:79:C8:60","isValid":true,"virtualMachine":"Not detected","applications":[],"transmissionType":"unicast","administrationType":"UAA","wiresharkNotes":"No details","comment":""}}
```

`./mac_vendor.py E8:40:40:79:C8:60 --query "name,valid"`

Output:

```text
name="Cisco Systems, Inc"
valid="True"
```

`./mac_vendor.py E8:40:40:79:C8:60 --query "name,valid" --output csv`

Output:

```text
name,valid
"Cisco Systems, Inc","True"
```

### Code formatting

Code formatting has be done using [black](https://github.com/psf/black). I really like the philosophy of `gofmt` on which black is based.

## Running with Docker

For your convenience a Dockerfile has also been provided along with the code.

 docker run --env MACADDRESSIO_API_KEY=key <image_name> mac_vendor.py <MAC_ADDRESS> <OPTIONAL_PARAMS>

Either build it yourself or you can use the one below:

 Example:

```bash
docker run --env MACADDRESSIO_API_KEY=$MY_API_KEY balwa/macaddress-python-client:latest mac_vendor.py E8-40-40-79-C8-60
```

## Security

While the docker image build process does have an optional argument to bake the `MACADDRESSIO_API_KEY` key with the build process, it's a bad idea to use it non-local environments. This is only meant for image build on your local machine.

Also, relaying on MAC address vendor information to detect anomalous devices in your network by itself isn't a complete security guarantee. An attacker can easily alter the MAC address of their machine to match the  trusted MAC address value. Do consider enabling other security features like DHCP snooping to reduce the  surface for Man in the Middle attacks.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
