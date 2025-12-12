-- database: ./[TUR] M4L3_world_information.db

SELECT country.country, info.density
FROM info
JOIN country ON info.country_id = country.country_id
WHERE info.population > 10000000 AND info.area < 8000000
ORDER BY info.density DESC
LIMIT 1;
