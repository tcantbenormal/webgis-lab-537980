# Web GIS Lab 03: District Dashboard

## Part 1: Set up the project

The lab was done in the same repository as Lab 2, `webgis-lab-537980`, so that Lab 2 stays published. As in Lab 2, VS Code is not installed on this machine: every command was run in a PowerShell window, the page was served with Python's built-in server from the repository root so that the address ends in `/lab3/index.html`, and the QGIS toolchain was driven from the command line with QGIS itself used for the Checkpoint 2 view. Each command was run on its own and screenshotted.

### 1.1 Create the folder

```powershell
cd D:\MS\WebGIS\webgis-lab
mkdir lab3
mkdir lab3\data
copy data\districts.geojson lab3\data\districts.geojson
```

![cd to the Lab 2 repository](screenshots/p1_01_cd_repo.png)

![mkdir lab3](screenshots/p1_02_mkdir_lab3.png)

![mkdir lab3\data](screenshots/p1_03_mkdir_data.png)

![Copy the Lab 2 districts.geojson into lab3\data](screenshots/p1_04_copy_districts.png)

The three files were created with one PowerShell command and listed:

```powershell
New-Item lab3\index.html, lab3\style.css, lab3\app.js -ItemType File
Get-ChildItem lab3
```

![New-Item creates index.html, style.css and app.js](screenshots/p1_05_new_item_files.png)

![Get-ChildItem lab3](screenshots/p1_06_dir_lab3.png)

### Checkpoint 1

The `lab3` folder with its three files and `data\districts.geojson`, shown in File Explorer opened from the console.

![explorer lab3](screenshots/p1_07_explorer.png)

![Checkpoint 1: lab3 with index.html, style.css, app.js and data](screenshots/checkpoint1_lab3_folder.png)

---

## Part 2: Make a point layer in QGIS

### 2.1 Point on surface, not centroid

Both tools from Vector, Geometry Tools were run on `lab3/data/districts.geojson` through `qgis_process`, the same algorithms the menu runs.

```powershell
qgis_process-qgis-ltr.bat run native:centroids --INPUT=lab3\data\districts.geojson --ALL_PARTS=false --OUTPUT=..\lab3-data\centroids.geojson
qgis_process-qgis-ltr.bat run native:pointonsurface --INPUT=lab3\data\districts.geojson --ALL_PARTS=false --OUTPUT=..\lab3-data\point_on_surface.geojson
```

![OSGeo4W tools on the PATH](screenshots/p2_01_osgeo_env.png)

![Centroids](screenshots/p2_02_centroids.png)

![Point on Surface](screenshots/p2_03_point_on_surface.png)

**The district whose centroid falls outside it is Sibi, in Balochistan.** Sibi is a MultiPolygon in two parts joined by a narrow neck, so its centre of mass (67.9447 E, 29.7615 N) lands in the gap between the parts, inside the neighbouring district. Point on Surface places the point at 68.2501 E, 29.7271 N, inside the larger eastern part. A symbol drawn at the centroid would be read as belonging to the neighbour.

### 2.2 Export

The Point on Surface result was exported with precision 5 in EPSG:4326, exactly as the Save Features As dialog does:

```powershell
ogr2ogr -f GeoJSON lab3\data\district_points.geojson ..\lab3-data\point_on_surface.geojson -t_srs EPSG:4326 -lco COORDINATE_PRECISION=5
```

![Export district_points.geojson](screenshots/p2_04_export_points.png)

![ogrinfo: 160 point features, WGS 84, pop_2023 carried over; file size 31,576 bytes](screenshots/p2_05_points_info.png)

| district_points.geojson | Value |
|---|---|
| Size | 31,576 bytes (31 kB) |
| Feature count | 160 |
| Geometry | Point, EPSG:4326, five decimal places |
| Attributes | district, province, pcode, pop_2023, area_km2 (inherited from the districts) |
| Districts with no population | 25 |

The attribute table in QGIS confirms 160 features with the inherited attributes:

![Attribute table of the point layer: 160 features](screenshots/p2_06_qgis_attribute_table_points.png)

### Checkpoint 2

Sibi zoomed in QGIS with the districts, the centroids (red circles) and the points on surface (green triangles). The red Sibi centroid sits in the narrow neck outside the polygon; the green Sibi point is inside the eastern part.

![Checkpoint 2: Sibi, centroid outside the district, point on surface inside](screenshots/checkpoint2_sibi_centroid_vs_point_on_surface.png)

---

## Part 3: The page, the map and its basemaps

### 3.1 index.html and 3.2 style.css

Both files were written exactly as given in the handout.

![index.html](screenshots/p3_01_index_html.png)

![style.css](screenshots/p3_02_style_css.png)

### 3.3 The map, through its options, and 3.4 three basemaps and a layer control

The first block of `app.js` creates the map with `center`, `zoom`, `minZoom: 5`, `maxZoom: 14`, `maxBounds` and `maxBoundsViscosity: 1.0` in the options object, then the three tile layers, the layer control with `collapsed: false`, and the metric scale bar.

![app.js: map options, basemaps, layer control, scale](screenshots/p3_03_app_v1_map_basemaps.png)

The server was started from the repository root so that `lab3/index.html` is reached at `http://127.0.0.1:5500/lab3/index.html` and the data paths resolve relative to it.

![Starting the server from the repository root](screenshots/p3_04_start_server.png)

![The server log serving lab3](screenshots/p3_05_server_window.png)

**A substitution that had to be made.** The handout's default basemap, Carto Positron at `basemaps.cartocdn.com`, now returns placeholder tiles stamped "API KEY REQUIRED" instead of map tiles, because CARTO has put its free basemaps behind an API key. The page as written therefore opened on a grid of watermark tiles:

![Carto Positron tiles now require an API key](screenshots/p3_06_map_with_layer_control.png)

The quiet grey default was replaced with Esri's free Light Gray Canvas service, which serves the same purpose (a basemap that does not compete with a thematic layer) and uses the same `{z}/{y}/{x}` order as the Esri imagery template, so the handout's lesson about reading templates closely still applies. The attribution string credits Esri.

```javascript
const light = L.tileLayer(
  'https://server.arcgisonline.com/ArcGis/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}', {
  maxZoom: 16,
  attribution: 'Tiles &copy; Esri'
});
```

![app.js with the Light Gray Canvas default](screenshots/p3_07_app_v1_basemap_fix.png)

### Checkpoint 3

The Network tab with the Satellite (Esri) basemap selected and one tile request opened. Its URL is `https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/5/13/22`.

![Checkpoint 3: an Esri tile request with its URL](screenshots/checkpoint3_esri_tile_request_url.png)

**Row and column in the Esri URL.** The Esri template ends `{z}/{y}/{x}`, so in `/tile/5/13/22` the numbers are zoom 5, **row 13**, **column 22**. OpenStreetMap's template ends `{z}/{x}/{y}`, so the equivalent OSM tile is `/5/22/13.png`, column first. Leaflet fills in whichever placeholders the template contains in the order they appear, which is why each provider's template must be copied exactly.

---

## Part 4: A thematic layer, done properly

### 4.1 Why density, not population

Lab 2 shaded districts by population, which largely repeats their areas: a large district holds many people simply because it is large. A choropleth colours areas, so the value behind the colour must not grow with area. The dashboard therefore shades by density, `pop_2023 / area_km2`, computed by `densityOf` from two stored attributes every time a district is styled, and shows the population count a second way in Part 6, as proportional symbols.

### 4.2 to 4.5 Style by density, the feature group, loading, drawing and the legend

`show`, `densityOf`, `colourFor` and `styleFor` were added; `districtGroup` is a `L.featureGroup` registered with the layer control as the overlay "Population density"; `draw(province)` uses the `filter` hook with `keep`, clears and refills the group and updates the count; `loadJSON` and `loadData` fetch both files with `Promise.all`; and the legend lists the five density classes plus the no-data class.

![app.js: density functions, group, draw, loadData](screenshots/p4_01_app_v2_density_draw_legend.png)

![app.js: the legend](screenshots/p4_02_app_v2_rest.png)

With these breaks the 135 districts with census data fall 20, 18, 34, 41 and 22 into the five classes, exactly as the handout states, and 25 are grey.

### Checkpoint 4

The density map with its legend, and the layer control open showing the three basemaps and the one overlay.

![Checkpoint 4: density map, legend, layer control with three basemaps and one overlay](screenshots/checkpoint4_density_map_legend_layer_control.png)

---

## Part 5: Interaction: highlight and an info panel

The `info` control was added with `onAdd` and the custom `update` method; `highlight`, `unhighlight` and `zoomToDistrict` were written; `bindDistrict` binds a sticky tooltip and the three handlers; and `onEachFeature: bindDistrict` was handed to `L.geoJSON` inside `draw`.

![app.js: info control, highlight, unhighlight, zoomToDistrict, bindDistrict](screenshots/p5_01_app_v3_info_highlight.png)

### Checkpoint 5

Lahore under the pointer: the thick dark outline brought to the front, the tooltip, and the info panel reporting Punjab, population 13,004,135, area 1,729.9 km², density 7,517 per km², zoom level 5.

![Checkpoint 5: Lahore highlighted with tooltip and info panel](screenshots/checkpoint5_hover_highlight_info_panel.png)

---

## Part 6: Proportional symbols in their own pane

### 6.1 to 6.5

The `symbols` pane was created with z-index 450, between overlayPane (400) and markerPane (600). `radiusFor` takes the square root of the population divided by 160, so that the area of each circle, not its radius, follows the count; Lahore at 13.0 million gets a radius of 22.5 px. `circleFor` builds a `circleMarker` in the symbols pane with a tooltip; `hasPopulation` drops the 25 districts without a census value before `circleFor` can meet a null; `circleGroup` is the second overlay, "Population", filled inside `draw` with `filter` and `pointToLayer` together; three reference circles drawn with the same `radiusFor` were added to the legend; and the NUST overlay pairs a `L.circle` of 25,000 m with a `L.circleMarker` of 6 px.

![app.js: pane, radiusFor, circleFor, hasPopulation, circleGroup](screenshots/p6_01_app_v4_pane_circles.png)

![app.js: legend circles and the NUST overlay](screenshots/p6_02_app_v4_legend_nust.png)

### Checkpoint 6

The full dashboard: 135 circles above the density shading, and the legend showing both the density classes and the circle sizes.

![Checkpoint 6a: circles above the density shading, legend with both parts](screenshots/checkpoint6a_dashboard_circles_above_density.png)

The NUST overlay at zoom 5 and zoom 10. At zoom 5 the 25 km `L.circle` is about 6 px across on screen, the same size as the 6 px `circleMarker`, so the two coincide. At zoom 10 the `L.circle` has grown to a radius of about 196 px while the `circleMarker` is still 6 px. Measured against the scale bar at zoom 10, 10 km is 79 px, so 25 km should be 197 px: the metre circle is drawn to scale.

![Checkpoint 6b: NUST overlay at zoom 5](screenshots/checkpoint6b_nust_overlay_zoom5.png)

![Checkpoint 6c: NUST overlay at zoom 10, the 25 km circle against the 10 km scale bar](screenshots/checkpoint6c_nust_overlay_zoom10.png)

---

## Part 7: Map events, on and off

`showCoordinates` is a named function so that `map.off('click', showCoordinates)` can find the very function `map.on` registered. The checkbox's `change` listener switches it on and off, and a `zoomend` handler keeps the info panel's zoom level current.

![app.js: showCoordinates, the checkbox listener, zoomend](screenshots/p7_01_app_v5_events.png)

### Checkpoint 7

With the checkbox ticked, a click on the sea south of Karachi opens a popup reading `23.8810, 66.6211`.

![Checkpoint 7: coordinate popup on the sea](screenshots/checkpoint7_coordinate_popup_on_sea.png)

**Notes from the three steps**

1. **Sea, then a district.** The sea click gave only the coordinate popup and the zoom stayed at 5, because no district layer was under the pointer. Clicking a district in western Balochistan ran both handlers: Leaflet fired the layer's `click` first, so `zoomToDistrict` zoomed the map to level 8 around the district, and the event then bubbled to the map, so `showCoordinates` opened a popup reading `28.3415, 65.0830` at the clicked point. The panel briefly showed the district's figures while the pointer was over it.

   ![Step 1: district click runs both handlers, zoom to 8 and a coordinate popup](screenshots/p7_02_click_district_both_handlers.png)

2. **The legend.** With the checkbox ticked, clicking the legend produced no popup, because `L.DomEvent.disableClickPropagation(div)` stops the click reaching the map. With that one line removed and the page reloaded, the same click opened a coordinate popup, `28.4575, 98.6572`, the location under the legend in the bottom-right corner. The line was then put back.

   ![Step 2: legend click with disableClickPropagation, no popup](screenshots/p7_03_click_legend_no_popup.png)

   ![Step 2: the line removed from app.js](screenshots/p7_04_legend_without_disableClickPropagation.png)

   ![Step 2: the same click without disableClickPropagation opens a popup](screenshots/p7_05_click_legend_popup_appears.png)

3. **Unticked.** After unticking the checkbox, `map.off` had removed the handler and clicks on the sea did nothing.

   ![Step 3: checkbox unticked, a sea click opens nothing](screenshots/p7_06_unticked_sea_click_nothing.png)

---

## Part 8: Filter by province (extension)

`fillProvinceList` builds the drop-down from the data and the `change` listener calls `draw(event.target.value)`, which already filters through the `keep` hook.

![app.js: fillProvinceList and the change listener](screenshots/p8_01_app_v6_province.png)

### Checkpoint 8

Gilgit Baltistan selected: the count reads 14 districts, the map has zoomed to the province, the layer control is open and its overlays still switch the rebuilt layers because they point at the two feature groups, not at the `L.geoJSON` layers inside them.

![Checkpoint 8: Gilgit Baltistan, 14 districts, layer control open](screenshots/checkpoint8_gilgit_baltistan_selected.png)

**Why no circles appear.** The 2023 census did not cover Gilgit-Baltistan, so all 14 districts have `pop_2023: null`. `hasPopulation` filters them out before `circleFor` runs, so the circle layer is rebuilt empty, while the districts are drawn grey as "no census data". The dashboard should say so: a silent empty layer reads as "nobody lives here". A one-line note in the count label, such as "14 districts, no census data", or a legend entry stating that circles are drawn only where a census value exists, would make the absence an explicit statement rather than an apparent fact.

---

## Part 9: SVG or canvas (extension)

`useCanvas` is read from the query string on the first line of `app.js`, `preferCanvas: useCanvas` was added to the map options, and `draw` now times itself and logs the result.

![app.js: useCanvas, preferCanvas and the timing in draw](screenshots/p9_01_app_v7_canvas_switch.png)

### Measurements

Each renderer was reloaded five times with the cache disabled and the time printed for `draw(all)` recorded.

| | SVG (`index.html`) | Canvas (`index.html?canvas`) |
|---|---|---|
| draw(all), five runs, ms | 30.3, 32.1, 35.5, 35.8, 37.2 | 21.1, 21.6, 22.7, 22.9, 30.9 |
| draw(all), median of five, ms | 35.5 | 22.7 |
| Elements inside `leaflet-overlay-pane` | one `svg` holding 162 elements: a `g` and 160 `path`s plus the NUST circle | one `canvas`, nothing inside it |
| Elements inside the `symbols` pane | one `svg` holding 136 elements: a `g` and 135 circle `path`s | one `canvas` |
| Hover highlight still works? | Yes | Not on the districts while the circles are shown; see below |
| Can you inspect one district in Elements? | Yes, each district is a `path` with its own attributes | No, the canvas is a single element with pixels inside |

### Checkpoint 9

![Checkpoint 9a: Elements tab in SVG mode, the overlay pane holds an svg of paths](screenshots/checkpoint9a_elements_svg_mode.png)

![Checkpoint 9b: Elements tab in canvas mode, the overlay pane holds one canvas](screenshots/checkpoint9b_elements_canvas_mode.png)

![Hover highlight in SVG mode](screenshots/p9_02_svg_hover_highlight.png)

![Canvas mode: the pointer over a district does not highlight it while the circles' canvas lies above](screenshots/p9_03_canvas_hover_highlight.png)

**The hover result, explained.** In canvas mode each pane gets its own `canvas` element that covers the whole map. The symbols pane sits at z-index 450 above the overlay pane, so every mouse move lands on the circles' canvas, whose renderer hit-tests only its own circles and never passes the event down to the districts' canvas underneath. The circle tooltips therefore still work, but the district highlight does not, even when the "Population" overlay is switched off, because the empty canvas is still there. Hiding the symbols pane altogether brings the district highlight back, which confirms the cause. In SVG mode the upper `svg` only captures the pointer where it has painted content, so the districts beneath remain reachable. The pane that solved the draw-order problem in Part 6 creates a pointer problem in canvas mode.

**Reading the result.** With 160 districts and 135 circles canvas was faster here, 22.7 against 35.5 ms, but both are well under a frame of perceptible delay and the difference is not what decides the choice. The lecture's guidance is that canvas starts to pay at a few thousand features. For the tehsil layer, administrative level 3, with several times as many features and more vertices each, the gap would widen in canvas's favour: SVG would have to create and keep thousands of `path` nodes in the DOM, each restyled on hover and each re-laid-out on every pan and zoom, while canvas repaints one bitmap. The cost of canvas is what this table shows: no per-feature element to inspect, and hit-testing that must be done by the renderer, with the pane interaction above as a consequence.

---

## Part 10: Publish and submit

### 10.1 Commit and push

```powershell
cd D:\MS\WebGIS\webgis-lab
git status --short
git add -A
git commit -m "Lab 3: district dashboard"
git push
git log --oneline
```

![git status](screenshots/p10_01_git_status.png)

![git add -A](screenshots/p10_02_git_add.png)

![The Lab 3 commit](screenshots/p10_03_git_commit.png)

![git push](screenshots/p10_04_git_push.png)

![git log: Lab 3 on top of the Lab 2 history](screenshots/p10_05_git_log.png)

GitHub Pages rebuilt the site from the existing configuration. The dashboard is live at `https://tcantbenormal.github.io/webgis-lab-537980/lab3/` and Lab 2 still works at its old address.

![The live lab3 page served by GitHub Pages](screenshots/p10_06_github_pages_lab3_live.png)

![Lab 2 still live at the root address](screenshots/p10_07_lab2_still_live.png)

### 10.2 Report

This report, with the screenshots, was added as `lab3/report.md` and `lab3/report.docx` in a second commit.

---

## Questions

**1. Lab 2 shaded districts by population. Name one large, thinly populated district and one small, crowded one, and explain how each would mislead on the Lab 2 map.**

Chagai in Balochistan covers about 44,500 km² with 269,000 people, a density of about 6 per km²; on the Lab 2 map it sat in the lowest population class and looked unremarkable, when in fact it is one of the emptiest places in the country, and its sheer size gave that pale colour a large visual weight. Lahore covers 1,730 km² with 13.0 million people, about 7,500 per km²; on the Lab 2 map it was in the darkest class, correctly, but so were several large rural districts whose counts are high only because they are big, so the reader could not tell a crowded district from a large one. Shading by density separates the two: Chagai drops to the palest class and Lahore stays the darkest, and the colour now says something about the place rather than about the size of the polygon.

**2. `radiusFor` takes a square root. What would the map suggest about Lahore against a district of 3 million if it did not?**

The eye compares the areas of circles, and area grows with the square of the radius. If the radius followed population directly, Lahore at 13 million would have a radius 4.3 times that of a 3-million district and therefore an area about 19 times larger, suggesting Lahore held nineteen times as many people rather than four. With the square root, the radii are in the ratio 2.1 and the areas in the ratio 4.3, which is the true ratio of the populations.

**3. Why does the layer control hold `districtGroup` rather than the `L.geoJSON` layer itself?**

Because `draw` throws the `L.geoJSON` layer away and builds a new one every time the province changes. A control that pointed at the old layer would switch on and off something that is no longer on the map, and would never see the new one. The feature group stays put while its contents change: `draw` clears it and adds the new layer inside it, so the control's checkbox keeps working after every rebuild, which Checkpoint 8 shows.

**4. What would go wrong if the circles were drawn in `overlayPane` instead of the `symbols` pane? Describe what the user would see when hovering.**

Polygons and circle markers are both vector paths, so in one pane whichever is drawn later covers the other; the circles, drawn after the districts, would start on top. But `highlight` calls `bringToFront` on the hovered district, which lifts it above everything else in the same pane. The user would see the circles over that district disappear under the highlighted polygon, then reappear when the pointer left, with the symbols flickering in and out as the mouse moved across the map. A pane with a higher z-index settles the order once, and `bringToFront` can only reorder within the polygons' own pane.

**5. Why can `map.off` remove `showCoordinates`, when it could not remove an anonymous function passed to `map.on`?**

`map.off` removes a handler by identity: it searches the registered handlers for the very function object you pass in. `showCoordinates` is a named function stored in a variable, so the same object can be passed to `on` and later to `off`, and the two match. An anonymous function written inline in `map.on('click', function (e) { ... })` has no name and no variable holding it; once the call returns there is no way to refer to that object again, and anything you passed to `off` would be a different function that matches nothing. The handler could never be removed.

**6. On the NUST overlay, which circle would you use to show a 25 km evacuation zone, and which to mark the campus on a national map? Why?**

The evacuation zone needs `L.circle` with a radius in metres: it represents a real distance on the ground, so it must grow and shrink with the zoom and measure 25 km against the scale bar at every level, as Checkpoint 6 shows. The campus marker on a national map needs `L.circleMarker` with a radius in pixels: it marks a location, not an extent, and it should stay a visible 6 px dot at zoom 5 rather than shrinking to nothing, which a 25 km `L.circle` does at that zoom, where it was about 6 px across and indistinguishable from the marker.

---

## Submission

- **Repository URL:** https://github.com/tcantbenormal/webgis-lab-537980 (folder `lab3`)
- **Live lab3 page:** https://tcantbenormal.github.io/webgis-lab-537980/lab3/
