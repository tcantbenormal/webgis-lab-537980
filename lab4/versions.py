"""Print every version number the Lab 4 report asks for."""
import os, sys, platform, django, psycopg
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webgis.settings"); django.setup()
from django.db import connection
from django.contrib.gis import gdal, geos
c = connection.cursor()
c.execute("SELECT version()"); pg = c.fetchone()[0].split(",")[0]
c.execute("SELECT postgis_full_version()"); pgis = c.fetchone()[0]
print("Python    ", platform.python_version())
print("Django    ", django.get_version())
print("psycopg   ", psycopg.__version__)
print("PostgreSQL", pg)
print("PostGIS   ", pgis.split("[")[0].strip(), "|", pgis.split("GEOS=")[1].split('"')[1], "(GEOS in PostGIS) |", "PROJ", pgis.split('PROJ="')[1].split('"')[0].split()[0])
print("GDAL      ", gdal.gdal_version().decode(), "(GeoDjango, from C:\OSGeo4W)")
print("GEOS      ", geos.geos_version().decode(), "(GeoDjango, from C:\OSGeo4W)")
