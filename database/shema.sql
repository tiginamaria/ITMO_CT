CREATE TABLE IF NOT EXISTS "Photos" (
        "PhotoID"       INTEGER NOT NULL,
        "PhotoName"     TEXT NOT NULL,
        "UploadDateTime"        TEXT NOT NULL,
        "PhotoDateTime" TEXT,
        "LocationLatitude"      REAL,
        "LocationLongitude"     REAL,
        "Weather"       INTEGER,
        PRIMARY KEY("PhotoID" AUTOINCREMENT),
        UNIQUE("PhotoName")
);

CREATE TABLE IF NOT EXISTS "Colors" (
        "ColorID"       INTEGER NOT NULL,
        "PhotoID"       INTEGER NOT NULL,
        "ColorRed"      INTEGER NOT NULL,
        "ColorGreen"    INTEGER NOT NULL,
        "ColorBlue"     INTEGER NOT NULL,
        PRIMARY KEY("ColorID" AUTOINCREMENT),
        FOREIGN KEY("PhotoID") REFERENCES "Photos"("PhotoID") ON UPDATE CASCADE ON DELETE CASCADE
);
