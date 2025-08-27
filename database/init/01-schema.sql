-- Configuration initiale pour la stabilité
CREATE SCHEMA IF NOT EXISTS eventgear;
SET search_path TO eventgear;

-- Extension pour UUID (plus stable que les ID séquentiels)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tables de référence (changent rarement)
-- ========================================

-- Catégories de matériel
CREATE TABLE categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    parent_id UUID REFERENCES categories(id) ON DELETE SET NULL,
    color VARCHAR(7), -- Couleur hex pour l'UI
    icon VARCHAR(50), -- Nom d'icône pour l'UI
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Lieux de stockage
CREATE TABLE storage_locations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    address TEXT,
    parent_id UUID REFERENCES storage_locations(id) ON DELETE SET NULL,
    notes TEXT,
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- États possibles du matériel
CREATE TABLE equipment_states (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(50) UNIQUE NOT NULL, -- 'new', 'good', 'to_check', 'broken', 'retired'
    name VARCHAR(100) NOT NULL,
    color VARCHAR(7),
    can_be_rented BOOLEAN DEFAULT true,
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tables principales
-- ==================

-- Contacts (clients, fournisseurs, techniciens)
CREATE TABLE contacts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(50) UNIQUE, -- Optionnel, pour référence rapide
    company_name VARCHAR(200),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255),
    phone VARCHAR(50),
    address TEXT,
    contact_type VARCHAR(50), -- 'client', 'supplier', 'technician', 'other'
    notes TEXT,
    active BOOLEAN DEFAULT true,
    -- Métadonnées JSON pour futures extensions sans migration
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Index pour les recherches
    INDEX idx_contacts_email (email),
    INDEX idx_contacts_type (contact_type)
);

-- Articles de stock
CREATE TABLE equipment (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(100) UNIQUE NOT NULL, -- Code interne
    name VARCHAR(200) NOT NULL,
    description TEXT,
    category_id UUID REFERENCES categories(id) ON DELETE SET NULL,
    
    -- Identification
    serial_number VARCHAR(200),
    barcode VARCHAR(200),
    manufacturer VARCHAR(200),
    model VARCHAR(200),
    
    -- Quantités et valeur
    quantity_total INTEGER DEFAULT 1,
    quantity_available INTEGER DEFAULT 1,
    unit_value DECIMAL(10,2),
    currency VARCHAR(3) DEFAULT 'EUR',
    
    -- Localisation et état
    storage_location_id UUID REFERENCES storage_locations(id) ON DELETE SET NULL,
    state_id UUID REFERENCES equipment_states(id) ON DELETE SET NULL,
    
    -- Garantie
    purchase_date DATE,
    warranty_end_date DATE,
    supplier_id UUID REFERENCES contacts(id) ON DELETE SET NULL,
    
    -- Maintenance
    maintenance_interval_days INTEGER, -- NULL = pas de maintenance préventive
    last_maintenance_date DATE,
    usage_count INTEGER DEFAULT 0, -- Nombre de sorties
    
    -- Métadonnées flexibles
    specifications JSONB DEFAULT '{}', -- Specs techniques
    metadata JSONB DEFAULT '{}', -- Champs custom futurs
    
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Index pour performances
    INDEX idx_equipment_category (category_id),
    INDEX idx_equipment_location (storage_location_id),
    INDEX idx_equipment_barcode (barcode),
    INDEX idx_equipment_available (quantity_available)
);

-- Projets
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    
    -- Client et responsable
    client_id UUID REFERENCES contacts(id) ON DELETE SET NULL,
    manager_id UUID REFERENCES contacts(id) ON DELETE SET NULL,
    
    -- Dates
    start_date TIMESTAMPTZ NOT NULL,
    end_date TIMESTAMPTZ NOT NULL,
    prep_date TIMESTAMPTZ, -- Date de préparation
    return_date TIMESTAMPTZ, -- Date prévue de retour
    
    -- Lieu
    venue_name VARCHAR(200),
    venue_address TEXT,
    
    -- Statut
    status VARCHAR(50) DEFAULT 'draft', -- 'draft', 'confirmed', 'prepared', 'ongoing', 'completed', 'cancelled'
    
    -- Documents et notes
    notes TEXT,
    internal_notes TEXT, -- Notes non visibles client
    
    -- Métadonnées
    metadata JSONB DEFAULT '{}',
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Index
    INDEX idx_projects_dates (start_date, end_date),
    INDEX idx_projects_status (status),
    INDEX idx_projects_client (client_id)
);

-- Attribution du matériel aux projets
CREATE TABLE project_equipment (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    equipment_id UUID NOT NULL REFERENCES equipment(id) ON DELETE RESTRICT,
    
    -- Quantités
    quantity_planned INTEGER NOT NULL DEFAULT 1,
    quantity_prepared INTEGER DEFAULT 0,
    quantity_returned INTEGER DEFAULT 0,
    
    -- États
    checkout_date TIMESTAMPTZ, -- Date de sortie effective
    checkin_date TIMESTAMPTZ, -- Date de retour effective
    checkout_by UUID REFERENCES contacts(id) ON DELETE SET NULL,
    checkin_by UUID REFERENCES contacts(id) ON DELETE SET NULL,
    
    -- Notes sur l'état
    checkout_notes TEXT,
    checkin_notes TEXT,
    condition_on_return VARCHAR(50), -- 'good', 'damaged', 'missing'
    
    -- Métadonnées
    metadata JSONB DEFAULT '{}',
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Contrainte d'unicité et index
    UNIQUE(project_id, equipment_id),
    INDEX idx_project_equipment_dates (checkout_date, checkin_date)
);

-- Historique des mouvements (pour traçabilité complète)
CREATE TABLE equipment_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    equipment_id UUID NOT NULL REFERENCES equipment(id) ON DELETE CASCADE,
    project_id UUID REFERENCES projects(id) ON DELETE SET NULL,
    
    action VARCHAR(50) NOT NULL, -- 'checkout', 'checkin', 'maintenance', 'repair', 'move', 'state_change'
    quantity INTEGER,
    
    -- Qui, quand, où
    performed_by UUID REFERENCES contacts(id) ON DELETE SET NULL,
    performed_at TIMESTAMPTZ DEFAULT NOW(),
    location_from UUID REFERENCES storage_locations(id) ON DELETE SET NULL,
    location_to UUID REFERENCES storage_locations(id) ON DELETE SET NULL,
    
    -- Détails
    notes TEXT,
    metadata JSONB DEFAULT '{}',
    
    -- Index pour les requêtes fréquentes
    INDEX idx_history_equipment (equipment_id),
    INDEX idx_history_project (project_id),
    INDEX idx_history_date (performed_at)
);

-- Documents attachés (bons PDF, photos, contrats...)
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Relation polymorphe via type + id
    entity_type VARCHAR(50) NOT NULL, -- 'project', 'equipment', 'contact'
    entity_id UUID NOT NULL,
    
    document_type VARCHAR(50), -- 'checkout_form', 'checkin_form', 'invoice', 'photo', 'contract'
    filename VARCHAR(255) NOT NULL,
    mime_type VARCHAR(100),
    file_size INTEGER,
    file_path TEXT, -- Chemin relatif dans le stockage
    
    -- Métadonnées
    metadata JSONB DEFAULT '{}',
    
    uploaded_by UUID REFERENCES contacts(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Index
    INDEX idx_documents_entity (entity_type, entity_id)
);

-- Vues utiles pour simplifier les requêtes
-- =========================================

-- Vue de disponibilité du matériel
CREATE VIEW v_equipment_availability AS
SELECT 
    e.*,
    e.quantity_total - COALESCE(SUM(
        CASE 
            WHEN pe.checkin_date IS NULL AND pe.checkout_date IS NOT NULL 
            THEN pe.quantity_planned 
            ELSE 0 
        END
    ), 0) as real_quantity_available
FROM equipment e
LEFT JOIN project_equipment pe ON e.id = pe.equipment_id
LEFT JOIN projects p ON pe.project_id = p.id
WHERE p.status NOT IN ('completed', 'cancelled') OR p.status IS NULL
GROUP BY e.id;

-- Triggers pour updated_at automatique
-- =====================================

CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Appliquer le trigger à toutes les tables avec updated_at
CREATE TRIGGER update_categories_updated_at BEFORE UPDATE ON categories
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_storage_locations_updated_at BEFORE UPDATE ON storage_locations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_contacts_updated_at BEFORE UPDATE ON contacts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_equipment_updated_at BEFORE UPDATE ON equipment
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_projects_updated_at BEFORE UPDATE ON projects
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_project_equipment_updated_at BEFORE UPDATE ON project_equipment
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- Données initiales minimales
-- ============================

INSERT INTO equipment_states (code, name, color, can_be_rented, sort_order) VALUES
    ('new', 'Neuf', '#10b981', true, 1),
    ('good', 'Bon état', '#22c55e', true, 2),
    ('to_check', 'À vérifier', '#f59e0b', false, 3),
    ('repair', 'En réparation', '#ef4444', false, 4),
    ('broken', 'Hors service', '#991b1b', false, 5),
    ('retired', 'Retiré', '#6b7280', false, 6);

INSERT INTO categories (code, name) VALUES
    ('sound', 'Son'),
    ('light', 'Éclairage'),
    ('video', 'Vidéo'),
    ('struct', 'Structure'),
    ('cable', 'Câblage'),
    ('misc', 'Divers');

-- Permissions (optionnel mais recommandé)
-- ========================================

-- Créer un rôle pour l'application
CREATE ROLE eventgear_app WITH LOGIN PASSWORD 'changeme';
GRANT ALL PRIVILEGES ON SCHEMA eventgear TO eventgear_app;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA eventgear TO eventgear_app;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA eventgear TO eventgear_app;
