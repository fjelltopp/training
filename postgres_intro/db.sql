CREATE TABLE patients (
    id          integer PRIMARY KEY,
    name        varchar(40) NOT NULL,
    age         integer NOT NULL,
    visit_date  date,
    disease     varchar(15),
    tests       jsonb
);

INSERT INTO patients  (id, name, age, visit_date, disease, tests)
VALUES
 (1,'gunnar', 39, '2018-03-01', 'diabetes', '{"bp": 300, "glucose": 8}'),
 (2, 'jonathan', 18, '2018-03-05', 'diabetes', '{}'),
 (3, 'gunnar2', 32, '2018-03-09', 'hypetension', '{"bp": 10, "glucose": 3}'),
 (4, 'jonathan2', 99, '2018-02-01', 'diabetes', '{"bp": 50, "glucose": 59}'),
 (5, 'gunnar3', 300, '2018-03-07', 'diabetes', '{"bp": 200, "weight": 98}'),
 (6, 'joanthan3', 76, '2018-03-10', 'hypertension', '{"bp": 100}');
      

