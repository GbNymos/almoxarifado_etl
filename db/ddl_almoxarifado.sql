CREATE TABLE Grupo (
    codigo_grupo INTEGER PRIMARY KEY,
    denominacao_grupo TEXT NOT NULL
);

CREATE TABLE Item_almoxarifado (
    id_item INTEGER PRIMARY KEY ,
    codigo_item INTEGER NOT NULL,
    denominacao_item TEXT NOT NULL,
    unidade_medida TEXT NOT NULL,
    codigo_grupo INTEGER,
    FOREIGN KEY (codigo_grupo) REFERENCES Grupo(codigo_grupo)
);