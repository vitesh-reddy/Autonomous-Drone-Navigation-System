# Assets Directory

Place image assets here for pygame visualization.

## Required Files

The visualization requires the following PNG image files:

1. **grid.png** (60×600 pixels)
   - Grid background for the game environment
   
2. **drone.png** (60×60 pixels)
   - Sprite for the drone without package
   
3. **drone_box.png** (60×60 pixels)
   - Sprite for the drone carrying the package
   
4. **pickup.png** (60×60 pixels)
   - Sprite for the pickup location/item
   
5. **drop.png** (60×60 pixels)
   - Sprite for the drop location/item
   
6. **bird1.png** (60×60 pixels)
   - First bird type sprite
   
7. **bird2.png** (60×60 pixels)
   - Second bird type sprite

## Important Notes

- All images must be in PNG format with transparency support (RGBA)
- Image dimensions must match (60×60 for square sprites, 60×600 for grid)
- If any image is missing, the visualization will display a warning but training will still complete

## Fallback Behavior

If assets are not available:
- Training and plotting still work normally
- Only pygame visualization will be skipped
- All learning metrics will still be generated

## File Placement

Place all image files directly in the `assets/` folder:

```
assets/
├── grid.png
├── drone.png
├── drone_box.png
├── pickup.png
├── drop.png
├── bird1.png
└── bird2.png
```
