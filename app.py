from flask import Flask, jsonify, request, render_template
import logging

app = Flask(__name__)


# --- GPIO setup with a safe mock fallback (works on non-Pi machines) ---
PIN = 14

try:
    import RPi.GPIO as GPIO  # type: ignore
    HAS_GPIO = True
except Exception:
    HAS_GPIO = False

if not HAS_GPIO:
    # simple mock for local/dev environments
    class MockGPIO:
        BCM = 'BCM'
        OUT = 'OUT'
        HIGH = 1
        LOW = 0

        def __init__(self):
            self._mode = None
            self._states = {}

        def setmode(self, mode):
            self._mode = mode

        def setup(self, pin, mode):
            self._states[pin] = self.LOW

        def output(self, pin, value):
            self._states[pin] = value

        def input(self, pin):
            return self._states.get(pin, self.LOW)

        def cleanup(self):
            self._states.clear()

    GPIO = MockGPIO()

# initialize
try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN, GPIO.OUT)
    # ensure LED is off initially
    GPIO.output(PIN, GPIO.LOW)
except Exception:
    logging.exception('Failed to initialize GPIO; continuing in degraded mode')


@app.route('/')
def welcome():
    """Serve a small welcome page with a toggle for the LED on PIN 14."""
    return render_template('index.html', pin=PIN)


@app.route('/api')
def api_index():
    # preserve previous JSON root behavior at /api
    return jsonify(message="Hello from Sparki Flask app")


@app.route('/health')
def health():
    return jsonify(status="ok")


@app.route('/echo', methods=['POST'])
def echo():
    data = request.get_json(silent=True)
    return jsonify(received=data)


@app.route('/gpio/state')
def gpio_state():
    try:
        state = bool(GPIO.input(PIN))
    except Exception:
        state = False
    return jsonify(pin=PIN, state=state)


@app.route('/gpio/toggle', methods=['POST'])
def gpio_toggle():
    """Toggle or set the GPIO pin state.

    Accepts JSON { "state": true|false } to explicitly set state,
    otherwise toggles current state.
    """
    payload = request.get_json(silent=True) or {}
    try:
        current = bool(GPIO.input(PIN))
    except Exception:
        current = False

    if 'state' in payload:
        new_state = bool(payload['state'])
    else:
        new_state = not current

    try:
        GPIO.output(PIN, GPIO.HIGH if new_state else GPIO.LOW)
    except Exception:
        logging.exception('Failed to write GPIO')

    return jsonify(pin=PIN, state=new_state)


if __name__ == '__main__':
    # Runs on localhost:80 by default for local development
    app.run(host='127.0.0.1', port=80, debug=True)
