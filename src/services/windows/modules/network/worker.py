
from src.utils.basics import terminal
import re, sys, ctypes, winreg as reg, subprocess
from src.utils.terminal import win_run_command

def get_ping_average():
    try:
        print("Measuring ping superficially from Fortnite (Epic Games) as an example....")
        result = subprocess.run(["ping", "ping-nae.ds.on.epicgames.com", "-n", "10"], capture_output=True, text=True)
        times = re.findall(r'time=(\d+)ms', result.stdout)
        if times:
            times = list(map(int, times))
            return sum(times) / len(times)
        else:
            terminal("e", "No se pudieron obtener resultados de ping.")
            return None
    except Exception as e:
        terminal("e", f"Error executing ping: {e}")
        return None

# Set DNS and TCP priorities in ServiceProvider.
def set_service_provider_priorities():
    try:
        with reg.OpenKey(reg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\Tcpip\ServiceProvider", 0, reg.KEY_SET_VALUE) as key:
            reg.SetValueEx(key, "DnsPriority", 0, reg.REG_DWORD, 1)
            reg.SetValueEx(key, "HostsPriority", 0, reg.REG_DWORD, 1)
            reg.SetValueEx(key, "LocalPriority", 0, reg.REG_DWORD, 1)
            reg.SetValueEx(key, "NetbtPriority", 0, reg.REG_DWORD, 1)
        terminal("s", "DNS and TCP priorities set successfully.")
    except Exception as e: terminal("e", f"Error setting DNS and TCP priorities: {e}")

# Set TcpAckFrequency on each network interface.
def set_tcp_ack_frequency():
    interfaces_path = r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces"
    try:
        with reg.OpenKey(reg.HKEY_LOCAL_MACHINE, interfaces_path) as interfaces:
            for i in range(reg.QueryInfoKey(interfaces)[0]):
                interface_name = reg.EnumKey(interfaces, i)
                interface_path = f"{interfaces_path}\\{interface_name}"
                try:
                    with reg.OpenKey(reg.HKEY_LOCAL_MACHINE, interface_path, 0, reg.KEY_SET_VALUE) as key:
                        reg.SetValueEx(key, "TcpAckFrequency", 0, reg.REG_DWORD, 1)
                    terminal("s", f"TcpAckFrequency set to 1 for interface {interface_name}.")
                except Exception as e: terminal("e", f"Error setting TcpAckFrequency for interface {interface_name}: {e}")
    except Exception as e: terminal("e", f"Error accessing network interfaces: {e}")

def main():
    initial_ping = get_ping_average()
    if initial_ping is not None: terminal("s", f"Initial average ping: {initial_ping:.2f} ms")
    set_service_provider_priorities()
    set_tcp_ack_frequency()
    for command in [
            ["netsh", "int", "tcp", "set", "global", "autotuninglevel=disabled"],
            ["netsh", "interface", "ip", "set", "dns", "name=\"Ethernet\"", "static", "1.1.1.1"],
            ["netsh", "interface", "ip", "add", "dns", "name=\"Ethernet\"", "address=1.0.0.1", "index=2"]
        ]: win_run_command(command)
    
    final_ping = get_ping_average()
    if final_ping is not None:
        terminal("s", f"Final average ping: {final_ping:.2f} ms")
        if initial_ping is not None: terminal("s", f"Expected ping improvement in Fortnitet: {(initial_ping - final_ping):.2f} ms")
    terminal("s", "Network settings optimized. Please restart your computer for all changes to take effect.")