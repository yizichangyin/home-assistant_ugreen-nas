
# 🧩 UGREEN NAS – Home Assistant Integration

**⚠️ Beta Version**  
This is an **experimental Home Assistant integration** for UGREEN NAS devices.  
Development is active, and the API is undocumented.

---

## ℹ️ Background & Limitations

- UGREEN currently does **not provide a long-lasting access token**.
- This integration uses a **local Docker token server** running on the NAS.
- **All data stays entirely within the local network.**
- A release via **HACS** is currently not possible.

---

## 🔧 Installing the Integration (Custom Component)

### 1. Prepare the Files

1. Download the repository as a ZIP:  
   👉 [Download Code](https://github.com/Tom-Bom-badil/home-assistant_ugreen-nas/archive/refs/heads/main.zip)

2. Extract the ZIP file.

3. Navigate to:
   ```
   home-assistant_ugreen-nas/custom_component_ugreen/custom_components/ugreen_nas
   ```

4. Copy the entire `ugreen_nas` folder to:
   ```
   /config/custom_components/
   ```

   If `custom_components` does not exist, you can create this folder yourself.

### 2. Restart Home Assistant

- Restart Home Assistant via the UI:  
  **Settings → System → Controls → Restart**

---

## 🐳 Installing the Docker Token Server (on UGREEN NAS)

To allow Home Assistant to receive a valid authentication token, a small local token server must be running:

### Steps:

1. Log into your UGREEN NAS.

2. Install and open **Docker** (if not already installed).

3. Create a new project, e.g., `ugreen-access-token`.

4. Open the **Compose Editor** and paste the content of the file  
   `home-assistant_ugreen-nas/custom_component_ugreen/ugreen_api_token/docker-compose.yaml`.

5. Add your credentials under `environment` and make further changes if necessary:
   ```yaml
   environment:
     - USERNAME=your_nas_username
     - PASSWORD=your_nas_password
   ```

6. Click **Deploy** and start Docker (the container will not start successfully – this is expected).

7. Now copy the remaining files from `ugreen_api_token` into the appropriate Docker folder on your NAS.

8. Manually start the project in Docker.

✅ If everything works, you should see the following in the **Logs tab**:
```
Uvicorn running on http://0.0.0.0:4115 (Press CTRL+C to quit)
```

---

## 🔗 Setup in Home Assistant

1. Open Home Assistant → **Settings → Devices & Services → Add Integration**

2. Search for **UGREEN NAS**

3. Enter your connection details:
   - IP address of your NAS
   - API port (default: `9443`)
   - Token port (default: `4115`)
   - Username & password
   - Optional: Enable HTTPS and certificate validation

> As mentioned, your data stays on the NAS and is only retrieved by Home Assistant via an HTTP request.

 Example token call:  
> `http://<NAS-IP>:4115/token?username=your_username&password=your_password`

4. Click **Submit** – done!

---

## 🧠 What Does This Integration Offer?

- **Sensors for:**
  - CPU & RAM (usage, frequency, model, temperature)
  - Upload/download speed
  - System and device information
  - Volumes, pools, and disks

- **Buttons for:**
  - Restart NAS
  - Shutdown NAS

---

## 🛠️ Troubleshooting

| Issue                   | Solution                                                              |
|-------------------------|-----------------------------------------------------------------------|
| `invalid_auth`          | Wrong username or password? Is the token server running?              |
| `cannot_connect`        | Is your NAS reachable from Home Assistant?                            |
| Token server not active | Is the Docker container running correctly? Check logs                 |
| Component not detected  | Restart Home Assistant and check the paths                            |

---

## 🗣️ Feedback, Bugs & Ideas

Help us improve this integration!  
👉 [Report an Issue on GitHub](https://github.com/Tom-Bom-badil/home-assistant_ugreen-nas/issues)

---

## ❤️ Thank You & Have Fun!

> Plugin Version: v0.8.0