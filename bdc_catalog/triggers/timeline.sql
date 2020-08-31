--
--  This file is part of BDC-Catalog.
--  Copyright (C) 2019 INPE.
--
--  BDC-Catalog is free software; you can redistribute it and/or modify it
--  under the terms of the MIT License; see LICENSE file for more details.
--

--
-- Trigger to keep up to date the collection timeline
--
CREATE OR REPLACE FUNCTION update_timeline()
RETURNS trigger AS $$
BEGIN
    -- Once Item update/insert, calculate the min/max time and update in collections.
    IF NOT EXISTS (SELECT * FROM bdc.timeline WHERE collection_id = NEW.collection_id AND (time_inst = NEW.start_date OR time_inst = NEW.end_date)) THEN
        INSERT INTO bdc.timeline (collection_id, time_inst, created, updated)
             VALUES (NEW.collection_id, NEW.start_date, now(), now()), (NEW.collection_id, NEW.end_date, now(), now())
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
