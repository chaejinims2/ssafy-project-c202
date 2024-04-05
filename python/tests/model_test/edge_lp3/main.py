
from edge_LP import NetworkManager
from my_main import EdgeLP

def main():
    edge_lp_config = {
        # "ip": "192.168.100.58", # kky
        "ip": "192.168.100.130", # icj
        "port": 3001,
        "baby_id": "1"
    }

    # Init NetworkManager
    network_manager = NetworkManager(**edge_lp_config)

    # Init EdgeLP : edge_lp.my_edge = { "network_manager", "sensor_data", "detector" }
    edge_lp = EdgeLP(network_manager)

    # # init for data collection
    edge_lp.start_data()


    while True:
        edge_lp.collect_data()


if __name__ == "__main__":
    main()