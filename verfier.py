import cv2
import numpy as np
import os
import math

print("🖌️ RALLY CROWD ESTIMATOR – POLYGON MODE")

# --- Step 1: User Inputs ---
image_path = input("📁 Enter image file name (e.g., map.jpg): ").strip()
if not os.path.isfile(image_path):
    print("❌ File not found.")
    exit()

people_density = float(input("👥 Enter crowd density (people per m²): "))
real_dist_m = float(input("📏 Enter real-world distance between 2 points (in meters): "))

# --- Step 2: Load Image ---
img = cv2.imread(image_path)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
height, width = img.shape[:2]
mask = np.zeros((height, width), dtype=np.uint8)
scale_points = []
polygon_points = []

# -------------------------------
# 📏 STEP 1: Scale Point Selection
# -------------------------------
def scale_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN and len(scale_points) < 2:
        scale_points.append((x, y))

cv2.namedWindow("STEP 1: Click 2 Scale Points Then Close")
cv2.setMouseCallback("STEP 1: Click 2 Scale Points Then Close", scale_click)

print("\n📏 STEP 1: Click 2 scale points on the image. Then close the window manually.")
while True:
    temp = img_rgb.copy()
    for pt in scale_points:
        cv2.circle(temp, pt, 6, (255, 0, 0), -1)
    cv2.imshow("STEP 1: Click 2 Scale Points Then Close", cv2.cvtColor(temp, cv2.COLOR_RGB2BGR))
    if len(scale_points) == 2:
        break
    if cv2.waitKey(1) & 0xFF == 27:
        break
cv2.destroyAllWindows()

if len(scale_points) < 2:
    print("❌ You must click 2 points.")
    exit()

# Calculate meters per pixel
pt1, pt2 = scale_points
pixel_dist = math.hypot(pt1[0] - pt2[0], pt1[1] - pt2[1])
meters_per_pixel = real_dist_m / pixel_dist
pixel_area_m2 = meters_per_pixel ** 2

# -------------------------------
# 🎨 STEP 2: Polygon Drawing Mode
# -------------------------------
def polygon_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        polygon_points.append((x, y))

cv2.namedWindow("STEP 2: Draw Polygon - Press Enter When Done")
cv2.setMouseCallback("STEP 2: Draw Polygon - Press Enter When Done", polygon_click)

print("🎯 STEP 2: Click to draw polygon points around the road area. Press ENTER to finish.")
while True:
    temp = img_rgb.copy()
    for pt in scale_points:
        cv2.circle(temp, pt, 6, (255, 0, 0), -1)
    for pt in polygon_points:
        cv2.circle(temp, pt, 4, (0, 255, 255), -1)
    if len(polygon_points) > 1:
        cv2.polylines(temp, [np.array(polygon_points)], False, (0, 255, 255), 2)
    cv2.imshow("STEP 2: Draw Polygon - Press Enter When Done", cv2.cvtColor(temp, cv2.COLOR_RGB2BGR))
    key = cv2.waitKey(1) & 0xFF
    if key == 13:  # Enter key
        break
cv2.destroyAllWindows()

if len(polygon_points) < 3:
    print("❌ You must define at least 3 polygon points.")
    exit()

# Fill polygon into mask
cv2.fillPoly(mask, [np.array(polygon_points)], 255)

# -------------------------------
# ✅ Final Calculation
# -------------------------------
road_pixels = np.sum(mask == 255)
road_area_m2 = road_pixels * pixel_area_m2
estimated_people = int(road_area_m2 * people_density)

# -------------------------------
# 🖼️ Output
# -------------------------------
print("\n✅ ESTIMATION COMPLETE")
print(f"📏 Distance: {real_dist_m:.2f} m")
print(f"🧮 Pixel distance: {pixel_dist:.2f} px → {meters_per_pixel:.5f} m/pixel")
print(f"🛣️ Road pixels in polygon: {road_pixels}")
print(f"📐 Area: {road_area_m2:.2f} m²")
print(f"👥 Estimated crowd: {estimated_people} people")

# Overlay output image
overlay = img_rgb.copy()
overlay[mask == 255] = [0, 255, 0]
for pt in scale_points:
    cv2.circle(overlay, pt, 6, (255, 0, 0), -1)
for pt in polygon_points:
    cv2.circle(overlay, pt, 4, (0, 255, 255), -1)
output_file = "overlay.jpg"
cv2.imwrite(output_file, cv2.cvtColor(overlay, cv2.COLOR_RGB2BGR))
print(f"🖼️ Overlay saved as: {output_file}")
