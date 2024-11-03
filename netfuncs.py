import sys
import json

def ipv4_to_value(ipv4_addr):

    octets = map(int, ipv4_addr.split('.'))
    return sum(octet << (8 * (3 - i)) for i, octet in enumerate(octets))


def value_to_ipv4(addr):

    return '.'.join(str((addr >> (8 * (3 - i))) & 0xFF) for i in range(4))


def get_subnet_mask_value(slash):

    prefix_length = int(slash.strip('/'))
    mask = (1 << 32) - (1 << (32 - prefix_length))
    return mask


def ips_same_subnet(ip1, ip2, slash):

    ipval1 = ipv4_to_value(ip1)
    ipval2 = ipv4_to_value(ip2)
    netmask = get_subnet_mask_value(slash)
    return (get_network(ipval1, netmask)) == (get_network(ipval2, netmask))


def get_network(ip_value, netmask):

    return ip_value & netmask


def find_router_for_ip(routers, ip):

    for router_ip, router_info in routers.items():
        if ips_same_subnet(ip, router_ip, router_info["netmask"]):
            return router_ip
    return None

   

# Uncomment this code to have it run instead of the real main.
# Be sure to comment it back out before you submit!

# def my_tests():
#     print("-------------------------------------")
#     print("This is the result of my custom tests")
#     print("-------------------------------------")

#     print(ipv4_to_value("1.2.3.4"))
#     print(value_to_ipv4(4294901760))
#     print(get_subnet_mask_value("/24"))
#     print(ips_same_subnet("10.34.0.0", "10.34.166.254", "/24")) 


## -------------------------------------------
## Do not modify below this line
##
## But do read it so you know what it's doing!
## -------------------------------------------

def usage():
    print("usage: netfuncs.py infile.json", file=sys.stderr)

def read_routers(file_name):
    with open(file_name) as fp:
        json_data = fp.read()
        
    return json.loads(json_data)

def print_routers(routers):
    print("Routers:")

    routers_list = sorted(routers.keys())

    for router_ip in routers_list:

        # Get the netmask
        slash_mask = routers[router_ip]["netmask"]
        netmask_value = get_subnet_mask_value(slash_mask)
        netmask = value_to_ipv4(netmask_value)

        # Get the network number
        router_ip_value = ipv4_to_value(router_ip)
        network_value = get_network(router_ip_value, netmask_value)
        network_ip = value_to_ipv4(network_value)

        print(f" {router_ip:>15s}: netmask {netmask}: " \
            f"network {network_ip}")

def print_same_subnets(src_dest_pairs):
    print("IP Pairs:")

    src_dest_pairs_list = sorted(src_dest_pairs)

    for src_ip, dest_ip in src_dest_pairs_list:
        print(f" {src_ip:>15s} {dest_ip:>15s}: ", end="")

        if ips_same_subnet(src_ip, dest_ip, "/24"):
            print("same subnet")
        else:
            print("different subnets")

def print_ip_routers(routers, src_dest_pairs):
    print("Routers and corresponding IPs:")

    all_ips = sorted(set([i for pair in src_dest_pairs for i in pair]))

    router_host_map = {}

    for ip in all_ips:
        router = str(find_router_for_ip(routers, ip))
        
        if router not in router_host_map:
            router_host_map[router] = []

        router_host_map[router].append(ip)

    for router_ip in sorted(router_host_map.keys()):
        print(f" {router_ip:>15s}: {router_host_map[router_ip]}")

def main(argv):
    if "my_tests" in globals() and callable(my_tests):
        my_tests()
        return 0

    try:
        router_file_name = argv[1]
    except:
        usage()
        return 1

    json_data = read_routers(router_file_name)

    routers = json_data["routers"]
    src_dest_pairs = json_data["src-dest"]

    print_routers(routers)
    print()
    print_same_subnets(src_dest_pairs)
    print()
    print_ip_routers(routers, src_dest_pairs)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
    
