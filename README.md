
# 🌐 Ashans Cryptocurrency Protocol

**Ashans** is a privacy-first, fully encrypted blockchain protocol designed for secure peer-to-peer communication, rotating addresses, and a custom Proof-of-Work (PoW) consensus mechanism.

---

## 🔐 Key Features

- ✅ Node-to-node encrypted communication
- 🔁 Address rotation every 10–30 seconds
- 🧱 Custom encrypted blockchain message layer
- ⛏ Advanced PoW algorithm with difficulty tuning
- 🛰 Secret node routing (only previous node knows next hop)
- 🔁 Floating token address infrastructure
- 📜 Custom consensus implementation
- 🧪 CI/CD with GitHub Actions
- 🧾 Full contributor and documentation support

---

## ⚙️ Environment Setup

> Make sure you have **Python 3.11+** and **pip** installed.

### 📦 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/ashans.git
cd ashans
```

### 🧪 2. Create Virtual Environment (Optional)

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 📥 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> If `requirements.txt` is missing, install core tools like:
```bash
pip install cryptography flask pytest
```

### ⚡ 4. Set Up Environment

```bash
python setup_env.py
```

This script generates keys, sets initial config, and prepares node runtime files.

---

## 🚀 Running Ashans

### 🟢 Launch a Node

```bash
python run_node.py
```

Each node handles dynamic routing, peer communication, and participates in mining + consensus.

---

## 🧪 Testing

Run unit tests:

```bash
pytest tests/
```

---

## 🌍 Network Participation

You can create multiple nodes on different terminals/machines and allow them to auto-discover and route messages securely.

---

## 🤝 Contributing

We welcome pull requests and contributions! Check out:
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

---

## 📄 License

This project is licensed under the MIT License.

---

## 💬 Stay in Touch

Have questions or ideas? Start a GitHub Discussion or open an Issue!

---

Built with ❤️ for decentralized privacy.
