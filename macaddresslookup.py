#!/usr/bin/env python3
import argparse
import logging
import os
import re
import sys
import urllib.request
import json

logging.basicConfig(
    level=logging.WARN,
    format="%(levelname)s %(asctime)s %(message)s",
    handlers=[logging.FileHandler("macaddresslookup.log"), logging.StreamHandler()],
)


def validate_macaddress(mac_address):
    """Simple function to validate mac address
    
    :param mac_address: input MAC address
    :type mac_address: str
    :return: True if valid format
    :rtype: bool
    """
    return re.match("^([0-9A-Fa-f]{2}[:.-]?){5}([0-9A-Fa-f]{2})$", mac_address.strip())


def request_builder(mac_address, api_key):
    req_url = "https://api.macaddress.io/v1"
    query_params = {"output": "json", "search": mac_address}
    encoded_url = "{0}?{1}".format(req_url, urllib.parse.urlencode(query_params))
    auth_header = {"X-Authentication-Token": api_key}
    req = urllib.request.Request(encoded_url, headers=auth_header)
    return req


def request_sender(request):
    """Returns a string of response obtained from the request
    
    :param request: request URL object
    :type request: urllib.request.Request
    :return: response json output
    :rtype: string
    """
    try:
        response = urllib.request.urlopen(request)
        output = response.read().decode("utf-8")
        return output
    except urllib.error.HTTPError:
        logging.error(
            "status code:{0} message:{1}".format(response.status, response.msg)
        )
        exit(response.status)
    finally:
        response.close()


def recursive_key_lookup(inp_dict):
    for key, value in inp_dict.items():
        if type(value) is dict:
            yield (key)
            yield from recursive_key_lookup(value)
        else:
            yield (key)


def match_key(inp_dict, query_val):
    key_list = []
    for key in recursive_key_lookup(inp_dict):
        key_list.append(key)
    for key in key_list:
        if query_val.lower() in key.lower():
            return key
    return None


def recursive_val_lookup(key, inp_dict):
    if key in inp_dict:
        return inp_dict[key]
    for val in inp_dict.values():
        if isinstance(val, dict):
            nested_val = recursive_val_lookup(key, val)
            if nested_val is not None:
                return nested_val
    return None


def formatted_output(response, query_list, output_type):
    output_str = ""
    output_dict = {}
    try:
        response_dict = json.loads(response)
        for query in query_list:
            search_key = match_key(response_dict, query)
            if search_key is not None:
                search_val = recursive_val_lookup(search_key, response_dict)
                output_dict[query] = search_val
            else:
                output_dict[query] = None
    except ValueError as e:
        logging.error("Could not load JSON output to string.")
    if output_type == "json":
        output_str = json.dumps(output_dict)
    elif output_type == "csv":
        output_str = (
            ",".join(output_dict.keys())
            + "\n"
            + ",".join('"{0}"'.format(val) for val in output_dict.values())
        )
    else:
        if len(output_dict) == 1:
            output_str = next(iter(output_dict.values()))
        else:
            output_str = "\n".join(
                "{!s}={!s}".format(key, val) for (key, val) in output_dict.items()
            )
    return output_str


def main():
    """Main function
    """

    # Setup commandline parser
    parser = argparse.ArgumentParser(
        description="Query macaddress.io and fetch the vendor information associated with the mac address"
    )

    parser.add_argument("macaddr", type=str, help="MAC Address of the device")
    parser.add_argument(
        "-o",
        "--output",
        help="output format control, accepted values are json, csv, minimal",
        dest="output",
        default="minimal",
    )
    parser.add_argument(
        "-q",
        "--query",
        help="query fields, one or multiple comma seperated eg. name,transmission,valid,blockfound",
        dest="query",
        default="name",
    )
    parser.add_argument(
        "-r",
        "--rawjson",
        help="return raw json from the server that can be piped to jq for other fields",
        action="store_true",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="make output more verbose sets to DEBUG",
        action="store_true",
    )

    args = parser.parse_args()
    mac_address = args.macaddr
    query_fields = args.query
    output_type = args.output

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    try:
        api_key = os.environ["MACADDRESSIO_API_KEY"]
        if api_key == "":
            logging.error("Please set the environment variable MACADDRESSIO_API_KEY")
            sys.exit(1)
    except KeyError:
        logging.error("Please set the environment variable MACADDRESSIO_API_KEY")
        sys.exit(1)
    if not validate_macaddress(mac_address):
        logging.error("Could not validate mac_address")
        sys.exit(1)
    response = request_sender(request_builder(mac_address, api_key))
    if args.rawjson:
        print(response)
        sys.exit(0)
    query_list = [x.strip() for x in query_fields.split(",")]
    print(formatted_output(response, query_list, output_type))


if __name__ == "__main__":
    main()
