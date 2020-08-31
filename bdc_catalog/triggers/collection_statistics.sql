--
--  This file is part of BDC-Catalog.
--  Copyright (C) 2019 INPE.
--
--  BDC-Catalog is free software; you can redistribute it and/or modify it
--  under the terms of the MIT License; see LICENSE file for more details.
--

--
-- Defines triggers used in Brazil Data Cube Catalog.
-- Make sure to have initial tables created before.
--

--
-- Trigger to keep up to date the collection start_date, end_date and extent attributes.
--
CREATE OR REPLACE FUNCTION update_collection_time()
RETURNS trigger AS $$
BEGIN
    -- Once Item update/insert, calculate the min/max time and update in collections.
    UPDATE bdc.collections
       SET start_date = stats.min_date,
           end_date = stats.max_date,
           extent = stats.extent
      FROM (
        SELECT min(start_date) AS min_date,
               max(end_date) AS max_date,
               ST_SetSRID(ST_Envelope(ST_Extent(geom)), 4326) AS extent
          FROM bdc.items
         WHERE collection_id = NEW.collection_id
      ) stats;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS update_collection_time_trigger
  ON bdc.items;

CREATE TRIGGER update_collection_time_trigger
    AFTER INSERT OR UPDATE ON bdc.items
      FOR EACH ROW
    EXECUTE PROCEDURE update_collection_time();
