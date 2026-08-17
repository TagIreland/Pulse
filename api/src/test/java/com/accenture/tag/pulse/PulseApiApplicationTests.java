package com.accenture.tag.pulse;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

/**
 * Starts the whole application and checks it comes up. It is a small test and it
 * catches a surprising amount: a missing bean, a broken property file, a component
 * that will not construct.
 *
 * This is what turns the build red in GitHub Actions when someone breaks main.
 * Add more as you go — one test per endpoint that would fail if the endpoint broke
 * in the most likely way.
 */
@SpringBootTest
class PulseApiApplicationTests {

    @Test
    void contextLoads() {
    }
}
