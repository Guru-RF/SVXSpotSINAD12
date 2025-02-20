# SVXSpotSINAD12

SVXSpotSINAD12 is a script designed to measure the **12 dB SINAD sensitivity** of a receiver using a signal generator. The script takes 5-second samples and provides real-time SINAD12 readings, helping you determine the receiver's sensitivity.

## Prerequisites

- A signal generator capable of **2.5 kHz deviation with a 1 kHz tone**
- A properly configured receiver
- A Linux-based environment

## Installation & Setup

1. **Configure the Frequency**
    - Run the configuration script:
      ```sh
      ./sinad_hotspot_config
      ```
    - If using **VHF**, edit the configuration file manually before proceeding.

2. **Set the Volume**
    - Run the volume calibration script:
      ```sh
      ./sinad_hotspot_volume
      ```

3. **Start SINAD Measurement**
    - Execute the main script:
      ```sh
      ./sinad.sh
      ```

## How It Works

- The script takes **5-second samples** from the configured frequency.
- It continuously reads out **SINAD12** values every **5 seconds**.
- You can **adjust the signal generator output power** during the test.
- When the **SINAD script reports 12 dB**, read the **output power** from your signal generator.
- The **generator output power at this point** is your **12 dB SINAD sensitivity**.

## Notes

- Ensure your signal generator is correctly set to **2.5 kHz deviation** and **1 kHz tone**.
- Make sure the receiver and generator are correctly aligned to the frequency set in the configuration.

## License

This project is released under the **MIT License**.

## Contributing

Pull requests and improvements are welcome! Open an issue for any questions or enhancements.

## Contact

For further inquiries, visit the [GitHub repository](https://github.com/Guru-RF/SVXSpotSINAD12).
