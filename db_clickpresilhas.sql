CREATE TABLE Empresa_03 (
  A03_id INTEGER   NOT NULL ,
  A03_nome VARCHAR(40)    ,
  A03_cnpj VARCHAR(15)      ,
PRIMARY KEY(A03_id));




CREATE TABLE Notafiscal_01 (
  A01_id INTEGER   NOT NULL ,
  Empresa_03_A03_id INTEGER   NOT NULL ,
  A01_codigo VARCHAR(255)    ,
  A01_data DATETIME      ,
PRIMARY KEY(A01_id)  ,
  FOREIGN KEY(Empresa_03_A03_id)
    REFERENCES Empresa_03(A03_id));


CREATE INDEX Notafiscal_01_FKIndex1 ON Notafiscal_01 (Empresa_03_A03_id);


CREATE INDEX IFK_Rel_02 ON Notafiscal_01 (Empresa_03_A03_id);


CREATE TABLE Etiqueta_02 (
  A02_id INTEGER   NOT NULL ,
  Notafiscal_01_A01_id INTEGER   NOT NULL ,
  A02_codigo VARCHAR(255)    ,
  A0_data DATETIME      ,
PRIMARY KEY(A02_id)  ,
  FOREIGN KEY(Notafiscal_01_A01_id)
    REFERENCES Notafiscal_01(A01_id));


CREATE INDEX Etiqueta_02_FKIndex1 ON Etiqueta_02 (Notafiscal_01_A01_id);


CREATE INDEX IFK_Rel_03 ON Etiqueta_02 (Notafiscal_01_A01_id);



