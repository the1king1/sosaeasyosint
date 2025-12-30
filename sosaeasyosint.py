import requests, socket, dns.resolver, whois, phonenumbers, re, sys
from phonenumbers import geocoder, carrier, timezone, number_type

# ================= BANNER =================
def banner():
    print("""
 ███████╗ ██████╗ ███████╗ █████╗ 
 ██╔════╝██╔═══██╗██╔════╝██╔══██╗
 ███████╗██║   ██║███████╗███████║
 ╚════██║██║   ██║╚════██║██╔══██║
 ███████║╚██████╔╝███████║██║  ██║
 ╚══════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝



        ك  FRAMEWORK v1سوسا العم ايدي 
""")

# ================= MENU =================
def menu():
    print("""
1  - IP Intelligence
2  - Domain / WHOIS
3  - DNS Records
4  - Port Scanner
5  - Subdomain Finder
6  - Email OSINT
7  - Phone OSINT
8  - Hash Analyzer
9  - Crypto Tracker (ETH)
0  - Exit
""")

# ================= IP =================
def ip_lookup():
    ip = input("IP > ")
    try:
        r = requests.get(f"https://ipinfo.io/{ip}/json").json()
        for k,v in r.items():
            print(f"{k}: {v}")
    except:
        print("Error fetching IP data")

# ================= DOMAIN =================
def domain_lookup():
    d = input("Domain > ")
    try:
        data = whois.whois(d)
        for k,v in data.items():
            print(f"{k}: {v}")
    except:
        print("WHOIS failed")

# ================= DNS =================
def dns_lookup():
    d = input("Domain > ")
    for rtype in ["A","AAAA","MX","NS","TXT"]:
        try:
            ans = dns.resolver.resolve(d, rtype)
            for r in ans:
                print(f"{rtype}: {r}")
        except:
            pass

# ================= PORT SCAN =================
def port_scan():
    t = input("IP / Domain > ")
    ports = [21,22,25,53,80,110,143,443,3306,3389,8080]
    for p in ports:
        try:
            s = socket.socket()
            s.settimeout(0.5)
            s.connect((t,p))
            print(f"Port {p}: OPEN")
            s.close()
        except:
            pass

# ================= SUBDOMAIN =================
def subdomain_scan():
    d = input("Domain > ")
    subs = ["www","mail","ftp","dev","test","api","admin","panel","cpanel"]
    for s in subs:
        sub = f"{s}.{d}"
        try:
            socket.gethostbyname(sub)
            print("FOUND:", sub)
        except:
            pass

# ================= EMAIL =================
def email_osint():
    e = input("Email > ")
    if not re.match(r"[^@]+@[^@]+\.[^@]+", e):
        print("Invalid email format")
        return

    domain = e.split("@")[-1]
    print("Format: VALID")

    try:
        mx = dns.resolver.resolve(domain, "MX")
        for r in mx:
            print("MX:", r.exchange)
    except:
        print("No MX records")

    providers = {
        "gmail.com":"Google",
        "outlook.com":"Microsoft",
        "yahoo.com":"Yahoo"
    }
    print("Provider:", providers.get(domain,"Unknown"))

# ================= PHONE =================
def phone_lookup():
    p = input("Phone (+..) > ")
    try:
        num = phonenumbers.parse(p)
        print("Valid:", phonenumbers.is_valid_number(num))
        print("Country:", geocoder.description_for_number(num,"en"))
        print("Carrier:", carrier.name_for_number(num,"en"))
        print("Timezones:", timezone.time_zones_for_number(num))
        print("Type:", number_type(num))
    except:
        print("Invalid phone number")

# ================= HASH =================
def hash_analyzer():
    h = input("Hash > ").lower()
    patterns = {
        "MD5": r"^[a-f0-9]{32}$",
        "SHA1": r"^[a-f0-9]{40}$",
        "SHA256": r"^[a-f0-9]{64}$",
        "SHA512": r"^[a-f0-9]{128}$"
    }
    for t,p in patterns.items():
        if re.match(p,h):
            print("Type:", t)
            print("Length:", len(h))
            return
    print("Unknown hash")

# ================= CRYPTO =================
def crypto_tracker():
    w = input("ETH Wallet > ")
    r = requests.get(f"https://api.blockcypher.com/v1/eth/main/addrs/{w}/balance")
    if r.status_code != 200:
        print("API Error")
        return
    d = r.json()
    print("Balance:", d["balance"]/1e18, "ETH")
    print("Transactions:", d["n_tx"])

# ================= MAIN =================
def main():
    banner()
    while True:
        menu()
        c = input("Select > ")

        if c=="1": ip_lookup()
        elif c=="2": domain_lookup()
        elif c=="3": dns_lookup()
        elif c=="4": port_scan()
        elif c=="5": subdomain_scan()
        elif c=="6": email_osint()
        elif c=="7": phone_lookup()
        elif c=="8": hash_analyzer()
        elif c=="9": crypto_tracker()
        elif c=="0":
            print("Bye")
            sys.exit()
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
