import socket
import time

# 1. Configuration
PS5_IP = "192.XX.X.X"  # <--- DOUBLE CHECK THIS in PS5 Settings
PORT = 33740  # The 'Secret' GT7 Port
HEARTBEAT = b'A'  # The 'Wake Up' signal


def scout_ps5():
    # Create a UDP Socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5.0)  # Wait 5 seconds for a response

    print(f"Sending Heartbeat to {PS5_IP}:{PORT}...")

    try:
        # Send the 'Wake Up' signal
        sock.sendto(HEARTBEAT, (PS5_IP, PORT))

        # Listen for any return data
        data, addr = sock.recvfrom(2048)
        if data:
            print(f"SUCCESS! Received {len(data)} bytes from PS5.")
            print("Your M4 and PS5 are officially talking.")
    except socket.timeout:
        print("TIMEOUT: PS5 didn't answer. Is the game in a race?")
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        sock.close()


if __name__ == "__main__":
    scout_ps5()