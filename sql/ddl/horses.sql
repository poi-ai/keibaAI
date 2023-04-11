-- 競走馬の基本データ(不変のデータ)を格納
CREATE TABLE horses (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'レコードID',
    jbis_id MEDIUMINT UNSIGNED NOT NULL COMMENT 'JBIS競走馬ID',
    father_name VARCHAR(30) COMMENT '父名',
    father_jbis_id MEDIUMINT UNSIGNED COMMENT '父のJBIS競走馬ID',
    mother_name VARCHAR(30) COMMENT '母名',
    mother_jbis_id MEDIUMINT UNSIGNED COMMENT '母のJBIS競走馬ID',
    birth_day DATE COMMENT '誕生日',
    country VARCHAR(10) COMMENT '生産国',
    birth_place VARCHAR(50) COMMENT '生産地',
    breeder VARCHAR(50) COMMENT '生産牧場',
    hair_color VARCHAR(20) COMMENT '毛色',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード追加時刻',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'レコード更新時刻'
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;