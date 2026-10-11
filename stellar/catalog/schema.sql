PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS star (
  id      INTEGER PRIMARY KEY,
  name    TEXT NOT NULL UNIQUE,
  constel TEXT NOT NULL,
  ra_deg  REAL NOT NULL CHECK (ra_deg >= 0 AND ra_deg < 360),
  dec_deg REAL NOT NULL CHECK (dec_deg BETWEEN -90 AND 90),
  mag     REAL NOT NULL,
  role    TEXT NOT NULL CHECK (role IN ('OPTION','CONTROL')),
  command TEXT UNIQUE,
  CHECK ((role = 'CONTROL') = (command IS NOT NULL))
);

CREATE TABLE IF NOT EXISTS menu_node (
  id        INTEGER PRIMARY KEY,
  parent_id INTEGER REFERENCES menu_node(id),
  label     TEXT NOT NULL,
  hint      TEXT,
  is_leaf   INTEGER NOT NULL DEFAULT 0 CHECK (is_leaf IN (0,1))
);

CREATE TABLE IF NOT EXISTS menu_edge (
  node_id   INTEGER NOT NULL REFERENCES menu_node(id),
  star_id   INTEGER NOT NULL REFERENCES star(id),
  next_node INTEGER NOT NULL REFERENCES menu_node(id),
  PRIMARY KEY (node_id, star_id)
);

-- Solo las estrellas OPTION pueden ser ramas del menú.
CREATE TRIGGER IF NOT EXISTS menu_edge_option_only
BEFORE INSERT ON menu_edge
WHEN (SELECT role FROM star WHERE id = NEW.star_id) <> 'OPTION'
BEGIN
  SELECT RAISE(ABORT, 'menu_edge.star_id must reference an OPTION star');
END;

CREATE TABLE IF NOT EXISTS payload (
  id         INTEGER PRIMARY KEY,
  seq_hash   BLOB NOT NULL UNIQUE,
  kind       TEXT NOT NULL CHECK (kind IN ('text','image','audio','video')),
  nonce      BLOB NOT NULL,
  ciphertext BLOB NOT NULL,
  media_path TEXT
);
