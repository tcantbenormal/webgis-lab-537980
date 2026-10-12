# Web GIS Lab 02: District Explorer

## Part 1: Set up the project

### 1.1 Create the folder

```
cd D:\MS\WebGIS
mkdir webgis-lab
cd D:\MS\WebGIS\webgis-lab
mkdir data
```

![cd to the course folder](screenshots/p1_01_cd.png)

![mkdir webgis-lab](screenshots/p1_02_mkdir.png)

![cd into the project folder](screenshots/p1_03_cd_project.png)

![mkdir data](screenshots/p1_04_mkdir_data.png)

### 1.2 Create the repository

The GitHub repository `webgis-lab-537980` was created public with no README, .gitignore or licence. The folder was then connected to it:

```
git init
git branch -M main
git remote add origin https://github.com/tcantbenormal/webgis-lab-537980.git
```

![git init](screenshots/p1_05_git_init.png)

![git branch -M main](screenshots/p1_06_git_branch.png)

![git remote add origin](screenshots/p1_07_git_remote.png)

### 1.3 Create the three files

The three empty files were created in PowerShell and listed:

```
New-Item index.html, style.css, app.js -ItemType File
Get-ChildItem
```

![New-Item creates the three files](screenshots/p1_08_new_item_files.png)

![Get-ChildItem shows the four entries](screenshots/p1_09_dir.png)

### Checkpoint 1

The files `index.html`, `style.css`, `app.js` and the empty `data` folder have been created as required in the folder.

![Checkpoint 1: project folder with the three files and the data folder](screenshots/checkpoint1_project_folder.png)

## Part 2: Prepare the data

### 2.0 Tools and the LMS copy of the shapefile

GDAL and QGIS come with OSGeo4W, so their `bin` folder was added to the console's `PATH` and `PROJ_LIB` was pointed at OSGeo4W's own PROJ database.

![OSGeo4W tools on the PATH, ogrinfo version](screenshots/p2_01_osgeo_env.png)

The raw OCHA download was unzipped into `D:\MS\WebGIS\lab2-data\download\shp`, outside the project, so raw data is never committed. The admin level 2 layer `pak_admin2` has 160 features and the fields `adm2_name`, `adm1_name`, `adm2_pcode` and `area_sqkm`.

![cd to the working folder](screenshots/p2_02_cd_data.png)

![The adm2 components of the download](screenshots/p2_03_unzipped.png)

`The` four fields renamed to `district`, `province`, `pcode` and `area_km2` (one decimal) and joined `pop_2023` from the supplied `districts.geojson` on `pcode`. 135 districts receive a population and 25 stay empty, matching the handout.

![Writing data to districts](screenshots/p2_04_make_lms_copy.png)

### 2.1 Inspect what you were given

`ogrinfo -so` is the command-line form of Layer Properties, Information. It reports the geometry type, the feature count (160), the extent, the CRS (WGS 84, EPSG:4326) and the field types: `district`, `province`, `pcode` as String, `pop_2023` as Integer64 and `area_km2` as Real. The population column is numeric, so classification will work.

![ogrinfo: fields, types, CRS and feature count](screenshots/p2_05_ogrinfo_fields.png)

The five shapefile components add up to **4,123,167 bytes (4.12 MB)**.

![Shapefile component sizes and their sum](screenshots/p2_06_shapefile_size.png)

The layer was also opened in QGIS and the attribute table inspected with F6. The 24 Azad Kashmir and Gilgit-Baltistan districts show `NULL` population, as expected.

![The LMS copy loaded in QGIS](screenshots/p2_15_qgis_layer_loaded.png)

![Attribute table in QGIS: 160 features, population NULL in Azad Kashmir](screenshots/p2_16_qgis_attribute_table.png)

### 2.2 Version A: a straight conversion

```
ogr2ogr -f GeoJSON districts_A.geojson lms_copy\districts.shp -t_srs EPSG:4326
```

![Export A](screenshots/p2_07_export_A.png)

### 2.3 Version B: reduced coordinate precision

The `COORDINATE_PRECISION` layer option is the same setting as in the Save Features As dialog.

```
ogr2ogr -f GeoJSON districts_B.geojson lms_copy\districts.shp -t_srs EPSG:4326 -lco COORDINATE_PRECISION=5
```

![Export B with five decimal places](screenshots/p2_08_export_B.png)

### 2.4 Versions C and D: simplified geometry

Simplify was run twice on the original layer with the QGIS processing algorithm (method 0 is Douglas-Peucker, the distance method the dialog uses by default), then each result was exported with precision 5.

```
qgis_process-qgis-ltr.bat run native:simplifygeometries --INPUT=lms_copy\districts.shp --METHOD=0 --TOLERANCE=0.001 --OUTPUT=simplified_C.geojson
qgis_process-qgis-ltr.bat run native:simplifygeometries --INPUT=lms_copy\districts.shp --METHOD=0 --TOLERANCE=0.01  --OUTPUT=simplified_D.geojson
ogr2ogr -f GeoJSON districts_C.geojson simplified_C.geojson -lco COORDINATE_PRECISION=5
ogr2ogr -f GeoJSON districts_D.geojson simplified_D.geojson -lco COORDINATE_PRECISION=5
```

![Simplify, tolerance 0.001 degrees](screenshots/p2_09_simplify_C.png)

![Simplify, tolerance 0.01 degrees](screenshots/p2_10_simplify_D.png)

![Export C with precision 5](screenshots/p2_11_export_C.png)

![Export D with precision 5](screenshots/p2_12_export_D.png)

### 2.5 Record your measurements

![Sizes of the four GeoJSON versions](screenshots/p2_13_sizes.png)

| `Version` | `What was done` | `Size (bytes)` | `Size` | `% of A` |
|---|---|---|---|---|
| `Shapefile` | `.shp + .shx + .dbf + .prj + .cpg of the adm2 layer` | `4,123,167` | `4.12 MB` | `n/a (41%)` |
| `A` | `Straight conversion, default precision` | `10,081,114` | `10.08 MB` | `100%` |
| `B` | `Precision 5` | `5,074,003` | `5.07 MB` | `50.3%` |
| `C` | `Simplified 100 m, precision 5` | `916,160` | `0.92 MB` | `9.1%` |
| `D` | `Simplified 1 km, precision 5` | `220,409` | `0.22 MB` | `2.2%` |

For reference, the file supplied in the Lab 2 folder is 933,119 bytes, almost identical to version C, which suggests it was produced the same way.

**Why GeoJSON A is larger than the shapefile it came from.** A shapefile stores every coordinate as an 8-byte binary double, so 16 bytes per vertex regardless of the value. GeoJSON writes each coordinate as decimal text with up to 15 significant digits plus brackets, commas and spaces, about 40 bytes per vertex, and repeats every property name in every feature. The published download sizes quoted in the handout (24.3 MB shapefile bundle versus 27.7 MB GeoJSON) show the same effect; here the ratio is 2.4 to 1 because the adm2 `.dbf` is small. Cutting the precision to five decimals halves the file; throwing away vertices the eye cannot see at the map's scale removes another 80 percent.

Version C was copied into the project as the file the map will use:

```
copy districts_C.geojson D:\MS\WebGIS\webgis-lab\data\districts.geojson
```

![Copy version C into the project's data folder](screenshots/p2_14_copy_C.png)

### Checkpoint 2

Versions A (grey fill, dark outline) and D (red outline) drawn together in QGIS, zoomed to the district boundaries around Bagh and Muzaffarabad. The 1 km simplification cuts across every bend of the original line.

![Checkpoint 2: version A and version D together in QGIS](screenshots/checkpoint2_qgis_A_vs_D.png)

## Part 3: Read the data as text

### 3.1 Open it

Instead of VS Code's formatter, `python -m json.tool` wrote a formatted copy to a separate file. Formatting put every number on its own line and grew the file from 916,160 to 6,705,645 bytes, more than seven times, which is why the formatted copy is never the one served.

![Format a copy and compare sizes](screenshots/p3_01_format_copy.png)

![The first 38 lines of the formatted copy](screenshots/p3_02_formatted_head.png)

### 3.2 Find the structure

Each answer was read from the file with a one-line Python command.

![Outer object type](screenshots/p3_03_outer_type.png)

![Number of entries in features](screenshots/p3_04_feature_count.png)

![Geometry type of the first feature](screenshots/p3_05_geometry_type.png)

![Brackets before the first number](screenshots/p3_06_bracket_depth.png)

![Keys inside properties](screenshots/p3_07_property_keys.png)

### 3.3 Check the coordinate order and 3.4 that the rings close

![The first coordinate pair](screenshots/p3_08_first_pair.png)

![First and last pair of the outer ring](screenshots/p3_09_ring_closes.png)

### Checkpoint 3

1. **Type of the outermost object:** `FeatureCollection`.
2. **Entries in the features array:** 160, matching the QGIS feature count.
3. **Geometry type of the first feature:** `MultiPolygon`. The first feature is Bagh. In the raw shapefile it is a single polygon, but after simplification it is written as a MultiPolygon with one part, because the simplifier emits the general type for the layer.
4. **Levels of square bracket before the first number:** four, `[[[[73.53892, 34.12617], ...`. A MultiPolygon is a list of polygons, each a list of rings, each a list of positions, each a list of two numbers. For a plain Polygon it would be three.
5. **Keys inside properties:** `district`, `province`, `pcode`, `pop_2023`, `area_km2`.
**First coordinate pair:** `[73.53892, 34.12617]`. The first number is in the seventies and the second in the thirties, so the file is longitude first, latitude second, as GeoJSON requires. **Ring closure:** the outer ring of Bagh has 147 points and its first and last pairs are identical, so the ring is closed and valid.

## Part 4: Build the page

### 4.1 index.html and 4.2 style.css

Both files were written exactly as given in the handout. Their contents were listed from the console.

![index.html](screenshots/p4_01_index_html.png)

![style.css](screenshots/p4_02_style_css.png)

### 4.3 View it

The Live Server substitute was started in its own window from the project folder, so that `index.html` is the root of the site:

```
python -m http.server 5500 --bind 127.0.0.1
```

![Starting the server in a second console window](screenshots/p4_03_start_server.png)

![The server log: index.html, style.css and app.js served with status 200](screenshots/p4_04_server_window.png)

### Checkpoint 4

The page open at `http://127.0.0.1:5500` with the header, the empty panel reading `loading...`, and the empty map area. `app.js` is still empty at this point, so nothing is drawn into the 580 px tall map box.

![Checkpoint 4: header and empty map area on 127.0.0.1](screenshots/checkpoint4_empty_map.png)

## Part 5: Load the data with JavaScript

### 5.1 Create the map

The first version of `app.js` creates the map and the OpenStreetMap tile layer.

![app.js, first version](screenshots/p5_01_app_v1.png)

![A pannable map centred on Pakistan at zoom 5](screenshots/p5_02_map_centred_on_pakistan.png)

### 5.2 Keep the view on Pakistan

The `L.map` call was replaced with the version that sets `maxBounds`, `maxBoundsViscosity: 1.0` and `minZoom: 5`.

![app.js with the Pakistan limits](screenshots/p5_03_app_v2_bounds.png)

To test the limits, the map was asked to pan to central Europe (48 N, 10 E). Leaflet refused: the view stayed at 30.6 N, 69.5 E and the zoom-out button is greyed out at zoom 5.

![After an attempt to pan to Europe the map is still on Pakistan and cannot zoom out](screenshots/p5_04_maxbounds_stops_at_edge.png)

### 5.3 Fetch the file

`loadData` was added with `fetch`, the `response.ok` check and the three `console.log` lines.

![app.js with loadData](screenshots/p5_05_app_v3_fetch.png)

The Console shows `features: 160`, the first feature and its properties. 160 matches the QGIS feature count and the property names match the ones used in the next parts.

![Console after reload: feature count, first feature, properties](screenshots/p5_06_console_fetch_logs.png)

![The first feature expanded: geometry, properties, type](screenshots/p5_07_first_feature_expanded.png)

![Walking down geometry to coordinates: a MultiPolygon with one part of 147 points](screenshots/p5_08_walk_down_to_coordinates.png)

### 5.4 Try the array methods

The four expressions were typed into the Console one at a time.

![districts.features.length](screenshots/p5_09_console_length.png)

![map and slice: the first ten district names](screenshots/p5_10_console_map_slice.png)

![filter: Punjab has 36 districts](screenshots/p5_11_console_filter_punjab.png)

### Checkpoint 5

Feature count, the expanded first feature, and the distinct province list from `[...new Set(...)].sort()`: Azad Kashmir, Balochistan, Gilgit Baltistan, Islamabad, Khyber Pakhtunkhwa, Punjab, Sindh. This is the list that fills the drop-down in Part 8.

![Checkpoint 5: feature count, expanded first feature and the seven provinces](screenshots/checkpoint5_console.png)

## Part 6: Draw it with Leaflet

### 6.1 Add the layer

`draw(features)` was added with the two guards, and `draw(districts.features)` called at the end of `loadData`.

![app.js with draw](screenshots/p6_01_app_v4_draw.png)

![160 districts drawn in grey, the count label updated](screenshots/p6_02_districts_drawn.png)

### 6.2 Check the network activity

With **Disable cache** ticked and the page reloaded, the Network tab lists 22 requests and 1.3 MB transferred. The GeoJSON request is 916 kB and took 10 ms from the local server. Fifteen requests end in `.png`: the map tiles for zoom 5.

![Network tab, all requests, with districts.geojson at 916 kB in 10 ms](screenshots/p6_05_network_all_requests.png)

![Fetch/XHR filter: the single GeoJSON request](screenshots/p6_03_network_geojson_request.png)

![Img filter: the tile requests](screenshots/p6_04_network_tiles_only.png)

![districts.geojson selected](screenshots/p6_06_geojson_selected.png)

### Checkpoint 6

One tile selected with its Preview open: a single 256 by 256 `image/png`, 25.8 kB. Its URL is `https://tile.openstreetmap.org/5/23/12.png`. The three numbers are zoom 5, column 23 and row 12; the first is the zoom level.

![Checkpoint 6: a selected tile request with its Preview](screenshots/checkpoint6_tile_preview.png)

Panning the map made six new tile requests arrive; the count of `.png` requests rose from 15 to 21.

![After a pan: new tile requests at the bottom of the list](screenshots/p6_07_pan_new_tile_requests.png)

### Throttling the connection

The throttle was set to **3G** and the page reloaded. The GeoJSON now takes 26.6 s instead of 10 ms and the page finishes after 31.7 s.

![3G throttle: districts.geojson in 26.59 s, finish 31.73 s](screenshots/p6_08_network_throttled_3G.png)

Version A was then copied over `data/districts.geojson` and the throttled reload repeated. The 10 MB file took 3.5 minutes. Version C was restored afterwards and the throttle set back to No throttling.

![Substituting version A](screenshots/p6_09_substitute_A.png)

![3G throttle with version A: 10,081 kB in 3.5 minutes](screenshots/p6_10_network_throttled_3G_version_A.png)

![Restoring version C](screenshots/p6_11_restore_C.png)

![Throttle back to No throttling](screenshots/p6_12_throttle_back_to_none.png)

**Load time table**

| `Condition` | `File served` | `Transfer size` | `districts.geojson time` | `Page finish` |
|---|---|---|---|---|
| `No throttling, cache disabled` | `Version C` | `916 kB` | `10 ms` | `574 ms` |
| `3G preset` | `Version C` | `916 kB` | `26.59 s` | `31.73 s` |
| `3G preset` | `Version A` | `10,081 kB` | `3.5 min (209.9 s)` | `3.6 min` |

On a 3G connection the straight conversion takes seven times longer than the simplified file; everything else on the page (CSS, JavaScript, fifteen tiles) is finished within the first 9 s in both cases.

## Part 7: Classify and add a popup

### 7.1 Shade by population, 7.2 Add a popup, 7.3 Add a legend

`show`, `colourFor` and `styleFor` were added above `draw`; the fixed `fillColor` was replaced with `style: styleFor`; `onEachFeature` binds the popup through `show`; and the legend control was appended at the end of the file.

![app.js with the classification, popup and legend code](screenshots/p7_01_app_v5_classify_popup_legend.png)

![The map shaded by population with the legend](screenshots/p7_02_shaded_map_with_legend.png)

**Classification breaks:** five classes with breaks at 300,000, 750,000, 1,500,000 and 3,000,000, plus a grey class for districts with no census value. The breaks roughly double at each step, so each class is visually distinct across a range that runs from a few tens of thousands (Hunza, Awaran) to thirteen million (Lahore); equal intervals would put all but a handful of districts in the lowest class. The 25 districts without a census figure are drawn grey rather than falling into the lowest class, so "no data" is never mistaken for "sparsely populated".

### Checkpoint 7

The shaded map with the legend and the popup for Lahore open: Province Punjab, Population 13,004,135, Area 1,729.9 km².

![Checkpoint 7: shaded map, legend and one popup](screenshots/checkpoint7_shaded_legend_popup.png)

## Part 8: Filter with a control (extension)

`fillProvinceList()` builds the options from the data and is called before `draw` in `loadData`; the `change` listener filters the features and redraws.

![app.js with fillProvinceList and the change listener](screenshots/p8_01_app_v6_filter.png)

### Checkpoint 8

![Checkpoint 8a: all provinces, 160 districts](screenshots/checkpoint8a_all_provinces.png)

![Checkpoint 8b: Khyber Pakhtunkhwa selected, 35 districts, map zoomed to the province](screenshots/checkpoint8b_single_province.png)

## Part 9: Measure the coordinate systems (extension)

### 9.1 Produce two projected copies

```
ogr2ogr -f GeoJSON d_3857.geojson  lms_copy\districts.shp -t_srs EPSG:3857
ogr2ogr -f GeoJSON d_32643.geojson lms_copy\districts.shp -t_srs EPSG:32643
```

![Export in EPSG:3857, Web Mercator](screenshots/p9_01_export_3857.png)

![Export in EPSG:32643, UTM zone 43N](screenshots/p9_02_export_32643.png)

### 9.2 Compute areas in each

The Field Calculator step was done with OGR SQL. `OGR_GEOM_AREA` is the planar area in the layer's own coordinate system, the same quantity QGIS's `$area` gives when the project ellipsoid is set to None, so the two layers give different numbers for the same district.

```
ogr2ogr -f GeoJSON d_3857_area.geojson  d_3857.geojson  -sql "SELECT *, OGR_GEOM_AREA / 1000000 AS area_calc FROM districts"
ogr2ogr -f GeoJSON d_32643_area.geojson d_32643.geojson -sql "SELECT *, OGR_GEOM_AREA / 1000000 AS area_calc FROM districts"
```

![area_calc added to the Web Mercator copy](screenshots/p9_03_area_field_3857.png)

![area_calc added to the UTM copy](screenshots/p9_04_area_field_32643.png)

![The new field and the CRS confirmed with ogrinfo](screenshots/p9_05_check_field.png)

### 9.3 Compare

Five districts from the south coast to the far north, compared with `compare_crs.py`:

![The comparison table](screenshots/p9_06_compare.png)

| `District` | `Latitude` | `3857 km²` | `UTM km²` | `% difference` | `1/cos²(lat)` | `Measured ratio` |
|---|---|---|---|---|---|---|
| `South Karachi` | `24.89` | `619.6` | `515.7` | `20.1%` | `1.215` | `1.201` |
| `Sukkur` | `27.55` | `6,608.0` | `5,217.1` | `26.7%` | `1.272` | `1.267` |
| `Multan` | `29.93` | `4,875.0` | `3,656.2` | `33.3%` | `1.331` | `1.333` |
| `Islamabad` | `33.65` | `1,305.1` | `901.5` | `44.8%` | `1.443` | `1.448` |
| `Hunza` | `36.55` | `17,744.0` | `11,410.5` | `55.5%` | `1.550` | `1.555` |

### Checkpoint 9: answers

1. **Does the difference grow or shrink northwards?** It grows, from 20 percent at Karachi to 55 percent at Hunza. Web Mercator stretches both axes by 1/cos(latitude), so the error increases steadily with latitude.
2. **Predicted inflation factor.** For Islamabad at 33.65 N, 1/cos²(33.65°) = 1.443. The measured ratio of the two areas is 1,305.1 / 901.5 = 1.448. The prediction is within 0.4 percent of the measurement; the small residual is because a district spans a range of latitudes and the UTM figure itself carries a scale factor of up to 0.9996 to 1.0010 away from the zone's central meridian. The lecture's "about 40 percent too large" at this latitude is confirmed.
3. **Which figure goes in a report?** The UTM zone 43N value. It is computed in a conformal projection designed for this longitude band, with distortion below 0.1 percent, so the number is a real area in square kilometres. The Web Mercator figure is only a measure of how much screen the district covers; it is never a quantity to report. Store in EPSG:4326, display in EPSG:3857, measure in EPSG:32642 or 32643.
## Part 10: Publish and submit

### 10.1 Commit and push

```
git status
git add -A
git commit -m "District Explorer: map, classification, filter"
git push -u origin main
```

![git status before staging](screenshots/p10_01_git_status.png)

![git add -A](screenshots/p10_02_git_add.png)

![The first commit](screenshots/p10_03_git_commit.png)

![git log](screenshots/p10_04_git_log.png)

![git push -u origin main](screenshots/p10_05_git_push.png)

### 10.2 Turn on hosting

GitHub Pages was enabled from the `main` branch, root folder. The site returned 404 while it was being built and then 200.

![The live page served by GitHub Pages](screenshots/p10_06_github_pages_live.png)

### 10.3 Report

The report, the checkpoint screenshots and the measurement tables were then committed and pushed as a second commit, so the repository history reads: page, map and data first; report second.

![git add -A with the report and screenshots](screenshots/p10_07_git_add_report.png)

![The report commit](screenshots/p10_08_git_commit_report.png)

![git push](screenshots/p10_09_git_push_report.png)

![Final git log](screenshots/p10_10_git_log_final.png)

## Questions

**1. Version D is far smaller than version A. Give one situation in which version D would be the wrong choice.**

Any map where the user zooms in to a single district or a city. At tolerance 0.01 degrees, about 1 km, a boundary is reduced to a few dozen straight segments; at zoom 10 or closer those segments are visibly wrong, shared borders may open into slivers, and a point that is really inside a district can fall outside its simplified polygon. Version D is right for a thumbnail or a country overview and wrong for anything that will be inspected or queried locally.

**2. The page makes one request for your GeoJSON file and dozens for tiles. Explain the difference in how those two kinds of data reach the browser.**

The GeoJSON is vector data: one file holding every coordinate of every district, fetched once by `fetch`, parsed into JavaScript objects, and drawn by Leaflet in the browser. After that one transfer, panning, zooming, filtering and styling cost no further requests. The tiles are raster data: the basemap is pre-rendered by the server into 256 by 256 pixel images for every zoom level, and the browser only asks for the squares that cover the current view at the current zoom. Each square is its own HTTP request, so the number of tile requests grows every time the view changes, while the vector layer is still the single file loaded at the start.

**3. Why does the map container need a height when the heading does not?**

An `h1` contains text, and a block element's default height grows to fit its content. The map `div` is empty, so its natural height is zero. Leaflet draws into whatever box it is given and does not enlarge it, so without the `height: calc(100vh - 150px)` rule it would render a map zero pixels tall, with no error and a clean console.

**4. `draw` removes the existing layer before adding a new one. What would go wrong if it did not?**

`L.geoJSON(...).addTo(map)` adds a layer; it never replaces one. Without `map.removeLayer(layer)`, each change of the drop-down would stack a new layer on top of the old ones: the previously drawn provinces would still be visible under the new selection, popups from several layers would overlap, and the map would slow down with every change as the number of polygons kept growing. The count label would also lie, because it reports the new subset while the old features are still drawn.

**5. A classmate's districts all appear in the same colour. List two possible causes and how you would tell them apart.**

Cause one: the population values cannot be read as numbers, for example `"1,500,000"` with a thousands separator, `" 95000"` with a stray space, or a placeholder like `"NA"`. Every comparison in `colourFor` is then false and each feature falls through to the lowest class. Cause two: the property name in the code does not match the data, for example `pop2023` or `Pop_2023`, so `feature.properties.pop_2023` is `undefined` for every district and the first line of `colourFor` paints them all grey. To tell them apart: look at the colour. All grey means the value is `undefined` or `null`, so check the property name in the Console with `districts.features[0].properties`. All the palest orange means the values exist but failed the numeric comparisons, so check `typeof districts.features[0].properties.pop_2023` and look at the attribute table for separators or text.

**6. You open the page by double-clicking `index.html` instead of using Live Server. The basemap appears but the districts do not. Explain why.**

Opened from the file system, the page has a `file:///` address and no proper web origin. Leaflet, its CSS and the OpenStreetMap tiles all come from `https://` servers, which the browser is happy to load from any page, so the basemap appears. `fetch('data/districts.geojson')`, however, is a request from a `file://` page to another local file, which the browser blocks under its security rules; the promise rejects or returns a failed response, `districts` stays `null`, and `draw` never runs. Served from `http://127.0.0.1:5500`, the same relative URL is an ordinary same-origin request and works.

## Submission

- **Repository URL:** https://github.com/tcantbenormal/webgis-lab-537980
- **Live GitHub Pages URL:** https://tcantbenormal.github.io/webgis-lab-537980/