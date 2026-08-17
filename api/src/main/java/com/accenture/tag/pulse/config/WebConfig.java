package com.accenture.tag.pulse.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

/**
 * You are here because the browser refused your first request from Angular and the
 * error message was unhelpful. That is CORS.
 *
 * The browser will not let a page served from one origin call an API on another
 * unless the API says it is allowed. Your dashboard is on localhost:4200 and this
 * API is on localhost:8080 — different origins.
 *
 * Read about it before you fix it, then add a mapping below. Two questions worth
 * being able to answer:
 *
 *   1. Which origins do you actually want to allow? "*" makes the error go away and
 *      is the wrong answer in anything that ever ships.
 *   2. When the dashboard is deployed to Vercel, its origin changes. What needs to
 *      happen here, and how will you avoid hardcoding it?
 */
@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        // TODO allow the dashboard to call this API.
        //
        // registry.addMapping("/api/**")
        //         .allowedOrigins("http://localhost:4200")
        //         .allowedMethods("GET", "POST");
    }
}
