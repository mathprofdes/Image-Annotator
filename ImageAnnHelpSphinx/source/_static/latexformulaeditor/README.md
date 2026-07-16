# Overview:

An offline LaTeX formula editor that offers real-time preview with customizable rendering engines (KaTeX/MathJax). It includes features like click-to-insert LaTeX elements, clipboard export, and image export (SVG, PNG, JPG). Designed for both ease of use and offline-first functionality, the editor is lightweight and deployable on local servers.

# Features:

* __Real-time Preview__: Instantly render LaTeX formulas with KaTeX or MathJax.

* __Click-to-insert__: Easily insert LaTeX elements at the cursor.

* __Export Options__: Export formulas as SVG, PNG, JPG, or copy formulas as PNG to the clipboard.

* __Minimalistic Interface__: Clean and simple UI for focused editing.

* __Cross-Platform__: Works locally by opening `index.html` in any modern browser.

* __Customizable__: Lightweight structure for easy modifications.

# Demo:

Live demo available at: https://latex.moskensoap.xyz

# Running the Editor in Browser:

You can easily run the LaTeX Formula Editor by following these simple steps:

- **Option 1: Clone with Git**

  Open a terminal and run the following command:
  ```bash
  git clone https://github.com/moskensoap/latex-formula-editor.git
  ```
  Then, navigate to the project folder and open `index.html` in any modern browser.

- **Option 2: Download ZIP**

  Go to the [repository page](https://www.github.com/moskensoap/latex-formula-editor), click "Code" > "Download ZIP", and extract the files. After extracting, simply double-click `index.html` to open it in your browser.
  

# Running the Editor with Electron

## Step 1: Install Dependencies

```bash
git clone https://github.com/moskensoap/latex-formula-editor.git
cd latex-formula-editor
npm install
```

## Step 2: Run in Development Mode

```bash
npm run start
```

## Step 3: Build for Production
```bash
# Build for Windows (64-bit)
npm run build:win64

# Build for Windows (32-bit)
npm run build:win32

# Build for macOS (Intel)
npm run build:mac

# Build for macOS (Apple Silicon)
npm run build:mac-arm

# Build for Linux (64-bit)
npm run build:linux
```

## Step 4:  Locate the Executable

```bash
cd dist
```
Find the appropriate executable for your platform in the generated folder (e.g., latexformula-win32-x64) and run the application. 

Enjoy!

# Docker Deployment:

### 1. Quick Start (via Docker Hub):

```bash
docker run --restart unless-stopped -d -p 8080:80 --name latex-formula-editor moskensoap/latex-formula-editor:latest
```

Access via: 

`http://localhost:8080` (local)

`http://<your-ip>:8080` (remote)

### 2. Custom Build (from source):

If you need a custom Docker image, or if the architecture of the provided Docker Hub image does not suit your needs, you can build your own Docker image by following these steps:

* __To start:__

```bash
cd docker
docker compose up -d
```

* __To stop:__

```bash
docker compose down
```

Access via: 

`http://localhost:8080` (local)

`http://<your-ip>:8080` (remote)

### 3. OCR (Convert Images to LaTeX):
Powered by [LaTeX-OCR](https://github.com/lukas-blecher/LaTeX-OCR) by @lukas-blecher.

* __To start:__

```bash
cd docker/pix2tex
docker compose up -d
```

* __To stop:__

```bash
docker compose down
```

Access via: 

`http://localhost:8501` (local)

`http://<your-ip-address>:8501` (remote)

# Rendering Engines & Export Support

This project bundles:

* KaTeX: https://github.com/KaTeX/KaTeX

* MathJax: https://github.com/mathjax/MathJax

* html2canvas: https://github.com/niklasvh/html2canvas

You can update KaTeX or MathJax by replacing the corresponding folders. If folder structure changes, adjust paths in the HTML accordingly.

We are grateful to these excellent open-source projects for making this editor possible.

# Feedback & Contributions

We welcome your suggestions, questions, and feature ideas!
Feel free to open an [issue](https://github.com/moskensoap/latex-formula-editor/issues) to start a discussion or report a problem.