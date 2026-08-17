-- One view per dashboard tile, returning exactly the columns agreed in AGREEMENT.md.
--
-- Everything awkward happens here, once, in SQL: the joins, the aggregation, the
-- rounding, the unit conversion. Not four times in Java, and not differently in each
-- of the four places that need it.
--
-- The API reads these and nothing else.

-- ---------------------------------------------------------------------------
-- The view behind the example endpoint, /api/sessions.
-- The column names here are what the Java RowMapper reads, so if you rename one,
-- something breaks in the other team's code. That is what the agreement is for.
-- ---------------------------------------------------------------------------

-- create or replace view v_sessions as
-- select session_key,
--        session_name,
--        circuit,
--        country,
--        year
-- from   sessions;

-- ---------------------------------------------------------------------------
-- TODO one view per tile.
-- ---------------------------------------------------------------------------

-- Before you write each one, settle three things and write them down:
--   1. Units. Milliseconds or seconds — pick one and be consistent.
--   2. Timezone. Store UTC, convert in the front end. Label the axis.
--   3. What a missing value means. A null lap time is not a lap time of zero, and
--      averaging across the gap is not the same as leaving it out.

-- If a view takes more than a second, look at what it is scanning before you look at
-- anything else.
