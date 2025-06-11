# 🛠️ How to Use `make` on Windows

This guide explains how to install and use `make` on Windows, with three different options depending on your preference and environment.

---

## ✅ Option 1: Use `make` on Windows via Git Bash

Git Bash provides a Unix-like shell on Windows. However, it **does not include `make` by default**, so you must install it separately.

### 📦 Step-by-Step: Installing Git Bash

1. Download Git for Windows:  
   👉 https://gitforwindows.org

2. Install Git and ensure that **Git Bash** is included in the installation.

3. Open Git Bash in your project folder by right-clicking and selecting **"Git Bash Here"**.

4. Now follow **Option 3** (below) to install `make` inside Git Bash via MSYS2.

---

## ✅ Option 2: Install GNU Make via Chocolatey

This method allows you to use `make` directly in PowerShell or Command Prompt.

### 📦 Step-by-Step: Installing `make` with Chocolatey

> ⚠️ You must have **Administrator privileges** to install Chocolatey and software packages.

1. Open **PowerShell as Administrator**.

2. Install Chocolatey by running:

   ```powershell
   Set-ExecutionPolicy Bypass -Scope Process -Force
   [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12
   iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
````

3. Close and reopen PowerShell **(or restart your system)**.

4. Now install `make`:

   ```powershell
   choco install make
   ```

5. Verify it works:

   ```powershell
   make --version
   ```

---

## ✅ Option 3: Manually Add `make` to Git Bash via MSYS2

MSYS2 provides a full Unix toolchain for Windows, including `make`.

### 📦 Step-by-Step: Installing `make` using MSYS2

1. Download MSYS2 from:
   👉 [https://www.msys2.org](https://www.msys2.org)

2. Install MSYS2 (default path: `C:\msys64`).

3. Open the **"MSYS2 MSYS"** terminal (not UCRT64 or MINGW64).

4. Update the package manager:

   ```bash
   pacman -Syu
   ```

   > 📝 If prompted, close the terminal and re-open it after updating.

5. Install `make`:

   ```bash
   pacman -S make
   ```

6. Verify installation:

   ```bash
   make --version
   ```

---

### ⚙️ Add `make` to System PATH (Optional but Recommended)

To use `make` in Git Bash (or any terminal), you must add it to your system's PATH:

1. Find the path to `make`, usually:

   ```
   C:\msys64\usr\bin
   ```

2. Open **System Properties → Environment Variables**.

3. Under **"User variables"** or **"System variables"**, find the `Path` variable and click **Edit**.

4. Add the path:

   ```
   C:\msys64\usr\bin
   ```

5. Click **OK** and restart Git Bash or your system.

6. Test in Git Bash:

   ```bash
   make --version
   ```

---

## ✅ Example Usage

Once `make` is installed, you can run:

```bash
make fmt
```

From within your project folder, assuming you have a `Makefile` with a `fmt` target.

---

## 📝 Alternative: Bash Script Instead of Makefile

If you prefer not to install `make`, create a simple Bash script:

**format.sh**

```bash
#!/bin/bash
isort mbox_converter/
black -l 100 mbox_converter/
black -l 100 tests/
```

Make it executable:

```bash
chmod +x format.sh
./format.sh
```

---

## 🔚 Summary

| Option     | Description                     | Difficulty |
| ---------- | ------------------------------- | ---------- |
| Git Bash   | Use `make` in Unix-like shell   | Medium     |
| Chocolatey | Use `make` in PowerShell or CMD | Easy       |
| MSYS2      | Full Unix toolchain for Windows | Medium     |

Choose the option that best fits your workflow!
