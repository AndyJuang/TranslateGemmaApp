# TranslateGemmaApp 🍎

**Mac Live Subtitle Translator**
*Real-time, Offline, Floating Subtitles for macOS.*

TranslateGemmaApp is a privacy-focused macOS application that listens to your microphone, transcribes speech using **Whisper**, and translates it into English using Google's **TranslateGemma** model. All processing happens entirely **offline** on your device, optimized for Apple Silicon (M1/M2/M3) using `mlx-lm`.

## 🚀 Features

- **🔒 Fully Offline**: No data leaves your device. Powered by local AI models.
- **⚡ Apple Silicon Optimized**: Uses `mlx-lm` for fast, efficient inference on Mac.
- **🎙️ Smart ASR**: Uses `faster-whisper` with **VAD (Voice Activity Detection)** to ignore silence and reduce hallucinations.
- **💬 Live Translation**: Powered by `google/translategemma-4b-it` for high-quality translation.
- **🖥️ Floating Overlay**: A transparent, "always-on-top" subtitle window that sits over your other apps.
- **⌨️ Global Hotkey**: Toggle recording on/off anywhere with `Option` + `Space`.
- **📊 Stats Dashboard**: Real-time display of CPU, RAM usage, and Model Status.

## 🛠️ Requirements

- **macOS** 13.3 or later.
- **Apple Silicon Mac** (M1/M2/M3/M4).
- **Python 3.10+**.
- **Microphone** access.
- **Input Monitoring** permission (for global hotkeys).

## 📥 Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/AndyJuang/TranslateGemmaApp.git
    cd TranslateGemmaApp
    ```

2.  **Create a Virtual Environment** (Recommended):
    ```bash
    /usr/bin/python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

    *Note: If you encounter `mlc-llm` or `mlx` errors, ensure you are using a clean environment and not Anaconda base.*

4.  **Model Authentication (One-time)**:
    `google/translategemma-4b-it` is a gated model.
    1.  Accept terms on [Hugging Face](https://huggingface.co/google/translategemma-4b-it).
    2.  Login locally:
        ```bash
        huggingface-cli login
        ```

##  ▶️ Usage

1.  **Run the App**:
    ```bash
    python3 main.py
    ```
    *First run will download models (~5GB). Please wait.*

2.  **Controls**:
    - **Toggle Recording**: Press `Option` + `Space`.
    - **Move Window**: Click and drag the subtitle text.
    - **Quit**: Press `Ctrl+C` in the terminal.

## 🧩 Tech Stack

- **UI**: PyQt6
- **ASR**: faster-whisper (Whisper-large-v3 logic compatible)
- **Translation**: mlx-lm (TranslateGemma 4B)
- **Input**: pynput
- **System Stats**: psutil

## 📄 License

MIT License.
