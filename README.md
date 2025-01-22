# NOCS Material Generator Addon for Blender

This Blender addon generates **NOCS (Normalized Object Coordinate Space)** materials for mesh objects, allowing you to visualize objects in normalized object space.

## Features
- Generate NOCS materials for individual objects.
- Automatically calculates bounding box dimensions for accurate normalization.
- Adds the generated material to the object with a vertex color map.

## Installation
1. Download the latest version of the addon (`nocs_material_generator.py`).
2. Open Blender and go to **Edit > Preferences > Add-ons**.
3. Click **Install...**, select the downloaded file, and enable the addon.
4. Access the addon in the **Item Tab** in the Sidebar under **NOCS Material Generator**.

## Usage
1. Select the object for which you want to generate a NOCS material.
2. Open the Sidebar (**N** key) and go to the **Item Tab**.
3. Find the **NOCS Material Generator** panel.
4. Click **Generate NOCS Material** to apply the material to the selected object.

## Notes
- Only works on objects of type `MESH`.
- Adds a new vertex color map called `NOCS` to the object.

## Requirements
- Blender 2.82 or newer.
