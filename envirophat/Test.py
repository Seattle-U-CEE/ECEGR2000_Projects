import threading
import queue
import time
import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
# Import the envirophat light module
from envirophat import light
import colorsys # To convert RGB to HSV

# --- Data Structures ---
# Queue for thread-safe data transfer
raw_color_queue = queue.Queue()

# List to store processed color data (e.g., historical RGB and HSV values)
processed_color_data = []
processed_data_lock = threading.Lock() # Lock for thread-safe access

# --- Configuration ---
# Set the desired sampling interval (in seconds)
sampling_interval = 0.5 # Read color data relatively frequently

# --- Threads ---

def data_acquisition_thread(color_queue):
    """
    Acquires color sensor data, timestamps it, and puts it in the queue.
    """
    print("Color data acquisition thread started")
    while True:
        try:
            # --- Acquire Color Sensor Data using Enviro pHAT ---
            # Use envirophat.light.rgb() to get RGB values
            r, g, b = light.rgb()

            # Get timestamp
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Store raw data with meaningful information
            raw_data = {
                "timestamp": timestamp,
                "r": r,
                "g": g,
                "b": b,
            }

            # Put raw data into the queue for processing
            color_queue.put(raw_data)
            # print(f"Acquired color data: R:{r}, G:{g}, B:{b}") # Optional: for debugging

            # Wait before acquiring next data
            time.sleep(sampling_interval)

        except Exception as e:
            print(f"Error in data acquisition: {e}")
            break  # Exit loop on error


def data_processing_thread(color_queue, processed_data_list, lock):
    """
    Retrieves color data from the queue, processes it, and stores it.
    """
    print("Color data processing thread started")
    while True:
        try:
            # Get data from the queue (blocks until data is available)
            raw_data = color_queue.get()

            # --- Data Processing: Convert RGB to HSV and store ---
            r = raw_data["r"]
            g = raw_data["g"]
            b = raw_data["b"]

            # Convert RGB (0-255 range) to HSV (0-1 range for colorsys)
            hsv = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)

            # Store processed data (using a lock for thread safety)
            processed_color = {
                "timestamp": raw_data["timestamp"],
                "r": r,
                "g": g,
                "b": b,
                "h": hsv[0],  # Hue
                "s": hsv[1],  # Saturation
                "v": hsv[2],  # Value
            }

            with lock:
                processed_data_list.append(processed_color)
                # Keep the list size manageable for plotting
                if len(processed_data_list) > 50: # Adjust buffer size as needed
                    processed_data_list.pop(0)

            # print(f"Processed color data: {processed_color}") # Optional: for debugging

            # Mark the task as done for the queue
            color_queue.task_done()

        except queue.Empty:
            # Queue is empty, wait a bit
            time.sleep(0.1)
        except Exception as e:
            print(f"Error in data processing: {e}")
            break  # Exit loop on error


def data_presentation_thread(processed_data_list, lock):
    """
    Retrieves processed data and presents it (plotting color changes).
    """
    print("Color data presentation thread started")

    # Setup the plot
    fig, ax = plt.subplots()
    ax.set_xlabel("Time")
    ax.set_ylabel("Value")
    ax.set_title("Real-time Color Tracking (RGB and HSV)")
    ax.set_ylim(0, 1) # Adjust y-axis limits for HSV values (0-1 range) or keep 0-255 for RGB

    # Initialize empty lines for plotting RGB and HSV values
    line_r, = ax.plot([], [], 'r-', label='Red (0-255)')
    line_g, = ax.plot([], [], 'g-', label='Green (0-255)')
    line_b, = ax.plot([], [], 'b-', label='Blue (0-255)')
    line_h, = ax.plot([], [], 'c-', label='Hue (0-1)') # Using cyan for Hue
    line_s, = ax.plot([], [], 'm-', label='Saturation (0-1)') # Using magenta for Saturation
    line_v, = ax.plot([], [], 'y-', label='Value (0-1)') # Using yellow for Value


    # Add a legend
    ax.legend()

    # Function to update the plot
    def update_plot(frame):
        with lock:
            if processed_data_list:
                timestamps = [item["timestamp"] for item in processed_data_list]
                r_values = [item["r"] for item in processed_data_list]
                g_values = [item["g"] for item in processed_data_list]
                b_values = [item["b"] for item in processed_data_list]
                h_values = [item["h"] for item in processed_data_list]
                s_values = [item["s"] for item in processed_data_list]
                v_values = [item["v"] for item in processed_data_list]

                # Update the data for the lines
                line_r.set_data(timestamps, r_values)
                line_g.set_data(timestamps, g_values)
                line_b.set_data(timestamps, b_values)
                line_h.set_data(timestamps, h_values)
                line_s.set_data(timestamps, s_values)
                line_v.set_data(timestamps, v_values)


                # Autoscale the x-axis for better viewing
                ax.relim()
                ax.autoscale_view()

                # Rotate x-axis labels for better readability
                plt.xticks(rotation=45, ha='right')

        return line_r, line_g, line_b, line_h, line_s, line_v # Return the updated lines

    # Create the animation
    ani = animation.FuncAnimation(fig, update_plot, interval=500) # Update plot every 500ms

    # Show the plot
    plt.tight_layout() # Adjust layout to prevent labels overlapping
    plt.show()


# --- Main Execution ---

if __name__ == "__main__":
    # Create threads
    acquisition_thread = threading.Thread(
        target=data_acquisition_thread, args=(raw_color_queue,)
    )
    processing_thread = threading.Thread(
        target=data_processing_thread,
        args=(raw_color_queue, processed_color_data, processed_data_lock),
    )
    presentation_thread = threading.Thread(
        target=data_presentation_thread, args=(processed_color_data, processed_data_lock)
    )

    # Start threads
    acquisition_thread.start()
    processing_thread.start()
    presentation_thread.start()

    # Keep the main thread alive so the other threads can continue running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping threads...")
        # You could add a mechanism here to signal the threads to exit gracefully
        pass

    print("Main thread finished")
