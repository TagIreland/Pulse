-- The normalised schema. This is the core of the data team's two days.
--
-- Raw tables are created for you by fetch.py, straight from whatever the API sent, and
-- they will be full of repetition: the driver's name and team on every single lap row.
-- Your job is to turn that into a proper relational model — one table per real-world
-- thing, a primary key on each, foreign keys between them, and no fact stored twice.
--
-- Design it yourself from what you actually pulled. Below is one worked table so the
-- shape is obvious, and then it is over to you.
--
-- Read about first, second and third normal form before you start. Twenty minutes of
-- reading saves two hours of restructuring.

-- ---------------------------------------------------------------------------
-- Worked example: one row per driver. Note that the name is here and nowhere else.
-- ---------------------------------------------------------------------------

drop table if exists drivers cascade;

create table drivers (
    driver_number integer primary key,
    full_name     text not null,
    team          text,
    country_code  text
);

insert into drivers (driver_number, full_name, team, country_code)
select distinct
       driver_number,
       full_name,
       team_name,
       country_code
from   raw_drivers
where  driver_number is not null;

-- ---------------------------------------------------------------------------
-- Your turn.
-- ---------------------------------------------------------------------------

-- TODO sessions. One row is one session of one race weekend.
--      What is the natural key? What belongs here rather than on every lap?

-- TODO laps. One row is one lap by one driver in one session. This is your fact
--      table and it will be the biggest. The primary key is more than one column.
--      Declare the foreign keys and watch them reject rows — that rejection is the
--      database telling you something true about your data.

-- TODO stints, pit stops, weather — whichever of them your four tiles need.
--      Do not build tables nothing reads.

-- ---------------------------------------------------------------------------
-- Reconcile before you move on. Take this seriously.
-- ---------------------------------------------------------------------------

-- If raw_laps has 1,247 rows and laps has 1,203, find the 44. They are usually
-- duplicates or a session you dropped by accident. If you cannot explain the
-- difference, you cannot trust the dashboard — and the panel will ask.

-- select count(*) as raw_rows from raw_laps;
-- select count(*) as modelled_rows from laps;

-- ---------------------------------------------------------------------------
-- Indexes
-- ---------------------------------------------------------------------------

-- TODO add an index on the columns you filter by most. Add it after you have seen
-- something be slow, and be able to say what it fixed.
