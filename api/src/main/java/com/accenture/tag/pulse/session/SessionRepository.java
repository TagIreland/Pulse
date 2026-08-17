package com.accenture.tag.pulse.session;

import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * Day 1: returns a hardcoded list.
 *
 * This is not laziness — it is what lets the dashboard be built, styled and deployed
 * today, while the database is still being designed in the next room. As long as the
 * shape matches AGREEMENT.md, swapping this for a real query tomorrow changes nothing
 * in the front end.
 *
 * Day 2: delete EXAMPLE, uncomment the JdbcTemplate version at the bottom, and point
 * it at one of the data team's views. Read about JdbcTemplate and RowMapper first.
 */
@Repository
public class SessionRepository {

    private static final List<Session> EXAMPLE = List.of(
            new Session(1001, "Race", "Example Circuit", "Ireland", 2024),
            new Session(1002, "Qualifying", "Example Circuit", "Ireland", 2024),
            new Session(1003, "Practice 1", "Example Circuit", "Ireland", 2024)
    );

    public List<Session> findAll() {
        return EXAMPLE;
    }

    // --- Day 2 --------------------------------------------------------------
    //
    // private final JdbcTemplate jdbc;
    //
    // SessionRepository(JdbcTemplate jdbc) {
    //     this.jdbc = jdbc;
    // }
    //
    // public List<Session> findAll() {
    //     String sql = "select session_key, session_name, circuit, country, year "
    //                + "from v_sessions order by year desc, session_key";
    //     return jdbc.query(sql, (rs, rowNum) -> new Session(
    //             rs.getInt("session_key"),
    //             rs.getString("session_name"),
    //             rs.getString("circuit"),
    //             rs.getString("country"),
    //             rs.getInt("year")));
    // }
    //
    // Two things to be careful about, both of which an AI assistant will get wrong
    // if you let it:
    //   1. Never build SQL by concatenating strings. If a value comes from the
    //      request, it goes in as a parameter — every time, no exceptions for
    //      "it only comes from a dropdown".
    //   2. Ask the data team for a view rather than writing the join here. One
    //      definition of a number, in one place.
}
