def data_seed():
    return """
        INSERT INTO modulo (cod, nombre) VALUES
        ('0485', 'PROGRAMACIÓN'),
        ('0484', 'BASE DE DATOS'),
        ('0494', 'ACCESO DE DATOS'),
        ('0483', 'SISTEMAS INFORMÁTICOS'),
        ('0488', 'DESARROLLO DE INTERFACES'),
        ('0490', 'SERVICIOS Y PROCESOS');

        INSERT INTO ra (id, codigo, descripcion, modulo_cod) VALUES
        (1, 'RA1', 'Reconoce la estructura de un programa informático', '0485'),
        (2, 'RA3', 'Escribe y depura código, utilizando estructuras de control', '0485'),
        (3, 'RA4', 'Desarrolla programas organizados en clases aplicando POO', '0485'),

        (4, 'RA1', 'Diseña bases de datos relacionales', '0484'),
        (5, 'RA2', 'Realiza operaciones básicas con SQL', '0484'),

        (6, 'RA1', 'Accede a bases de datos desde lenguajes de programación', '0494'),
        (7, 'RA2', 'Utiliza tecnologías de persistencia', '0494'),
        (8, 'RA3', 'Implementa acceso a datos en aplicaciones', '0494'),

        (9, 'RA2', 'Instala sistemas operativos', '0483'),
        (10, 'RA4', 'Configura redes locales', '0483'),

        (11, 'RA1', 'Diseña interfaces gráficas de usuario', '0488'),
        (12, 'RA2', 'Implementa interfaces gráficas', '0488'),

        (13, 'RA1', 'Desarrolla servicios en segundo plano', '0490'),
        (14, 'RA2', 'Implementa comunicaciones entre procesos', '0490');

        INSERT INTO ce (id, codigo, descripcion, modulo_cod, ra_id) VALUES
        (1, 'CE1.a', 'Se han identificado los bloques que componen la estructura de un programa', '0485', 1),
        (2, 'CE1.b', 'Se han utilizado entornos integrados de desarrollo', '0485', 1),
        (3, 'CE1.c', 'Se han creado proyectos de desarrollo de aplicaciones', '0485', 1),

        (4, 'CE3.a', 'Se ha escrito y probado código con estructuras de selección', '0485', 2),
        (5, 'CE3.b', 'Se han utilizado estructuras de repetición', '0485', 2),
        (6, 'CE3.g', 'Se han probado y depurado los programas', '0485', 2),

        (7, 'CE4.a', 'Se ha reconocido la sintaxis y estructura de una clase', '0485', 3),
        (8, 'CE4.b', 'Se han definido clases', '0485', 3),
        (9, 'CE4.c', 'Se han definido propiedades y métodos', '0485', 3),

        (10, 'CE1.a', 'Se han identificado entidades y relaciones', '0484', 4),
        (11, 'CE1.b', 'Se han creado esquemas conceptuales y lógicos', '0484', 4),
        (12, 'CE1.c', 'Se han normalizado tablas', '0484', 4),

        (13, 'CE2.a', 'Se han creado y modificado tablas', '0484', 5),
        (14, 'CE2.b', 'Se han insertado, actualizado y eliminado datos', '0484', 5),
        (15, 'CE2.c', 'Se han realizado consultas simples y complejas', '0484', 5),

        (16, 'CE1.a', 'Se han utilizado APIs de acceso a datos', '0494', 6),
        (17, 'CE1.b', 'Se han realizado operaciones CRUD', '0494', 6),
        (18, 'CE1.c', 'Se han gestionado conexiones y errores', '0494', 6),

        (19, 'CE2.a', 'Se han utilizado frameworks ORM', '0494', 7),
        (20, 'CE2.b', 'Se han mapeado clases a tablas', '0494', 7),
        (21, 'CE2.c', 'Se han realizado consultas con objetos', '0494', 7),

        (22, 'CE3.a', 'Se han separado capas de acceso y lógica', '0494', 8),
        (23, 'CE3.b', 'Se han utilizado patrones DAO', '0494', 8),
        (24, 'CE3.c', 'Se han probado operaciones de acceso', '0494', 8),

        (25, 'CE2.a', 'Se han instalado sistemas operativos libres y propietarios', '0483', 9),
        (26, 'CE2.b', 'Se han configurado dispositivos y periféricos', '0483', 9),
        (27, 'CE2.c', 'Se han instalado y actualizado controladores', '0483', 9),

        (28, 'CE4.a', 'Se han identificado elementos de red', '0483', 10),
        (29, 'CE4.b', 'Se han configurado direcciones IP', '0483', 10),
        (30, 'CE4.c', 'Se ha verificado la conectividad', '0483', 10),

        (31, 'CE1.a', 'Se han utilizado componentes visuales', '0488', 11),
        (32, 'CE1.b', 'Se han aplicado principios de usabilidad', '0488', 11),
        (33, 'CE1.c', 'Se han creado prototipos', '0488', 11),

        (34, 'CE2.a', 'Se han programado eventos', '0488', 12),
        (35, 'CE2.b', 'Se han enlazado datos a componentes', '0488', 12),
        (36, 'CE2.c', 'Se han validado entradas de usuario', '0488', 12),

        (37, 'CE1.a', 'Se han creado servicios como demonios o servicios del sistema', '0490', 13),
        (38, 'CE1.b', 'Se han gestionado hilos y procesos', '0490', 13),
        (39, 'CE1.c', 'Se han registrado eventos del sistema', '0490', 13),

        (40, 'CE2.a', 'Se han utilizado sockets', '0490', 14),
        (41, 'CE2.b', 'Se han implementado protocolos de comunicación', '0490', 14),
        (42, 'CE2.c', 'Se han gestionado errores de red', '0490', 14);
        """
