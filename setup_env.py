import os

ENV_FILE = ".env"

default_env = {
    "NODE_PORT": "5000",
    "NETWORK_ID": "shadownet",
    "DIFFICULTY": "5",
    "FLOATING_ADDRESS_INTERVAL": "10",  # in seconds
    "ADDRESS_ROTATION_INTERVAL": "30",  # in seconds
}

def create_env_file():
    if os.path.exists(ENV_FILE):
        print(f"{ENV_FILE} already exists.")
        return

    with open(ENV_FILE, "w") as f:
        for key, value in default_env.items():
            f.write(f"{key}={value}\n")
    print(f"{ENV_FILE} created with default values.")

if __name__ == "__main__":
    create_env_file()
