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
-- Trigger to keep up to date the collection tiles
--
CREATE OR REPLACE FUNCTION update_collection_tiles()
RETURNS trigger AS $$
BEGIN
    -- Once Item update/insert, calculate the min/max time and update in collections.
    UPDATE bdc.collections
       SET properties = COALESCE(NULLIF(properties, 'null'), '{}'::JSONB) || COALESCE(NULLIF(tiles, 'null'), '{}'::JSONB)
      FROM (
          SELECT ('{"bdc:tiles": '||to_json(array_agg(DISTINCT bdc.tiles.name))||'}')::JSONB as tiles
            FROM bdc.tiles, bdc.items
           WHERE bdc.items.collection_id = NEW.collection_id
             AND bdc.items.tile_id = bdc.tiles.id
      ) t
      WHERE id = NEW.collection_id
        AND grid_ref_sys_id is not null;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS update_collection_tiles_trigger
  ON bdc.items;

CREATE TRIGGER update_collection_tiles_trigger
    AFTER INSERT OR UPDATE ON bdc.items
      FOR EACH ROW
    EXECUTE PROCEDURE update_collection_tiles();
