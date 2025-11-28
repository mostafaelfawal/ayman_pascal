"""Helper for listing serial ports.

Keep this module small and importable by the UI. It returns a list
of port names (e.g., COM3 or /dev/ttyUSB0) that can be used to populate
an options menu.
"""
import serial.tools.list_ports


def get_serial_ports():
    """Return a list of available serial port device names.

    If the serial library isn't available, return an empty list so the UI
    can still load and notify the user gracefully.
    """
    if serial is None:
        return []

    ports = serial.tools.list_ports.comports()
    return [p.device for p in ports]