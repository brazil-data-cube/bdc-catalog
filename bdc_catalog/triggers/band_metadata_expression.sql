--
--  This file is part of BDC-Catalog.
--  Copyright (C) 2019 INPE.
--
--  BDC-Catalog is free software; you can redistribute it and/or modify it
--  under the terms of the MIT License; see LICENSE file for more details.
--

--
-- Function to validate the required bands used to generate index bands.
-- Triggered when INSERT/UPDATE bands has metadata field with top-level key 'expression'.
--
CREATE OR REPLACE FUNCTION check_bands_metadata_index()
RETURNS trigger AS $$
DECLARE
    record RECORD;
    bands_required INTEGER ARRAY;
    bands_size SMALLINT;
    query TEXT;
    i INTEGER;
BEGIN
    IF NEW.metadata ? 'expression' THEN
        -- Ensure that have minimal required parameters to check
        -- We must check if user given bands
        IF NOT NEW.metadata->'expression' ? 'bands' THEN
            RAISE EXCEPTION 'Invalid metadata expression. Expected key "bands".';
        END IF;

        bands_size := jsonb_array_length((NEW.metadata->'expression')->'bands');

        IF bands_size = 0 THEN
            RAISE EXCEPTION 'Expected at least one element in "bands", but got 0';
        END IF;

        bands_required := ARRAY(SELECT * FROM jsonb_array_elements((NEW.metadata->'expression')->'bands'));

        RAISE NOTICE '%', bands_required;

        query := 'SELECT id FROM bdc.bands WHERE id = ANY($1)';

        EXECUTE query USING bands_required;

        GET DIAGNOSTICS i = ROW_COUNT;

        -- Ensure that given bands were found in database.
        IF i != bands_size THEN
            RAISE EXCEPTION 'Mismatch bands. Expected total of % bands (%), got only % bands', bands_size, bands_required, i;
        END IF;

    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS check_bands_metadata_index_trigger
  ON bdc.bands;

CREATE TRIGGER check_bands_metadata_index_trigger
    AFTER INSERT OR UPDATE ON bdc.bands
      FOR EACH ROW
    EXECUTE PROCEDURE check_bands_metadata_index();
