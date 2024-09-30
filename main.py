import argparse
import time
import requests
import subprocess
import platform
def is_pc_up(pc_address):
    """Check if the PC is up by pinging it."""
    try:
        if platform.system() == "Windows":
            subprocess.check_output(["ping", "-n", "1", pc_address])
        else:
            subprocess.check_output(["ping", "-c", "1", pc_address])
        return True
    except subprocess.CalledProcessError:
        return False

class JBLSpeaker:
    def __init__(self, address, port, pin):
        self.base_url = f"http://{address}:{port}/fsapi"
        self.pin = pin
        self.session_id = None

    def _get_session_id(self):
        response = requests.get(f"{self.base_url}/CREATE_SESSION?pin={self.pin}")
        if response.status_code == 200:
            self.session_id = response.text.split("<sessionId>")[1].split("</sessionId>")[0]

    def get_power_state(self):
        if not self.session_id:
            self._get_session_id()
        response = requests.get(f"{self.base_url}/GET/netRemote.sys.power?pin={self.pin}&sid={self.session_id}")
        if response.status_code == 200:
            return int(response.text.split("<value>")[1].split("</value>")[0])
        return None

    def set_power_state(self, state):
        if not self.session_id:
            self._get_session_id()
        response = requests.get(f"{self.base_url}/SET/netRemote.sys.power?pin={self.pin}&sid={self.session_id}&value={state}")
        return response.status_code == 200

    def get_play_state(self):
        if not self.session_id:
            self._get_session_id()
        response = requests.get(f"{self.base_url}/GET/netRemote.play.control?pin={self.pin}&sid={self.session_id}")
        if response.status_code == 200:
            return int(response.text.split("<u8>")[1].split("</u8>")[0])
        return None

    def set_play_state(self, state):
        if not self.session_id:
            self._get_session_id()
        response = requests.get(f"{self.base_url}/SET/netRemote.play.control?pin={self.pin}&sid={self.session_id}&value={state}")
        return response.status_code == 200

def keep_jbl_up(args):
    """Main function to keep the JBL speaker up."""
    jbl = JBLSpeaker(args.jbl_address, args.jbl_port, args.jbl_pin)
    
    while True:
        try:
            if args.pc_address == None or is_pc_up(args.pc_address):
                # Send keep alive request to the speaker
                if args.use_play_state:
                    if jbl.set_play_state(jbl.get_play_state()):
                        print("JBL speaker turned on")
                    else:
                        print("Failed to turn on JBL speaker")
                else:
                    if jbl.set_power_state(1):
                        print("JBL speaker turned on")
                    else:
                        print("Failed to turn on JBL speaker")
            elif args.turn_off:
                # Turn off the speaker
                if jbl.set_power_state(0):
                    print("JBL speaker turned off")
                else:
                    print("Failed to turn off JBL speaker")
        except Exception as e:
            print(f"Error communicating with JBL speaker: {e}")
       
        time.sleep(args.interval)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Keep JBL speaker on.")
    parser.add_argument("--pc-address", type=str, help="IP address of the PC", default=None)
    parser.add_argument("--jbl-address", type=str, help="IP address of the JBL speaker", required=True)
    parser.add_argument("--jbl-port", type=str, help="Port of the JBL speaker", default=80)
    parser.add_argument("--jbl-pin", type=str, help="PIN of the JBL speaker", default=1234)
    parser.add_argument("--interval", type=int, help="Interval to send keep alive requests", default=60)
    parser.add_argument("--use-play-state", help="Use play state to turn on/off the JBL speaker", action="store_true")
    parser.add_argument("--turn-off", help="Turn off the JBL speaker when PC is off", action="store_true")

    args = parser.parse_args()
    keep_jbl_up(args)
