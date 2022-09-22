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
-- Trigger to keep up to date the collection timeline
--
CREATE OR REPLACE FUNCTION update_timeline()
RETURNS trigger AS $$
BEGIN
    -- Once Item update/insert, calculate the min/max time and update in collections.
    IF NOT EXISTS (SELECT * FROM bdc.timeline WHERE collection_id = NEW.collection_id AND time_inst = NEW.start_date) THEN
        INSERT INTO bdc.timeline (collection_id, time_inst, created, updated)
             VALUES (NEW.collection_id, NEW.start_date, now(), now())
                 ON CONFLICT DO NOTHING;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS update_update_timeline_trigger
  ON bdc.items;

CREATE TRIGGER update_update_timeline_trigger
    AFTER INSERT OR UPDATE ON bdc.items
      FOR EACH ROW
    EXECUTE PROCEDURE update_timeline();
