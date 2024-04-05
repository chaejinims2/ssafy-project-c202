from edge_LP import NetworkManager
from my_main import EdgeLP
import pkg_resources

mediapipe_version = pkg_resources.get_distribution("mediapipe").version

def main():
    """
    The main function initializes the NetworkManager and EdgeLP classes and starts the data collection process.
    """

    # Configuration for NetworkManager
    edge_lp_config = {
        "ip": "192.168.0.3", #  icj - home
        "port": 8083,  # Server Port
        "baby_id": 1  # Baby ID
    }

    # Initialize NetworkManager with the given configuration
    # NetworkManager is responsible for managing the network connections and sending data to the server.
    network_manager = NetworkManager(**edge_lp_config)

    # Initialize EdgeLP with the NetworkManager instance
    # EdgeLP is vd                                                                                                                                                                                                                                                  responsible for managing the data collection process.
    edge_lp = EdgeLP(network_manager)

    # Start data collection
    # This method initializes the data collection process.
    edge_lp.start_data()

    # Continuously collect data
    # This loop continuously collects data and sends it to the server.
    while True:
        edge_lp.collect_data()

if __name__ == "__main__":
    """
    This condition ensures that the main function is only executed when this script is run directly, 
    and not when it's imported as a module in another script.
    """
    main()