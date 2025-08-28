-- Création du schéma EventGear
CREATE SCHEMA IF NOT EXISTS eventgear;
SET search_path TO eventgear, public;

-- Extension pour UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Table des équipements
CREATE TABLE equipment (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    quantity_total INTEGER DEFAULT 1,
    quantity_available INTEGER DEFAULT 1,
    location VARCHAR(200),
    purchase_date DATE,
    purchase_price DECIMAL(10, 2),
    rental_price_daily DECIMAL(10, 2),
    weight_kg DECIMAL(10, 2),
    dimensions VARCHAR(100),
    notes TEXT,
    active BOOLEAN DEFAULT true,
    extra_data JSONB DEFAULT '{}',  -- Renommé
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Table des événements
CREATE TABLE events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    client_name VARCHAR(200),
    location VARCHAR(500),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    setup_date TIMESTAMPTZ,
    teardown_date TIMESTAMPTZ,
    status VARCHAR(50) DEFAULT 'planned',
    notes TEXT,
    extra_data JSONB DEFAULT '{}',  -- Renommé
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Table des allocations
CREATE TABLE equipment_allocations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_id UUID NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    equipment_id UUID NOT NULL REFERENCES equipment(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL DEFAULT 1,
    notes TEXT,
    allocated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(event_id, equipment_id)
);

-- Table des contacts
CREATE TABLE contacts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(50) UNIQUE,
    company_name VARCHAR(200),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255),
    phone VARCHAR(50),
    address TEXT,
    contact_type VARCHAR(50),
    notes TEXT,
    active BOOLEAN DEFAULT true,
    extra_data JSONB DEFAULT '{}',  -- Renommé
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Créer les index
CREATE INDEX idx_equipment_category ON equipment(category);
CREATE INDEX idx_equipment_active ON equipment(active);
CREATE INDEX idx_events_status ON events(status);
CREATE INDEX idx_events_dates ON events(start_date, end_date);
CREATE INDEX idx_contacts_email ON contacts(email);
CREATE INDEX idx_contacts_type ON contacts(contact_type);

-- Fonction pour mettre à jour updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers
CREATE TRIGGER update_equipment_updated_at BEFORE UPDATE ON equipment
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_events_updated_at BEFORE UPDATE ON events
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_contacts_updated_at BEFORE UPDATE ON contacts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
