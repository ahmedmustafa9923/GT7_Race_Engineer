import time
import csv
from gt_telem import TurismoClient

PS5_IP = "192.XXX.X.X"  # Your PS5 IP


def run_race_engineer():
    tc = TurismoClient(heartbeat_type="B")
    tc.playstation_ip = PS5_IP
    tc.start()

    # This list will hold our "Memory" before we save it
    data_log = []

    print(f"RECORDER READY. Drive a few laps, then press Ctrl+C to SAVE.")

    try:
        while True:
            t = tc.telemetry
            if t and t.speed_mps > 0.1:
                # 1. Collect the raw data
                current_frame = {
                    'speed': getattr(t, 'speed_mps', 0) * 3.6,
                    'throttle': (getattr(t, 'throttle', 0) / 255) * 100,
                    'brake': (getattr(t, 'brake', 0) / 255) * 100,
                    'gear': getattr(t, 'current_gear', 0),
                    # The library likely uses 'engine_rpm' or 'engine_speed'
                    'rpm': getattr(t, 'engine_rpm', getattr(t, 'rpm', 0))
                }
                # 2. Add to our memory list
                data_log.append(current_frame)

                print(f"RECORDING: {len(data_log)} frames captured | Speed: {current_frame['speed']:.1f}", end="\r")

            time.sleep(1 / 60)

    except KeyboardInterrupt:
        print(f"\n[STOP] Saving {len(data_log)} rows of data...")

        # 3. Write the data to a CSV file in your PyCharm folder
        keys = data_log[0].keys() if data_log else []
        if keys:
            with open('gt7_lap_data.csv', 'w', newline='') as output_file:
                dict_writer = csv.DictWriter(output_file, fieldnames=keys)
                dict_writer.writeheader()
                dict_writer.writerows(data_log)
            print("Successfully saved to: gt7_lap_data.csv")

    finally:
        tc.stop()


if __name__ == "__main__":
    run_race_engineer()