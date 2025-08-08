

-- Insert test activities
INSERT INTO activities (name, parent_id, level) VALUES
('Еда', NULL, 1),
('Мясная продукция', 1, 2),
('Молочная продукция', 1, 2),
('Автомобили', NULL, 1),
('Грузовые', 4, 2),
('Легковые', 4, 2),
('Запчасти', 6, 3),
('Аксессуары', 6, 3);

-- Insert test buildings
INSERT INTO buildings (address, latitude, longitude) VALUES
('г. Москва, ул. Ленина 1, офис 3', 55.755826, 37.617300),
('г. Москва, ул. Блюхера 32/1', 55.762863, 37.608521),
('г. Москва, ул. Тверская 10', 55.757989, 37.611523);

-- Insert test organizations
INSERT INTO organizations (name, building_id, phones) VALUES
('ООО "Рога и Копыта"', 1, '["2-222-222", "3-333-333"]'),
('Молочные продукты "Деревенька"', 2, '["8-800-555-3535"]'),
('Автозапчасти "Колесо"', 3, '["8-495-123-4567"]');

-- Link organizations to activities
INSERT INTO organization_activities VALUES
(1, 2), -- Рога и Копыта -> Мясная продукция
(1, 3), -- Рога и Копыта -> Молочная продукция
(2, 3), -- Деревенька -> Молочная продукция
(3, 7); -- Колесо -> Запчасти
