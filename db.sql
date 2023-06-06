\copy companies (symbol, comp_name, lat, lon, country, geo_state) FROM 'nasdaq.csv' DELIMITER ',' CSV HEADER;
