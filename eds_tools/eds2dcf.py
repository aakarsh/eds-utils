import sys
import argparse

from .core import str2int
from .core.file_io.read_eds import read_eds
from .core.file_io.write_eds import write_eds

EDS2DCF_DESCRIPTION = 'EDS to DCF CLI tool'


def eds2dcf(sys_args=None):
    if sys_args is None:
        sys_args = sys.argv[1:]

    name = 'eds2dcf'
    parser = argparse.ArgumentParser(description=EDS2DCF_DESCRIPTION, prog=name)
    parser.add_argument('filepath', metavar='FILEPATH', help='filepath to EDS file')
    parser.add_argument('node_id', help='set the node ID')
    parser.add_argument('node_name', help='set the node name')
    parser.add_argument('-b', '--baud-rate', type=int, default=1000,
                        help='set the baud rate (in kbps)')
    parser.add_argument('-j', '--net-number', type=int, default=0, help='set the net number')
    parser.add_argument('-k', '--network-name', default='', help='set the network name')
    parser.add_argument('-m', '--canopen-manager', action='store_true',
                        help='set a CANopen manager')
    parser.add_argument('-l', '--lss-serial-number', type=int, default=0,
                        help='set the LSS serial number')
    parser.add_argument('-o', '--output', default='', help='output file path')
    args = parser.parse_args(sys_args)

    eds, errors = read_eds(args.filepath)

    eds.device_commissioning.node_id = str2int(args.node_id)
    eds.device_commissioning.node_name = args.node_name
    eds.device_commissioning.baud_rate = args.baud_rate
    eds.device_commissioning.net_number = args.net_number
    eds.device_commissioning.network_name = args.network_name
    eds.device_commissioning.canopen_manager = args.canopen_manager
    eds.device_commissioning.lss_serialnumber = args.lss_serial_number

    if args.output:
        write_eds(eds, file_path=args.output, dcf=True)
    else:
        write_eds(eds, dcf=True)
