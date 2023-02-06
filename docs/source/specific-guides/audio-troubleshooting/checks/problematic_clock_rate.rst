Check for problematic clock rate
======================================
Be mindful with combination of sampling rate and ptime that causes non-whole number of samples,
such as:

- 10ms of 22050 Hz (220.5 samples), 
- 20ms of 11025 Hz (also 220.5 samples).
