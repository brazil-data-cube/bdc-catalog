--
-- This file is part of BDC-Catalog.
-- Copyright (C) 2022 INPE.
--
-- This program is free software: you can redistribute it and/or modify
-- it under the terms of the GNU General Public License as published by
-- the Free Software Foundation, either version 3 of the License, or
-- (at your option) any later version.
--
-- This program is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
-- GNU General Public License for more details.
--
-- You should have received a copy of the GNU General Public License
-- along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
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
           spatial_extent = stats.extent
      FROM (
        SELECT min(start_date) AS min_date,
               max(end_date) AS max_date,
               ST_SetSRID(ST_Envelope(ST_Extent(bbox)), 4326) AS extent
          FROM bdc.items
         WHERE collection_id = NEW.collection_id
           AND bdc.items.is_available = 't'
      ) stats
      WHERE id = NEW.collection_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS update_collection_time_trigger
  ON bdc.items;

CREATE TRIGGER update_collection_time_trigger
    AFTER INSERT OR UPDATE ON bdc.items
      FOR EACH ROW
    EXECUTE PROCEDURE update_collection_time();
