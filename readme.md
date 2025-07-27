# 🧭 Rally Crowd Estimator – Polygon Selection Version

This is a lightweight Python application for estimating the number of people at a rally, protest, or concert using a polygon-drawn area on a Google Maps snapshot.

Instead of tedious brushing, this version allows you to:
- Click **two points** to define a known real-world distance
- Click **multiple points** to outline a **polygonal road area**
- Automatically calculate:
  - Road area in square meters
  - Estimated crowd size based on user-defined density

---

## ✅ Features

- Polygon-based manual zone selection (quick and accurate)
- Crowd density input (people per m²)
- Scale calibration using known map distance
- Area calculation and live visual feedback
- Overlay image saved with highlighted road area and scale points

---

## 🚀 How to Use

### 1. 🖼 Prepare a Map Image
Take a screenshot from Google Maps showing the rally area. Save it as something like `image.jpeg`.

### 2. 🛠 Install Requirements
```bash
pip install -r requirements.txt
