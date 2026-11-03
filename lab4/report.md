# Web GIS Lab 04: Getting started with GeoDjango

## Part 1: Python and a first Django project

### 1.1 Check for Python

Python 3.14.7 was already installed from python.org, so no installer was needed. `py --list` shows one version, 3.14 (64-bit), and `where.exe python` lists the python.org copy first, ahead of the Microsoft Store alias.

![python --version: Python 3.14.7](screenshots/p1_01_python_version.png)

![py --list](screenshots/p1_02_py_list.png)

![pip --version, from Python 3.14](screenshots/p1_03_pip_version.png)

![where.exe python: the python.org copy comes first](screenshots/p1_04_where_python.png)

### 1.2 Create the project folder and a virtual environment

The project lives in the course folder as `Lab 4`, next to the earlier labs; the repository copy is the `lab4` folder of `webgis-lab-537980`.

```powershell
mkdir "Lab 4"
cd "Lab 4"
python -m venv venv
.\venv\Scripts\Activate.ps1
```

![mkdir Lab 4](screenshots/p1_05_mkdir_lab4.png)

![python -m venv venv](screenshots/p1_06_python_m_venv.png)

![Activate.ps1: the prompt now starts with (venv)](screenshots/p1_07_activate.png)

### 1.3 Install Django and the PostgreSQL driver

```powershell
pip install django "psycopg[binary]"
pip freeze > requirements.txt
python -m django --version
```

![pip install django psycopg[binary]](screenshots/p1_08_pip_install_django_psycopg.png)

![pip freeze > requirements.txt](screenshots/p1_09_pip_freeze_requirements.png)

![python -m django --version: 6.1.2](screenshots/p1_10_django_version.png)

### 1.4 Start a project and an app

```powershell
django-admin startproject webgis .
python manage.py startapp districts
```

![django-admin startproject webgis .](screenshots/p1_11_startproject.png)

![python manage.py startapp districts](screenshots/p1_12_startapp.png)

### 1.5 Run it

`migrate` created the default SQLite database and `runserver` started the development server on port 8000.

![python manage.py migrate, SQLite](screenshots/p1_13_migrate_sqlite.png)

![python manage.py runserver](screenshots/p1_14_runserver.png)

### Checkpoint 1

The "install worked" page at `127.0.0.1:8000`, with Django 6.1.2 reported by `python -m django --version` above.

![Checkpoint 1: the install worked page](screenshots/checkpoint1_install_worked.png)

![The admin login page at /admin/, no user yet](screenshots/p1_16_admin_login_page.png)

The server was stopped and `db.sqlite3` deleted, because SQLite cannot store geometry properly.

![db.sqlite3 removed](screenshots/p1_17_delete_db_sqlite3.png)

---

## Part 2: Install PostgreSQL and PostGIS

PostgreSQL 18 and the PostGIS 3.6 bundle were already installed on this machine from Stack Builder, with pgAdmin 4 and the command-line tools. The service `postgresql-x64-18` runs on port 5432.

### 2.3 Create a spatial database

In pgAdmin, Databases, Create, Database, named `webgis`; then in the Query Tool:

```sql
CREATE EXTENSION postgis;
SELECT postgis_full_version();
```

![pgAdmin connected to PostgreSQL 18](screenshots/p2_01_pgadmin_connected.png)

![Databases, Create, Database](screenshots/p2_02_pgadmin_create_database_menu.png)

![The new database named webgis](screenshots/p2_03_create_database_webgis.png)

![CREATE EXTENSION postgis](screenshots/p2_04_create_extension_postgis.png)

### Checkpoint 2

`postgis_full_version()` returns one line listing PostGIS 3.6.2, PostgreSQL 18, GEOS 3.14.1 and PROJ 8.2.1: proof that the database can hold geometry.

![Checkpoint 2: postgis_full_version() in the webgis database](screenshots/checkpoint2_postgis_full_version.png)

---

## Part 3: Connect Django to PostGIS

### 3.1 GDAL, GEOS and PROJ

OSGeo4W was already installed at `C:\OSGeo4W` for Lab 2, with GDAL, so nothing new was needed.

### 3.2 Store the password outside the code

```powershell
setx WEBGIS_DB_PASSWORD "..."
```

The variable is saved for every new window, so the terminal was closed, reopened and the environment activated again.

![setx WEBGIS_DB_PASSWORD](screenshots/p3_01_setx_db_password.png)

![setx confirmed, then deactivate](screenshots/p3_02_setx_and_deactivate.png)

![A new window, environment activated again](screenshots/p3_03_reactivate_venv.png)

### 3.3 Edit the settings

The three changes to `webgis/settings.py`: the OSGeo4W block below `BASE_DIR`, `django.contrib.gis` and `districts` in `INSTALLED_APPS`, and the PostGIS `DATABASES` entry whose password comes from the environment variable.

![settings.py: OSGeo4W paths](screenshots/p3_04_settings_osgeo4w_paths.png)

![settings.py: INSTALLED_APPS with django.contrib.gis and districts](screenshots/p3_05_settings_installed_apps.png)

![settings.py: DATABASES pointing at PostGIS](screenshots/p3_06_settings_databases.png)

### 3.4 Check each piece separately

```powershell
python manage.py shell -c "from django.contrib.gis import gdal, geos; print(gdal.gdal_version(), geos.geos_version())"
python manage.py check
python manage.py migrate
```

![GDAL 3.13.3 and GEOS 3.15.0 loaded by Python](screenshots/p3_07_gdal_geos_versions.png)

![manage.py check: no issues](screenshots/p3_08_manage_check.png)

### Checkpoint 3

`migrate` logged in to PostGIS and created Django's own tables there.

![Checkpoint 3: migrate against PostGIS](screenshots/checkpoint3_migrate_postgis.png)

---

## Part 4: A model with a geometry

### 4.1 The model

![districts/models.py](screenshots/p4_01_models_py.png)

### 4.2 From model to table

```powershell
python manage.py makemigrations districts
python manage.py sqlmigrate districts 0001
python manage.py migrate
```

![makemigrations districts](screenshots/p4_02_makemigrations.png)

### Checkpoint 4

The SQL of migration 0001. The two lines that matter: `"geom" geometry(MULTIPOLYGON,4326) NOT NULL`, a real PostGIS column constrained to multipolygons in EPSG:4326, and `CREATE INDEX ... USING GIST ("geom")`, the spatial index GeoDjango adds to every geometry field without being asked.

![Checkpoint 4: sqlmigrate districts 0001](screenshots/checkpoint4_sqlmigrate.png)

![migrate applies districts.0001_initial](screenshots/p4_04_migrate_districts.png)

**A correction made later.** In the first version of `models.py` the `class Meta` and `__str__` were written at module level rather than indented inside `District`. Django accepted the file, because at module level they are simply an unrelated class and a function, but the model had no ordering and districts showed in the admin as "District object (112)". The two blocks were indented into the class, which changes only the model's options, so `makemigrations` produced a tiny second migration, `0002_alter_district_options`, and `migrate` applied it.

![models.py corrected: Meta and __str__ inside the class](screenshots/p4_05_models_py_fixed.png)

![makemigrations: Change Meta options on district](screenshots/p4_06_makemigrations_meta.png)

![migrate applies 0002](screenshots/p4_07_migrate_meta.png)

![showmigrations districts: both applied](screenshots/p4_08_showmigrations.png)

---

## Part 5: Load the districts

### 5.1 The data file

```powershell
mkdir data
copy "..\Lab 3\data\districts.geojson" data\districts.geojson
```

![mkdir data](screenshots/p5_01_mkdir_data.png)

![Copy districts.geojson from Lab 3](screenshots/p5_02_copy_districts_geojson.png)

### 5.2 A loading script

![New-Item districts\load.py](screenshots/p5_03_new_item_load_py.png)

![districts/load.py](screenshots/p5_04_load_py.png)

The script reported the layer as 160 features of **Unknown** geometry type, because the file mixes 152 Polygon and 8 MultiPolygon features, and saved 160 districts.

![load.run(): 160 features, Unknown geometry, 160 districts saved](screenshots/p5_05_load_run_160.png)

### 5.3 Talk to the data

![python manage.py shell](screenshots/p5_06_shell_start.png)

### Checkpoint 5

The seven ORM lines: 160 districts, 29 in Sindh, 25 with no census figure; Lahore has 13,004,135 people, a MultiPolygon geometry of 238 coordinates.

![Checkpoint 5: the seven shell lines](screenshots/checkpoint5_shell_seven_lines.png)

---

## Part 6: The admin panel

### 6.1 Create an administrator, 6.2 register the model

![createsuperuser](screenshots/p6_01_createsuperuser.png)

![districts/admin.py with GISModelAdmin](screenshots/p6_02_admin_py.png)

### 6.3 Explore it

![The district list in the admin](screenshots/p6_03_admin_district_list.png)

![Search for karachi: six districts, all in Sindh](screenshots/p6_04_admin_search_karachi.png)

![Filtered to Sindh and sorted by population, West Karachi first](screenshots/p6_05_admin_sorted_by_population.png)

### Checkpoint 6

The list filtered to one province (Sindh, sorted by population, above); Lahore's page with its geometry on the OpenLayers map; the list after Lahore's population was changed to 1,500,000 and saved, with the admin's success message; and the pgAdmin query confirming the database row had changed.

![Checkpoint 6: Lahore's page with the map](screenshots/checkpoint6b_lahore_page_map.png)

![Checkpoint 6: the list after the change was saved, Lahore now 1500000](screenshots/checkpoint6a_filtered_list_lahore_changed.png)

![Checkpoint 6: pgAdmin shows pop_2023 = 1500000 for Lahore](screenshots/checkpoint6c_pgadmin_lahore_changed.png)

The figure was then set back to 13,004,135 and the same query run again in pgAdmin.

![pgAdmin: Lahore restored to 13004135](screenshots/p6_06_pgadmin_lahore_restored.png)

---

## Part 7: Leaflet, fed by Django

### 7.1 Two views, 7.2 two URLs

![districts/views.py](screenshots/p7_01_views_py.png)

![New-Item districts\urls.py](screenshots/p7_02_new_item_urls_py.png)

![districts/urls.py](screenshots/p7_03_districts_urls_py.png)

![webgis/urls.py includes districts.urls](screenshots/p7_04_webgis_urls_py.png)

`/api/districts/` returns a GeoJSON FeatureCollection built from PostGIS, and `?province=Sindh` returns 29 features instead of 160.

![/api/districts/: GeoJSON from the database](screenshots/p7_05_api_districts_json.png)

![/api/districts/?province=Sindh](screenshots/p7_06_api_districts_sindh.png)

### 7.3 The map page

![New-Item map.html in districts/templates/districts](screenshots/p7_07_new_item_map_html.png)

![districts/templates/districts/map.html](screenshots/p7_08_map_html_editor.png)

**What went wrong, and the fix.** The first attempt drew the 160 districts but no basemap. The tile URL in `map.html` had been edited to `https://openstreetmap.org{z}/{x}/{y}.png`, which loses the `tile.` host and the slash before `{z}`, so every tile request went to a non-existent address.

![The first attempt: districts but no basemap](screenshots/p7_09_map_without_basemap.png)

The line was put back to the handout's `https://tile.openstreetmap.org/{z}/{x}/{y}.png` and the server restarted in its own window.

![Activate the environment](screenshots/p7_10_activate_venv.png)

![map.html: the tile URL corrected](screenshots/p7_11_map_html_tile_fix.png)

![Starting runserver in a second window](screenshots/p7_12_start_runserver.png)

![The runserver window answering requests](screenshots/p7_13_runserver_window.png)

Ctrl+U shows the page as it arrived from Django: the template tag has been replaced, so the browser reads `const DISTRICTS_URL = "/api/districts/";`.

![view-source: the url tag rendered as /api/districts/](screenshots/p7_14_view_source_districts_url.png)

With the correct URL the tiles arrived, but as 256 by 256 "Access blocked" placeholders with status 403: OpenStreetMap's volunteer servers refused the requests, citing their tile usage policy. The same URL fetched directly from the command line returns a real tile, so the block is applied to the request pattern of this page, served from `127.0.0.1:8000`, rather than to the machine.

![OSM tiles returned as Access blocked placeholders](screenshots/p7_15_osm_tiles_access_blocked.png)

Since the basemap is only a backdrop for the districts, the page was switched to Esri's free Light Gray Canvas tiles, the same service used in Lab 3, with its `{z}/{y}/{x}` order and attribution. Nothing else in the page changed.

![map.html: Esri Light Gray Canvas as the basemap](screenshots/p7_16_map_html_basemap_esri.png)

### Checkpoint 7

The map at `127.0.0.1:8000` with the basemap drawn, the 160 districts coloured by province, and the tooltip for Lahore, Punjab.

![Checkpoint 7: the map with a tooltip](screenshots/checkpoint7a_map_basemap_tooltip.png)

The Network tab with the `api/districts/` request selected: status 200, type fetch, 1,027 kB in 317 ms from the Django development server.

![Checkpoint 7: the api/districts/ request, 1,027 kB](screenshots/checkpoint7b_network_api_districts_size.png)

---

## Part 8: Ask PostGIS a spatial question (extension)

### 8.1 The view

`district_at` reads `lat` and `lng` by name, builds `Point(lng, lat, srid=4326)` and asks for the first district whose geometry contains it; `geom__contains` becomes `ST_Contains` in SQL. The URL `api/where/` was added to `districts/urls.py`.

![views.py: district_at](screenshots/p8_01_views_district_at.png)

![urls.py with api/where/](screenshots/p8_02_urls_where.png)

Tested directly: the NUST coordinates name Islamabad with its population, a point in the sea returns `district: null`, and a bad argument returns status 400.

![/api/where/?lat=33.6423&lng=72.9906: Islamabad](screenshots/p8_04_api_where_islamabad.png)

![/api/where/ for a point in the sea: null](screenshots/p8_05_api_where_sea.png)

### 8.2 Call it from the map

![map.html: WHERE_URL and the click handler](screenshots/p8_03_map_html_click_handler.png)

### Checkpoint 8

A click on Islamabad opens a popup built from PostGIS's answer; a click on the sea south of Karachi reports "Not inside any district".

![Checkpoint 8: popup from a click, answered by PostGIS](screenshots/checkpoint8a_click_popup_from_postgis.png)

![A click on the sea: not inside any district](screenshots/p8_06_click_sea_not_inside.png)

### 8.3 The same question in SQL

![pgAdmin: ST_Contains names Islamabad](screenshots/p8_07_pgadmin_st_contains.png)

![Checkpoint 8: the area query](screenshots/checkpoint8b_pgadmin_area_query.png)

| District | Latitude | stored km² | geodesic km² | web_mercator km² | Mercator / geodesic | 1/cos²(lat) |
|---|---|---|---|---|---|---|
| Gwadar | 25.4 N | 11,574 | 11,574 | 14,244 | 1.23 | 1.23 |
| Lahore | 31.5 N | 1,730 | 1,730 | 2,385 | 1.38 | 1.37 |
| Gilgit | 35.9 N | 4,016 | 4,015 | 6,133 | 1.53 | 1.52 |

The stored `area_km2` and the geodesic area agree to the nearest square kilometre, because the stored figure was itself computed on the ellipsoid. The Web Mercator area is too large by exactly the factor 1/cos²(latitude) predicted in Lab 2: 23 percent at Gwadar on the coast, 38 percent at Lahore, 53 percent at Gilgit in the north. This is Lab 2's Part 9 in one SQL statement, and it says the same thing: never report an area computed in EPSG:3857.

---

## Part 9: Commit and submit

### 9.1 What not to commit

![lab4/.gitignore](screenshots/p9_01_gitignore.png)

### Versions on this machine

![Every version number](screenshots/p9_02_versions.png)

| Component | Version |
|---|---|
| Python | 3.14.7 (python.org, 64-bit) |
| Django | 6.1.2 |
| psycopg | 3.3.6 (binary) |
| PostgreSQL | 18.6 on x86_64-windows |
| PostGIS | 3.6.2, with GEOS 3.14.1 and PROJ 8.2.1 inside the database |
| GDAL (GeoDjango, from C:\OSGeo4W) | 3.13.3 |
| GEOS (GeoDjango, from C:\OSGeo4W) | 3.15.0 |
| OSGeo4W | C:\OSGeo4W, installed for Lab 2 |
| pgAdmin 4 | bundled with PostgreSQL 18 |

### Installation errors met, and what fixed them

1. **pgAdmin: "connection timeout expired" when connecting to the server.** On first use pgAdmin showed "Multiple connection attempts failed. All failures were: host 'localhost', port 5432 ... connection timeout expired" for both `::1` and `127.0.0.1`. The PostgreSQL service had not finished starting after the installer; waiting and retrying the connection succeeded, and the service has run normally since.

2. **Districts shown as "District object (112)" in the admin, and no ordering.** `class Meta` and `def __str__` had been written at module level, outside `District`, so the model had neither. Indenting them into the class fixed it; `makemigrations` then produced `0002_alter_district_options` for the new `ordering`, which `migrate` applied. No data changed.

3. **Map page drew districts but no basemap.** The tile URL in `map.html` had been changed to `https://openstreetmap.org{z}/{x}/{y}.png`, dropping the `tile.` host and the slash before `{z}`. Restoring the handout's `https://tile.openstreetmap.org/{z}/{x}/{y}.png` made the tile requests go to the right address.

4. **OpenStreetMap answered with "Access blocked" tiles (HTTP 403).** With the URL corrected, every tile came back as a placeholder image reading "App is not following the tile usage policy of OpenStreetMap's volunteer-run servers". The request from the page is refused while the same tile fetched by hand is served, so the policy is applied to the page's request pattern. The basemap was switched to Esri's free Light Gray Canvas, which needs no key and was already used in Lab 3; the districts, API and interaction are unaffected.

5. **`requirements.txt` written as UTF-16.** PowerShell's `>` redirection wrote the file in UTF-16 with a byte-order mark, which `pip install -r` on another machine may not read. The repository copy was re-encoded to UTF-8; the content is identical.

Nothing else went wrong: Python, OSGeo4W, PostgreSQL and PostGIS were already installed from earlier work, and every `manage.py` command ran first time.

### 9.2 Commit and push

The project was copied into the course repository as `lab4`, without `venv`, and pushed.

```powershell
cd D:\MS\WebGIS\webgis-lab
git status --short
git add -A
git commit -m "Lab 4: GeoDjango with PostGIS, admin and Leaflet"
git push
git log --oneline
```

![git status: lab4 untracked](screenshots/p9_03_git_status.png)

![git add -A: 22 files, no venv](screenshots/p9_04_git_add.png)

![The Lab 4 commit](screenshots/p9_05_git_commit.png)

![git push](screenshots/p9_06_git_push.png)

![git log](screenshots/p9_07_git_log.png)

This lab has no live URL: GitHub Pages serves files and cannot run Python or a database, so the project runs only on this machine. The submission is the repository and this report, added to `lab4/` as `report.md` and `report.docx` in a second commit.

![git add -A with the report and screenshots](screenshots/p9_08_git_add_report.png)

![The report commit](screenshots/p9_09_git_commit_report.png)

![git push](screenshots/p9_10_git_push_report.png)

![Final git log: both Lab 4 commits on top of Lab 3](screenshots/p9_11_git_log_final.png)

---

## Questions

**1. In Labs 2 and 3, every visitor downloaded the whole GeoJSON file. What can a page backed by Django and PostGIS do instead? Give two examples from this lab.**

It can send only what the visitor asked for, computed at the moment of asking. First, `/api/districts/?province=Sindh` makes the database do the filtering and returns 29 features rather than 160; the browser never receives the other provinces. Second, `/api/where/?lat=...&lng=...` sends a single point and gets back one small JSON answer, the district that contains it, instead of downloading every polygon and testing containment in JavaScript. Both answers come from the current table, so an edit in the admin is visible on the next request without anyone re-exporting a file.

**2. Why does `settings.py` read the database password from an environment variable, instead of containing the password itself?**

`settings.py` is committed to a public GitHub repository, and git keeps every version for ever, so a password written there is published and cannot be withdrawn by deleting it later. An environment variable lives only on the machine that runs the project; the committed file contains `os.environ.get("WEBGIS_DB_PASSWORD", "")`, which is harmless to publish, and each machine supplies its own value. The same pattern is used for any secret, and a server later in the course will have its own variable with its own password.

**3. In Part 4, the SQL ends with an index created `USING GIST`. What does it do, and which query in this lab benefits from it?**

A GiST index on the geometry column stores each district's bounding box in a tree, so a spatial query can discard every row whose box cannot possibly match without reading the geometry itself; only the few candidates whose boxes overlap are tested exactly. The query that benefits is Part 8's `District.objects.filter(geom__contains=point)`, which becomes `ST_Contains(geom, point)` in SQL: with the index PostGIS looks at the handful of districts whose boxes contain the point instead of running the containment test on all 160. GeoDjango creates the index on every geometry field without being asked, because without it every spatial query would be a full scan.

**4. The loading script wraps some geometries in a MultiPolygon. What would happen without that step, and why?**

The column was declared `geometry(MULTIPOLYGON, 4326)`, so PostGIS enforces the type on every insert. The file holds 152 plain Polygon features and 8 MultiPolygons, and GDAL reports the layer type as Unknown. Without the wrap, the first Polygon feature, Bagh, would be rejected with a geometry-type constraint error and the load would stop with nothing saved; the script's delete at the start would also have emptied the table. Wrapping each Polygon in a MultiPolygon of one part satisfies the column and changes nothing on the map. GeoDjango's `LayerMapping` shortcut refuses a mixed layer outright, which is why the script reads the features one by one.

**5. Who should have an admin login for a district dataset like this, and who should not?**

The admin is for the few people who maintain the data: whoever is responsible for keeping names, codes, census figures and boundaries correct, for example a data custodian at the bureau of statistics or the GIS officer who loaded the layer. Anyone who can log in can change or delete every row, and the change is an immediate UPDATE on the table. The public, students, analysts and the map's readers should not have a login; they get the data through the read-only API and the map page. Where someone needs to edit but not delete, the admin's own Users and permissions can grant change without delete, which is still more trust than a casual user should be given.

**6. Leaflet takes `[lat, lng]` and `Point` takes `(lng, lat)`. Where in this lab is each order used, and how does the extension's URL avoid confusing them?**

Latitude first is used wherever Leaflet is given a position by hand: `setView([30.3753, 69.3451], 5)`, `maxBounds: [[21.5, 58.5], [39.0, 80.5]]`, and the `e.latlng` object of a map click. Longitude first is used by everything that follows the GeoJSON and GEOS convention: the coordinates inside `districts.geojson` and the API's GeoJSON, `Point(lng, lat, srid=4326)` in the view, and `ST_MakePoint(72.9906, 33.6423)` in SQL. The extension's URL names the two numbers, `?lat=33.6423&lng=72.9906`, so the order in which they appear carries no meaning; the view reads `request.GET["lat"]` and `request.GET["lng"]` by name and puts them into `Point(lng, lat)` itself. The conversion between the two conventions therefore happens in exactly one place, inside the view, where it is written down.

---

## Submission

- **Repository URL:** https://github.com/tcantbenormal/webgis-lab-537980 (folder `lab4`)
- **Live URL:** none for this lab; the project runs only on the local machine.
