package com.accenture.tag.pulse.session;

/**
 * What the API sends to the dashboard. Field names here become the JSON keys, so
 * they have to match what is written in AGREEMENT.md — the front end is built
 * against that document, not against this class.
 *
 * A record is a good fit: it is immutable, and Spring turns it into JSON without
 * needing getters.
 */
public record Session(
        int sessionKey,
        String sessionName,
        String circuit,
        String country,
        int year
) {
}
