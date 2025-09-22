#!/usr/bin/env python3
import time, random, datetime, os

# Path relative to project root (this will create logs\auth_sim.log on Windows)
OUTFILE = os.path.join(os.path.dirname(__file__), "auth_sim.log")

users = ["alice","bob","carol","dave"]
ips = ["10.0.0.{}".format(i) for i in range(2,50)]
ports = [22,2222,2200,8022]

def nowts():
    # Use UTC ISO format so Logstash date filter matches
    return datetime.datetime.utcnow().isoformat()

def write_line(line):
    # Append a single line (with newline)
    with open(OUTFILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def simulate_normal():
    user = random.choice(users)
    ip = random.choice(ips)
    p = random.choice(ports)
    line = f"{nowts()} sshd: Accepted password for {user} from {ip} port {p}"
    write_line(line)

def simulate_failed(ip=None, user=None):
    if ip is None: ip = random.choice(ips)
    if user is None: user = random.choice(users)
    p = random.choice(ports)
    line = f"{nowts()} sshd: Failed password for {user} from {ip} port {p}"
    write_line(line)

def simulate_bruteforce(target_ip):
    # many failed attempts quickly
    for _ in range(random.randint(6,12)):
        simulate_failed(ip=target_ip)
        time.sleep(random.uniform(0.2,0.6))

if __name__ == "__main__":
    # Ensure logs directory exists (should already exist)
    os.makedirs(os.path.dirname(OUTFILE), exist_ok=True)

    # Clear logfile so each run is easy to inspect
    open(OUTFILE,"w", encoding="utf-8").close()

    # baseline noise
    for _ in range(30):
        if random.random() < 0.15:
            simulate_failed()
        else:
            simulate_normal()
        time.sleep(0.05)

    bf_ip = random.choice(ips)
    print("Simulating brute force from", bf_ip)
    simulate_bruteforce(bf_ip)

    # tail noise
    for _ in range(50):
        if random.random() < 0.1:
            simulate_failed()
        else:
            simulate_normal()
        time.sleep(0.1)

    print("Done. Log file written to:", OUTFILE)
