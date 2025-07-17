# 🧩 UGREEN NAS – Home Assistant Integration

**⚠️ Beta Version**  
This is an **experimental Home Assistant integration** for UGREEN NAS devices.  
Development is active, and the API is currently undocumented.

---

## ℹ️ Background & Limitations

- UGREEN currently does **not provide a long-term access token**.
- This integration uses a **local Docker token server** running on your NAS.
- **All data stays entirely within your local network.**
- A release via **HACS** is not possible at this time.

---

## 🔧 Installation

### 1. Add the Integration (Custom Component)

**Automatic:**

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=tom-bom-badil&repository=home-assistant_ugreen-nas&category=Integration)

**Manual:**

1. In Home Assistant, open **HACS** from the sidebar.
2. Click the **three dots (⋯)** in the top-right corner and choose **“Custom repositories”**.
3. Click **Add**.
4. Enter the following details:
   - **Repository URL:**  
     `https://github.com/Tom-Bom-badil/home-assistant_ugreen-nas`
   - **Category:** `Integration`
5. Confirm with **Add**.

---

## 🐳 Method 1: Run the Docker UGREEN API Token Proxy (on Home Assistant)

[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2FTom-Bom-badil%2Fhome-assistant_ugreen-nas)

⚠️ **Note:** Installation may take up to 10 minutes.

1. Open and add the addon.
2. Install the addon.
1. Go to the configuration.
2. Make the necessary changes (e.g., add the IP address of your NAS).
3. Save and start the add-on.

## 🐳 Method 2: Run the Docker UGREEN API Token Proxy (on UGREEN NAS)

To let Home Assistant receive a valid authentication token, you need to run a small local token server.

### Steps

1. Log in to your UGREEN NAS.

2. Install and open **Docker** (if not already installed).

3. Create a new project, e.g., `ugreen-access-token`.

4. Open the **Compose Editor** and paste the contents of this file:  
   [docker-compose.yaml](https://github.com/Tom-Bom-badil/home-assistant_ugreen-nas/blob/main/addons/docker-compose.yaml)

5. Add your credentials under `environment` and adjust other settings if needed:

   ```yaml
   environment:
     UGREEN_NAS_API_SCHEME: "https"
     UGREEN_NAS_API_PORT: "9999"
     UGREEN_NAS_API_VERIFY_SSL: "false"
     USERNAME: "your_admin_name"
     PASSWORD: "your_password"
   ```

6. Click **Deploy** and start the container.

✅ If everything works correctly, you should see the following in the **Logs tab**:

```
Uvicorn running on http://0.0.0.0:4115 (Press CTRL+C to quit)
```

---

## 🔗 Set Up in Home Assistant

**Automatic:**

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=ugreen)

**Manual:**

1. In Home Assistant, go to **Settings → Devices & Services → Add Integration**.

2. Search for **UGREEN NAS**.

## Configuration:

Enter your connection details:  
   - API port (default: `9999`)
   - Token port (default: `4115`)
   - Username & password
   - Optional: Enable HTTPS and SSL certificate validation

> As mentioned, your data stays on your NAS and is only retrieved by Home Assistant via an HTTP request.

Example token call:  
> `http://<NAS-IP>:<NAS-API-PORT>/token?username=your_username&password=your_password`

4. Click **Submit** – done!

---

## 🧠 What Does This Integration Provide?

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

| Issue                      | Possible Solution                                                     |
|----------------------------|------------------------------------------------------------------------|
| `invalid_auth`             | Wrong username/password? Is the token server running?                 |
| `500 Internal Server Error`| Is two-factor authentication (2FA) enabled for this user?¹            |
| `cannot_connect`           | Is your NAS reachable from Home Assistant?                            |
| Token server not active    | Is the Docker container running correctly? Check the logs.            |
| Component not detected     | Restart Home Assistant and double-check your paths.                   |

¹ If you need 2FA for regular users, it’s recommended to create a dedicated admin user for this integration with a long, complex password.

---

## 🗣️ Feedback, Bugs & Ideas

Help us improve this integration!  
👉 [Open an issue on GitHub](https://github.com/Tom-Bom-badil/home-assistant_ugreen-nas/issues)

---

## ❤️ Thank You & Have Fun!