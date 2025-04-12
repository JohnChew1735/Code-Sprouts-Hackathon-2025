# Default params parsed
def get_common_config():
    print("Please provide the following parameters:")
    limit = input("Limit (default 100000): ") or "100000"
    start_time = input("Start Time (timestamp in ms, e.g., 1583020800000): ") or "1583020800000"
    window = input("Window (e.g., hour, day): ") or "hour"

    return {
        "limit": int(limit),
        "start_time": start_time,
        "window": window
    }

# As more endpoint are added, add more config based on the params needed
def get_open_interest_config():
    config = get_common_config()
    exchange = input("Exchange (default binance): ") or "binance"
    config["exchange"] = exchange
    return config

def get_addresses_count_config():
    return get_common_config()

def get_price_config():
    config = get_common_config()
    exchange = input("Exchange (default binance): ") or "binance"
    config["exchange"] = exchange
    return config


