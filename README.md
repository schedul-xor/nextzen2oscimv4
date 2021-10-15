<del>Nextzen</del>Mapbox tiles -> OpenScienceMap v4 tiles converter
====

OpenScienceMap.org server isn't serving tile data anymore. To keep on using the [VTM tile renderer](https://github.com/mapsforge/vtm), you should change your tile provider, or launch your own tile provier.

*nextzen2oscimv4* is a oscimv4 tile server compatible with VTM renderer, using [tippecanoe](https://github.com/mapbox/tippecanoe) as a backend.

Installation
====

Install Required Softwares
----

 * [PostgreSQL](https://www.postgresql.org/) with [PostGIS extension](https://postgis.net/)
   * Usage of apt for Debian-based Linux distributions is OK
 * [Imposm3](https://imposm.org/)
   1. Download `imposm-0.XX.X-linux-x86-64.tar.gz` from https://github.com/omniscale/imposm3/releases
   2. Extract to `~/Documents`, which will create a directory like `~/Documents/imposm-0.XX.X-linux-x86-64`
 * [gdal](https://gdal.org/) ---- *Required for tegola-osm*
 * [tippecanoe](https://github.com/mapbox/tippecanoe) --- *Required to convert mvt into geojson*
   1. Clone to `~/Documents`, which will create a directory like `~/Documents/tippecanoe`
   2. `cd tippecanoe`
   3. `make -j`
   4. `sudo make install`
   5. Check if `which tippecanoe-decode` returns `/usr/local/bin/tippecanoe-decode`
 * [tegola](https://tegola.io/)
   1. Download `tegola_linux_amd64.zip` from https://github.com/go-spatial/tegola/releases
   2. Extract to `~/Documents`
 * [tegola-osm](https://github.com/go-spatial/tegola-osm)
   1. Clone to `~/Documents`, which will create a directory like `~/Documents/tegola-osm`
 * `apt install python3-flask`
 * `apt install python3-protobuf`
 * `apt install python3-redis`
 * [Redis](https://redis.io/) --- *KVS server required for tegola data cache*
   1. `apt install redis redis-tools`
 * [supervisor](http://supervisord.org/) --- *Required to daemonize tegola server and nextzen2oscimv4 server*
   1. `apt install supervisor`
 * [nginx](https://nginx.org/) --- *HTTP reverse proxy*
   1. `apt install nginx`
    
 and nextzen2oscimv4, clone this directory to `~/Documents`, which will create a directory like `~/Documents/nextzen2oscimv4`.
 
Create PostgreSQL database
----
|Key|Value|
|----|----|
|PG Server Host|localhost|
|PG Server Port|5432|
|Database|osm|
|Username|osm_user|
|Password|osm_password|
|Additional extensions|`postgis`|

Using `psql`...
```
CREATE USER osm_user PASSWORD 'osm_password';
CREATE DATABASE osm OWNER osm_user;
\c osm
CREATE EXTENSION postgis;
```

Update OSM data
----

```
#!/usr/bin/env sh

cd ~/Documents

# Sample values
PG_CONNECTION_STRING=postgis://osm_user:osm_password@localhost/osm
OSM_FILE_PATH=/tmp/some_country.osm.pbf

# 1. Import osm data into your PostGIS server using imposm3
cd imposm-0.11.0-linux-x86-64
./imposm3 import -connection ${PG_CONNECTION_STRING} -mapping ../tegola-osm/imposm3.json -read ${OSM_FILE_PATH} -write
./imposm3 import -connection ${PG_CONNECTION_STRING} -mapping ../tegola-osm/imposm3.json -deployproduction
cd ../tegola-osm
./natural_earth.sh && ./osm_land.sh
psql -U tegola -h localhost -d osm -U osm_user -a -f postgis_helpers.sql
psql -U tegola -h localhost -d osm -U osm_user -a -f postgis_index.sql
psql -U tegola -h localhost -d osm -U osm_user -a -f postgis_building_fix.sql

rm -fr ../nextzen2oscimv4/tmp/geojson/*
rm -fr ../nextzen2oscimv4/tmp/mvt/*
redis-cli FLUSHALL
```

Check if tegola is working on port 22380
----
```
cd ~/Documents/
export TEGOLA_PORT=22380
export OSM_DB_HOST=localhost
export OSM_DB_PORT=5432
export OSM_DB_NAME=osm
export OSM_DB_USER=osm_user
export OSM_DB_PASS=osm_password
export NE_DB_HOST=localhost
export NE_DB_PORT=5432
export NE_DB_NAME=osm
export NE_DB_USER=osm_user
export NE_DB_PASS=osm_password
export CACHE_TYPE=redis
./tegola --config=./tegola-osm/tegola.toml serve
```
If your configuration has no problem, it should start an HTTP server at port 22380. Launch any web browser (Firefox, Chrome, ...) which supports WebGL, check if http://localhost:22380/ shows.

Daemonize tegola
----

Create a configuration file to `/etc/supervisor/conf.d/tegola.conf`.

Note: tegola is already built to use multi-core, so single program is needed.

```
[group:tegola]
programs=tegola22380

[program:tegola22380]
user=YOUR_USERNAME
environment=TEGOLA_PORT=22380,OSM_DB_HOST=localhost,OSM_DB_PORT=5432,OSM_DB_NAME=osm,OSM_DB_USER=osm_user,OSM_DB_PASS=osm_password,NE_DB_HOST=localhost,NE_DB_PORT=5432,NE_DB_NAME=osm,NE_DB_USER=osm_user,NE_DB_PASS=osm_password,CACHE_TYPE=redis
command=/absolute_path_to/Documents/tegola --config=/absolute_path_to/Documents/tegola-osm/tegola.toml serve
directory=/absolute_path_to/Documents/
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/absolute_path_to/tegola-22380.log
stdout_logfile_maxbytes=50MB
stdout_logfile_backups=50
stdout_capture_maxbytes=1MB
stdout_events_enabled=false
loglevel=info
```

save this file, let supervisord read the updated configurations.

```
supervisorctl reread
supervisorctl update
```

Test nextzen2oscimv4 with tegola:22380 backend
----
Create `tmp` path under `~/Documents/nextzen2oscim4`.

```
cd nextzen2oscim4
mkdir tmp
mkdir tmp/mvt
mkdir tmp/geojson
```

Check if flask app runs without error.

```
export PYTHONIOENCODING=utf-8
flask run --port=32400
```

Daemonize nextzen2oscimv4
----

Create a configuration file to `/etc/supervisor/conf.d/nextzen2oscimv4.conf`.

```
[group:nextzen2oscimv4]
programs=nextzen2oscimv432400,nextzen2oscimv432401

[program:nextzen2oscimv432400]
user=xor
environment=PYTHONIOENCODING=utf-8
command=flask run --port=32400
directory=/absolute_path_to/Documentsnextzen2oscimv4/
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/absolute_path_to/Documents/nextzen2oscimv4-32400.log
stdout_logfile_maxbytes=50MB
stdout_logfile_backups=50
stdout_capture_maxbytes=1MB
stdout_events_enabled=false
loglevel=info

[program:nextzen2oscimv432401]
user=xor
environment=PYTHONIOENCODING=utf-8
command=flask run --port=32401
directory=/absolute_path_to/Documents/nextzen2oscimv4/
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/absolute_path_to/Documents/nextzen2oscimv4-32401.log
stdout_logfile_maxbytes=50MB
stdout_logfile_backups=50
stdout_capture_maxbytes=1MB
stdout_events_enabled=false
loglevel=info
```

save this file, let supervisord read the updated configurations.

```
supervisorctl reread
supervisorctl update
```

Reverse proxy with nginx
----

First, add upstream urls to `/etc/nginx/nginx.conf`.
```
http {
:
:
        include /etc/nginx/conf.d/*.conf;
        include /etc/nginx/sites-enabled/*;

        # Add nextzen2oscimv4 upstreams
        upstream nextzen2oscimv4_frontends{
            server 127.0.0.1:32400;
            server 127.0.0.1:32401;
        }
}
```

Second, add proxy pass to `/etc/nginx/sites-enabled/default`

```
        location /tiles/oscimv4/ {
                rewrite /tiles/oscimv4/(.*) $1 break;
       add_header Access-Control-Allow-Origin *;
       add_header Access-Control-Allow-Methods "POST, GET, OPTIONS";
       add_header Access-Control-Allow-Headers "Origin, Authorization, Accept";
       add_header Access-Control-Allow-Credentials true;
                proxy_pass_header Server;
                proxy_set_header Host $http_host;
                proxy_set_header X-Proxy-User $remote_user;
                proxy_redirect off;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Scheme $scheme;
                proxy_set_header X-Domestic-ID hamamatsuchou;
                proxy_pass http://nextzen2oscimv4_frontends/vtm/$1$is_args$args;
        }
```

Finally, reload nginx.

```
service nginx reload
```

OpenScienceMap v4 tiles are now accessable from http://HOSTNAME/tiles/oscimv4/{Z}/{X}/{Y}.vtm
