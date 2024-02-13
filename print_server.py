from flask import Flask, request
import subprocess
app = Flask(__name__)

port=12345
usb_interface="lp0"

def wrap_text(text, line_length):
    wrapped_text = ""
    current_line = ""
    words = text.split()
    for word in words:
        if len(current_line) + len(word) <= line_length:
            current_line += word + " "
        else:
            wrapped_text += current_line.strip() + "\n"
            current_line = word + " "
    if current_line:
        wrapped_text += current_line.strip()
    return wrapped_text+"\x0A"

def print_to_usb_thermal_printer(text):
    try:
        # Wrap the text to fit the line length of the thermal printer
        wrapped_text = wrap_text(text, 32)  # Adjust line length as needed
        print(wrapped_text)
        # Open a pipe to /dev/usb/lp0 and write the text
        with subprocess.Popen(['tee', '/dev/usb/'+usb_interface], stdin=subprocess.PIPE) as proc:
            proc.communicate(input=wrapped_text.encode('utf-8'))
        print("Text printed successfully to USB thermal printer.")
    except subprocess.CalledProcessError as e:
        print("Error printing to USB thermal printer:", e)

@app.route('/print/<string:text>', methods=['GET'])
def print_text(text):
    print_to_usb_thermal_printer(text)
    return "Print command received and processed."

@app.route('/size/<int:size>', methods=['GET'])
def set_size(size):
    set_character_size(size)
    return "Character size set."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
