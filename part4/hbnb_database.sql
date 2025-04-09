-- Uncomment these two lines to create MySQL DB
--CREATE DATABASE IF NOT EXISTS hbnb_database;
--USE hbnb_database;

-- User table
CREATE TABLE IF NOT EXISTS users (
    id CHAR(36) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password VARCHAR(128) NOT NULL,
    is_admin BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id)
);

-- Places table
CREATE TABLE IF NOT EXISTS places (
    id CHAR(36) NOT NULL,
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    owner_id CHAR(36) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id),
    FOREIGN KEY(owner_id) REFERENCES users(id)
);

-- Reviews table
CREATE TABLE IF NOT EXISTS reviews (
    id CHAR(36) NOT NULL,
    text TEXT NOT NULL,
    rating INT NOT NULL,
    user_id CHAR(36) NOT NULL,
    place_id CHAR(36) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id),
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(place_id) REFERENCES places(id),
    CHECK (rating BETWEEN 1 AND 5)
);

-- Amenities table
CREATE TABLE IF NOT EXISTS amenities (
    id CHAR(36) NOT NULL,
    name VARCHAR(50) NOT NULL UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id)
);

-- Place_Amenities association table
CREATE TABLE IF NOT EXISTS place_amenities (
    place_id CHAR(36) NOT NULL,
    amenity_id CHAR(36) NOT NULL,
    PRIMARY KEY(place_id, amenity_id),
    FOREIGN KEY(place_id) REFERENCES places(id),
    FOREIGN KEY(amenity_id) REFERENCES amenities(id)
);

-- Initial user data
INSERT INTO users(id, first_name, last_name, email, password, is_admin)
VALUES(
    "36c9050e-ddd3-4c3b-9731-9f487208bbc1",
    "Admin",
    "HBnB",
    "admin@hbnb.io",
    "$2b$12$BrNqyywhlf6q0xsUiffOk.1p91OrKKevs0kcaDR9IPZo8OtoRFSqa",
    1
);

-- Initial amenities data
INSERT INTO amenities(id, name)
VALUES (
    "da14bc97-611c-4620-a6fb-531b63e69c1d",
    "WiFi"
);
INSERT INTO amenities(id, name)
VALUES (
    "6fcd108e-5c3d-4db5-a2ad-2553647d1290",
    "Swimming Pool"
);
INSERT INTO amenities(id, name)
VALUES (
    "7a0f47c7-fdc6-4d65-895d-a0d1fb61dd92",
    "Air Conditioning"
);
