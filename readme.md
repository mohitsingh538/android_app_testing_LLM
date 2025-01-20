This repository revolutionizes mobile app testing by leveraging the power of large language models (LLMs) to interpret and execute high-level instructions seamlessly. Combine the flexibility of Appium, the efficiency of ADB, and the intelligence of cutting-edge AI to automate complex app interactions with ease. Whether it’s navigating UI screens, taking screenshots, or performing searches, this tool simplifies testing workflows for dynamic mobile applications. Perfect for developers and QA engineers aiming for smarter, faster, and more reliable automation! 🌟

---

# Key Update: Support for Fine-Tuned t5-base Model
To accommodate developers and startups where frequent LLM API calls may not be feasible due to cost, latency, or dependency constraints, this tool now includes support for a fine-tuned t5-base model. The t5-base model is a transformer-based sequence-to-sequence architecture designed to handle natural language processing tasks efficiently.
Download the fine-tuned model [here](https://drive.google.com/file/d/1H1J-SaVlIFbGj9HwJOluFZL7VcgU-0_C/view?usp=sharing). Training dataset is available inside:

```
android_app_testing_LLM/
├── fine-tuned/
│   ├── dataset
        └── natural_language_dataset.csv
```

This option is ideal for scenarios where:

1. #### Machine configurations support local inference:
   - The t5-base model can be run on a GPU or CPU, depending on available resources.

2. #### Rapid response from large models is not a critical priority:
   - While t5-base may not match the inference speed or sophistication of large LLMs, it provides sufficient accuracy for many sequence-to-sequence tasks, such as generating app actions.

3. #### Local-only setups are preferred:
   - Avoid reliance on external API calls for LLM inference, which enhances data security and reduces operational costs.

### Advantages of Using t5-base
- Cost Efficiency: No recurring costs for API calls.
- Flexibility: Works offline if the model is downloaded and loaded locally.
- Customizable: Fine-tuning is possible to adapt the model to specific app testing use cases.


---

# How to Run the App

This document provides step-by-step instructions to set up and run the app. Please follow these instructions carefully to ensure the application works as expected.

---

## Pre-requisites

Before running the application, ensure you have the following installed and configured:

1. **ADB (Android Debug Bridge)**:
   - Installed and available in your system's PATH.
   - Verify installation by running:
     ```bash
     adb version
     ```

2. **Appium Server**:
   - Installed and running with relaxed security enabled.
   - Start Appium server using:
     ```bash
     appium --relaxed-security
     ```

3. **Python Environment**:
   - Python 3.10 is recommended.
   - A virtual environment is highly recommended to isolate dependencies.

4. **Connected Debug Device**:
   - Connect your Android device via USB or Wi-Fi.
   - Verify the connection using:
     ```bash
     adb devices
     ```
   - Ensure the device is listed under `adb devices` output.

5. **Streamlit Installed**:
   - Required to launch the app as a Streamlit web app.

6. **Application is installed in the Emulator**:
   - Whichever app name you will be mentioning in the playground, it must be installed in your emulator.

7. **OpenAI supported LLM inference credentials**:
   - Base URL of the inference
   - API key
   - LLM Model

### Create a ```.env``` with following credentials:
- OPENAI_BASE_URL
- OPENAI_API_KEY
- OPENAI_MODEL

---

## Setup Instructions

1. **Clone the Repository**:
   - Clone the application repository to your local machine.
     ```bash
     git clone https://github.com/mohitsingh538/android_app_testing_LLM.git .
     cd android_app_testing_LLM
     ```

2. **Install Dependencies**:
   - Install all the required Python packages from the `requirements.txt` file.
     ```bash
     pip install -r requirements.txt
     ```

3. **Verify Appium and ADB Setup**:
   - Ensure Appium server is running:
     ```bash
     appium --relaxed-security
     ```
   - Confirm the device is connected using:
     ```bash
     adb devices
     ```

4. **Start the Application**:
   - Run the application using Streamlit:
     ```bash
     streamlit run main.py
     ```

5. **Access the Application**:
   - Open the URL displayed in your terminal, typically:
     ```
     Local URL: http://localhost:8501
     Network URL: http://<your-local-ip>:8501
     ```

---

## Troubleshooting

### Common Issues and Fixes

1. **Device Not Detected**:
   - Ensure the device is in developer mode and USB debugging is enabled.
   - Check the device connection with:
     ```bash
     adb devices
     ```

2. **Appium Server Not Running**:
   - Start the server with:
     ```bash
     appium --relaxed-security
     ```

3. **Dependencies Not Installed**:
   - Ensure all Python dependencies are installed:
     ```bash
     pip install -r requirements.txt
     ```

4. **Port Conflicts**:
   - If Streamlit fails to start due to port conflicts, specify an alternate port:
     ```bash
     streamlit run main.py --server.port <port>
     ```

---

## Screenshots

### Playground

![playground](https://i.ibb.co/vc7syHm/Screenshot-2025-01-17-at-10-41-14-PM.png)

### Debug Started

![debug started](https://i.ibb.co/nrPkYJ7/Screenshot-2025-01-17-at-10-41-46-PM.png)

### Debug Complete

![debug completed](https://i.ibb.co/5ktqdPz/Screenshot-2025-01-17-at-10-42-25-PM.png)

---

## Notes

- The application automates interactions with a specified app on the connected Android device.
- Ensure the target app is installed on the device and its package name and activity name are correct.
- Modify instructions and logic as needed to match your use case.

---


