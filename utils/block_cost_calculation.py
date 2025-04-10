def calculate_ashans_value(data_bytes: bytes, ashans_value_usd=10.0):
    size_mb = len(data_bytes) / (1024 * 1024)
    print(size_mb)
    usd_per_mb = 0.00001  # Average cloud storage cost
    cost_usd = size_mb * usd_per_mb
    ashans_per_usd = 1 / ashans_value_usd
    ashans_cost = cost_usd * ashans_per_usd
    return round(ashans_cost, 8), round(size_mb, 6)