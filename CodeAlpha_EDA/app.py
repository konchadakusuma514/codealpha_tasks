import http.server
import socketserver
import os
import sys

# ==============================================================================
# CYBERSHIELD SOC ANALYTICS - PURE PYTHON WEB SERVER (NO STREAMLIT)
# ==============================================================================
PORT = 5000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, "website")

if not os.path.exists(WEB_DIR):
    WEB_DIR = BASE_DIR

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def log_message(self, format, *args):
        # Keep terminal output clean
        pass

def main():
    target_port = PORT
    socketserver.TCPServer.allow_reuse_address = True
    
    httpd = None
    for p in range(5000, 5015):
        try:
            httpd = socketserver.TCPServer(("", p), QuietHandler)
            target_port = p
            break
        except OSError:
            continue
            
    if httpd is None:
        print("[!] Error: All ports 5000-5015 are busy.")
        sys.exit(1)

    url = f"http://localhost:{target_port}/index.html"
    ip_url = f"http://127.0.0.1:{target_port}/index.html"
    
    print("\n" + "=" * 70)
    print("  🛡️  CYBERSHIELD SOC ANALYTICS & THREAT INTELLIGENCE PLATFORM")
    print("  Task 2: Global Cybersecurity Exploratory Data Analysis (EDA)")
    print("=" * 70)
    print("\n  ✅ Web Server is LIVE and RUNNING!")
    print("\n  👉 COPY & OPEN THIS URL IN GOOGLE CHROME:")
    print(f"     🔗 {url}")
    print(f"     🔗 {ip_url}")
    print("\n  ⚡ Features Enabled:")
    print("     ✔ Clean Light Mode (Default) + Dark Mode Toggle")
    print("     ✔ Moving Video-Style Interactive Threat Broadcast Feed")
    print("     ✔ Head-to-Head Sector Threat Comparison Tool")
    print("     ✔ Global Interactive Choropleth Loss Map")
    print("     ✔ ANOVA & Chi-Square Hypothesis Testing")
    print("     ✔ Predictive Breach Loss & Downtime Simulator")
    print("\n  Press CTRL+C in this terminal to stop the server.")
    print("=" * 70 + "\n")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[+] CyberShield server stopped successfully.")
        sys.exit(0)

if __name__ == "__main__":
    main()