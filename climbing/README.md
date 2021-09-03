# Climbing
Adding a new climbing video works as follows:
1. record it (duh...)
2. add it to the `videos/` folder
3. run `../_plugins/add_new_climbs.py` and edit the new entries accordingly

```yaml
DJI_0051.MP4:
  color: blue       // the color of the route
  date: 2021-07-02  // the date
  zone: 4           // the zone in which it was climbed
  new: null         // whether it is new (updates the name to be in the canonical format)
  rotate: left      // whether to rotate the video (left/right)
  encode: null      // whether to encode using h264
  trim: 14.01,49.55 // whether to trim the video (start,end)
```
