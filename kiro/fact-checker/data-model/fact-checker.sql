-- SPDX-License-Identifier: Apache-2.0
-- (C)opyright 2025 BeachGeek.co.uk

-- Fact Checker Database Schema

-- Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    username TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Categories table
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    description TEXT
);

-- Facts table
CREATE TABLE facts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    supporting_url TEXT,
    supporting_info TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

CREATE INDEX idx_facts_user_id ON facts(user_id);
CREATE INDEX idx_facts_category_id ON facts(category_id);

-- Votes table
CREATE TABLE votes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fact_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    vote_type TEXT NOT NULL CHECK(vote_type IN ('fact', 'fake')),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fact_id) REFERENCES facts(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX idx_votes_fact_id ON votes(fact_id);
CREATE INDEX idx_votes_user_id ON votes(user_id);
