package com.accenture.tag.pulse.session;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

/**
 * The example endpoint. Copy this shape for the endpoints you agreed in AGREEMENT.md.
 *
 * Notice what is not here: no SQL, no business logic, no data. A controller's job is
 * to accept an HTTP request and hand back a result. Everything else belongs somewhere
 * else — and you will be asked to justify it if you put a query in here.
 */
@RestController
@RequestMapping("/api")
public class SessionController {

    private final SessionRepository repository;

    SessionController(SessionRepository repository) {
        this.repository = repository;
    }

    @GetMapping("/sessions")
    public List<Session> sessions() {
        return repository.findAll();
    }

    // TODO one method per endpoint in AGREEMENT.md.
    //
    // Before you write the second one, decide as a team:
    //   - what an empty result looks like (an empty list and a 200, not a 404)
    //   - what an error looks like — one JSON shape for every failure, never a
    //     stack trace and never a 200 with the word "error" inside it
    //   - whether anything here could ever return enough rows to need paging
}
