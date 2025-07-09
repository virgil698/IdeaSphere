-- PostgreSQL 初始化脚本

CREATE TABLE IF NOT EXISTS sample_table (
                                            id SERIAL PRIMARY KEY,
                                            name VARCHAR(255)
    );