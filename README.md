# 🎵 Music-Reactive LED Visualizer

This is my very first programming and electronics project! It captures live audio, processes the frequencies in real-time, and dynamically drives a 4-channel LED hardware layout. 

I engineered this project from scratch—moving step-by-step from blinking a single light to splitting live audio across multiple physical channels.

# ✨ Features

* **4-Band Frequency Splitting:** Automatically parses incoming audio into four separate frequency ranges to isolate different elements of the music.
* **Self-Calibrating Pipeline:** Built a frame-by-frame error correction loop. Even if data drops or skips, the system automatically self-calibrates on the next millisecond cycle so there is no visible lag.
* **Iterative Logic:** Built completely out of single-page scripts focusing on fast processing loops and reliable hardware communication.