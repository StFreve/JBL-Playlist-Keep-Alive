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

    def __del__(self):
        if self.session_id:
            self._delete_session()
            self.session_id = None

    def _get_session_id(self):
        response = requests.get(f"{self.base_url}/CREATE_SESSION?pin={self.pin}")
        if response.status_code == 200:
            self.session_id = response.text.split("<sessionId>")[1].split("</sessionId>")[0]
    
    def _delete_session(self):
        requests.get(f"{self.base_url}/DELETE_SESSION?pin={self.pin}&sid={self.session_id}")
    
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

    def get_play_status(self):
        if not self.session_id:
            self._get_session_id()
        response = requests.get(f"{self.base_url}/GET/netRemote.play.status?pin={self.pin}&sid={self.session_id}")
        if response.status_code == 200:
            return int(response.text.split("<u8>")[1].split("</u8>")[0])
        return None
    
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

    def get_play_info_duration(self):
        if not self.session_id:
            self._get_session_id()
        response = requests.get(f"{self.base_url}/GET/netRemote.play.info.duration?pin={self.pin}&sid={self.session_id}")
        if response.status_code == 200:
            return int(response.text.split("<u32>")[1].split("</u32>")[0])
        return None

    def get_mode(self):
        if not self.session_id:
            self._get_session_id()
        response = requests.get(f"{self.base_url}/GET/netRemote.sys.mode?pin={self.pin}&sid={self.session_id}")
        if response.status_code == 200:
            return int(response.text.split("<u32>")[1].split("</u32>")[0])
        return None
    
    def set_mode(self, mode):
        if not self.session_id:
            self._get_session_id()
        response = requests.get(f"{self.base_url}/SET/netRemote.sys.mode?pin={self.pin}&sid={self.session_id}&value={mode}")
        return response.status_code == 200

    def send_keep_alive_request(self):
        if self.get_mode() != 1 and self.get_play_status() == 0 and self.get_play_info_duration() != 0:
            # Speaker is in non-Bluetooth/Aux Mode, but playing music through cable
            # If we try to set play state to 2 (pause) - it will cause music to start playing
            # So we need to set the speaker to Bluetooth/Aux Mode first
            if not self.set_mode(1):
                print("Failed to set self speaker to Bluetooh/Aux Mode")
                return False
            print("Speaker set Bluetooh/Aux Mode")
        
        if (self.get_mode() == 1 and self.get_play_status() == 2) or self.get_play_info_duration() == 0:
            # If we are in Bluetooth/Aux mode and nothing is playing through Bluetooth we can just set play state to 2 (pause)
            # to keep the speaker on
            if not self.set_play_state(2):
                print("Failed to set play state to 2 (pause)")
                return False
            print("Set play state to 2 (pause)")
        else:
            print("Speaker is in Wireless Mode and playing music")
            return False
        
        return True

def keep_jbl_up(args):
    """Main function to keep the JBL speaker up."""
    jbl = JBLSpeaker(args.jbl_address, args.jbl_port, args.jbl_pin)
    
    while True:
        try:
            if args.pc_address == None or is_pc_up(args.pc_address):
                # Send keep alive request to the speaker
                if jbl.send_keep_alive_request():
                    print("Keep Alive Request Sent")
                else:
                    print("Failed to send keep alive request to JBL speaker")
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

    args = parser.parse_args()
    keep_jbl_up(args)
