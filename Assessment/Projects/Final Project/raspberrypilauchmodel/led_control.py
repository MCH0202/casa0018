import subprocess
import threading
import queue
import time
import re
import RPi.GPIO as GPIO

# Set GPIO pins
LED_PINS = {
    'can': 17,         # yellow LED
    'cardboard': 27,   # blue LED
    'glassbottle': 22  # green LED
}


GPIO.setmode(GPIO.BCM)
for pin in LED_PINS.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)


last_detected = None
last_time = time.time()
counter = 0
lock = threading.Lock()

# light up LED after classication 
current_led = None

def led_on(label):
    global current_led
    if current_led:
        GPIO.output(current_led, GPIO.LOW)
    if label in LED_PINS:
        GPIO.output(LED_PINS[label], GPIO.HIGH)
        current_led = LED_PINS[label]

def led_off():
    global current_led
    if current_led:
        GPIO.output(current_led, GPIO.LOW)
        current_led = None

def monitor_runner(q):
    global last_detected, last_time, counter
    while True:
        line = q.get()
        if line is None:
            break
        if 'classifyRes' in line:
            try:
                start = line.index('{')
                end = line.index('}')
                result_str = line[start:end+1]
                
                matches = re.findall(r"(\w+):\s'([0-9.]+)'", result_str)
                
                result = {label:float(score) for label, score in matches}
                
                best_label = max(result, key=lambda k: float(result[k]))
                best_score = float(result[best_label])
                #print(f"[DEBUG] {best_label}: {best_score}")
                with lock:
                    if best_score > 0.7:
                        if best_label == last_detected:
                            counter += 1
                        else:
                            last_detected = best_label
                            counter = 1
                        last_time = time.time()

                        if counter >= 5:
                            led_on(best_label)
                    else:
                        last_detected = None
                        counter = 0
            except Exception as e:
                print(f"[WARN] Failed to parse classifyRes: {e}")

print("[INFO] start Edge Impulse runner...")
runner = subprocess.Popen(
    ['edge-impulse-linux-runner --model "garbage-classification-linux-aarch64-v1.eim"'],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1
)

q = queue.Queue()
thread = threading.Thread(target=monitor_runner, args=(q,))
thread.start()

try:
    while True:
        line = runner.stdout.readline()
        if line == '' and runner.poll() is not None:
            break
        if line:
            print(line.strip())
            q.put(line.strip())

        # turn off led if overtime 
        with lock:
            if current_led and time.time() - last_time > 5:
                led_off()

except KeyboardInterrupt:
    print("[INFO] interrupted, turn off LED...")
finally:
    runner.terminate()
    q.put(None)
    thread.join()
    GPIO.cleanup()