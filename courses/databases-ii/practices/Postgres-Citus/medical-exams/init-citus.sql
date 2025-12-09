CREATE EXTENSION citus;

CREATE TABLE patients (
    patiend_id SERIAL PRIMARY KEY,
    names VARCHAR(100) NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAUL CURRENT_TIMESTAMP
);

CREATE TABLE medical_exams (
    exam_id INTEGER PRIMARY KEY,
    patient_id INTEGER, 
    examType VARCHAR(30) NOT NULL,
    result VARCHAR(100),
    created_at TIMESTAMP DEFAUL CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patiend_id)
);

-- Data
INSERT INTO patients (names, email) VALUES
('Pepita Perez', 'pperez@ud.edu.co'),
('Juanito Perigollaz', 'jperigollaz@ud.edu.co');