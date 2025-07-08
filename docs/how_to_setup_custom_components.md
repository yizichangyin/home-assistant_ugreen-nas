
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

## 🔧 Installing

### 1. Adding and installing the Integration (Custom Component)

1. In Home Assistant, open **HACS** from the sidebar.
2. Click the **three dots (⋯)** in the top-right corner and choose  
   **“Custom repositories”**.
3. Click **“Add”**.
4. Enter the following details:
   - **Repository URL:**  
     `https://github.com/Tom-Bom-badil/home-assistant_ugreen-nas`
   - **Category:** `Integration`
5. Confirm with **Add**.

---

## 🐳 Installing the Docker Token Server (on UGREEN NAS)

To allow Home Assistant to receive a valid authentication token, a small local token server must be running:

### Steps

1. Log into your UGREEN NAS.

2. Install and open **Docker** (if not already installed).

3. Create a new project, e.g., `ugreen-access-token`.

4. Open the **Compose Editor** and paste the content of this file  

   [Docker compose](https://github.com/Tom-Bom-badil/home-assistant_ugreen-nas/blob/main/addons/docker-compose.yaml)

5. Add your credentials under `environment` and make further changes if necessary:

   ```yaml
   environment:
     UGREEN_NAS_API_SCHEME: "https"
     UGREEN_NAS_API_PORT: "9443"
     UGREEN_NAS_API_VERIFY_SSL: "false"
     USERNAME: "your_admin_name"
     PASSWORD: "your_password"
   ```

6. Click **Deploy** and start Docker

✅ If everything works, you should see the following in the **Logs tab**:

```
Uvicorn running on http://0.0.0.0:4115 (Press CTRL+C to quit)
```

---

## 🔗 Setup in Home Assistant

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=ugreen)

1. Open Home Assistant → **Settings → Devices & Services → Add Integration**

2. Search for **UGREEN NAS**

3. Enter your connection details:
   - API port (default: `9443`)
   - Token port (default: `4115`)
   - Username & password
   - Optional: Enable HTTPS and certificate validation

> As mentioned, your data stays on the NAS and is only retrieved by Home Assistant via an HTTP request.

 Example token call:  
> `http://<NAS-IP>:<NAS-API-PORT>/token?username=your_username&password=your_password`

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

| Issue                       | Solution                                                              |
|-----------------------------|-----------------------------------------------------------------------|
| `invalid_auth`              | Wrong username or password? Is the token server running?              |
| `500 Internal Server Error` | 2-factor-authentication (2FA) activated for the user? ¹               |
| `cannot_connect`            | Is your NAS reachable from Home Assistant?                            |
| Token server not active     | Is the Docker container running correctly? Check logs                 |
| Component not detected      | Restart Home Assistant and check the paths                            |

¹ If you need 2FA on your device for regular users, it is recommended to create a dedicated admin user for the integration with an extra long and complex password.

---

## 🗣️ Feedback, Bugs & Ideas

Help us improve this integration!  
👉 [Report an Issue on GitHub](https://github.com/Tom-Bom-badil/home-assistant_ugreen-nas/issues)

---

## ❤️ Thank You & Have Fun

> Plugin Version: v0.8.0
