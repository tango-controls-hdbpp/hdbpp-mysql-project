
delimiter //
USE hdbpp//

CREATE PROCEDURE partition_table_year (IN table_name VARCHAR(255), IN col_name VARCHAR(255))
proc_label: BEGIN

SET @year:=YEAR(CURRENT_TIMESTAMP);

SET @table = table_name;
SET @col = col_name;
SET @s = CONCAT('ALTER TABLE ', table_name, ' PARTITION BY RANGE COLUMNS(',col_name,') (
	PARTITION p000 VALUES LESS THAN (\'',@year-1,'-01-01\'),
	PARTITION p', @year-1, ' VALUES LESS THAN (\'',@year,'-01-01\'),
        PARTITION p', @year, ' VALUES LESS THAN (\'',@year+1,'-01-01\'),
        PARTITION future       VALUES LESS THAN MAXVALUE  
    )');
PREPARE stmt FROM @s;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

END//

CREATE PROCEDURE partition_table_bimonth (IN table_name VARCHAR(255), IN col_name VARCHAR(255))
proc_label: BEGIN

SET @year:=YEAR(CURRENT_TIMESTAMP);

SET @table = table_name;
SET @col = col_name;
SET @s = CONCAT('ALTER TABLE ', table_name, ' PARTITION BY RANGE COLUMNS(',col_name,') (
	PARTITION p000 VALUES LESS THAN (\'',@year-1,'-01-01\'),
        PARTITION p', @year-1, '_01_02 VALUES LESS THAN (\'',@year-1,'-03-01\'),
        PARTITION p', @year-1, '_03_04 VALUES LESS THAN (\'',@year-1,'-05-01\'),
        PARTITION p', @year-1, '_05_06 VALUES LESS THAN (\'',@year-1,'-07-01\'),
        PARTITION p', @year-1, '_07_08 VALUES LESS THAN (\'',@year-1,'-09-01\'),
        PARTITION p', @year-1, '_09_10 VALUES LESS THAN (\'',@year-1,'-11-01\'),
        PARTITION p', @year-1, '_11_12 VALUES LESS THAN (\'',@year,'-01-01\'),
        PARTITION p', @year, '_01_02 VALUES LESS THAN (\'',@year,'-03-01\'),
        PARTITION p', @year, '_03_04 VALUES LESS THAN (\'',@year,'-05-01\'),
        PARTITION p', @year, '_05_06 VALUES LESS THAN (\'',@year,'-07-01\'),
        PARTITION p', @year, '_07_08 VALUES LESS THAN (\'',@year,'-09-01\'),
        PARTITION p', @year, '_09_10 VALUES LESS THAN (\'',@year,'-11-01\'),
        PARTITION p', @year, '_11_12 VALUES LESS THAN (\'',@year+1,'-01-01\'),
        PARTITION future       VALUES LESS THAN MAXVALUE  
    )');
PREPARE stmt FROM @s;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

END//

delimiter ;

CALL partition_table_year('att_parameter', 'recv_time');
CALL partition_table_year('att_history', 'time');

CALL partition_table_year('att_scalar_devboolean_ro', 'data_time');
CALL partition_table_year('att_scalar_devboolean_rw', 'data_time');
CALL partition_table_year('att_array_devboolean_ro', 'data_time');
CALL partition_table_year('att_array_devboolean_rw', 'data_time');

CALL partition_table_year('att_scalar_devuchar_ro', 'data_time');
CALL partition_table_year('att_scalar_devuchar_rw', 'data_time');
CALL partition_table_year('att_array_devuchar_ro', 'data_time');
CALL partition_table_year('att_array_devuchar_rw', 'data_time');

CALL partition_table_year('att_scalar_devshort_ro', 'data_time');
CALL partition_table_year('att_scalar_devshort_rw', 'data_time');
CALL partition_table_year('att_array_devshort_ro', 'data_time');
CALL partition_table_year('att_array_devshort_rw', 'data_time');

CALL partition_table_year('att_scalar_devushort_ro', 'data_time');
CALL partition_table_year('att_scalar_devushort_rw', 'data_time');
CALL partition_table_year('att_array_devushort_ro', 'data_time');
CALL partition_table_year('att_array_devushort_rw', 'data_time');

CALL partition_table_year('att_scalar_devlong_ro', 'data_time');
CALL partition_table_year('att_scalar_devlong_rw', 'data_time');
CALL partition_table_year('att_array_devlong_ro', 'data_time');
CALL partition_table_year('att_array_devlong_rw', 'data_time');

CALL partition_table_year('att_scalar_devulong_ro', 'data_time');
CALL partition_table_year('att_scalar_devulong_rw', 'data_time');
CALL partition_table_year('att_array_devulong_ro', 'data_time');
CALL partition_table_year('att_array_devulong_rw', 'data_time');

CALL partition_table_year('att_scalar_devlong64_ro', 'data_time');
CALL partition_table_year('att_scalar_devlong64_rw', 'data_time');
CALL partition_table_year('att_array_devlong64_ro', 'data_time');
CALL partition_table_year('att_array_devlong64_rw', 'data_time');

CALL partition_table_year('att_scalar_devulong64_ro', 'data_time');
CALL partition_table_year('att_scalar_devulong64_rw', 'data_time');
CALL partition_table_year('att_array_devulong64_ro', 'data_time');
CALL partition_table_year('att_array_devulong64_rw', 'data_time');

CALL partition_table_year('att_scalar_devfloat_ro', 'data_time');
CALL partition_table_year('att_scalar_devfloat_rw', 'data_time');
CALL partition_table_year('att_array_devfloat_ro', 'data_time');
CALL partition_table_year('att_array_devfloat_rw', 'data_time');

CALL partition_table_bimonth('att_scalar_devdouble_ro', 'data_time');
CALL partition_table_year('att_scalar_devdouble_rw', 'data_time');
CALL partition_table_year('att_array_devdouble_ro', 'data_time');
CALL partition_table_year('att_array_devdouble_rw', 'data_time');

CALL partition_table_year('att_scalar_devstring_ro', 'data_time');
CALL partition_table_year('att_scalar_devstring_rw', 'data_time');
CALL partition_table_year('att_array_devstring_ro', 'data_time');
CALL partition_table_year('att_array_devstring_rw', 'data_time');

CALL partition_table_year('att_scalar_devstate_ro', 'data_time');
CALL partition_table_year('att_scalar_devstate_rw', 'data_time');
CALL partition_table_year('att_array_devstate_ro', 'data_time');
CALL partition_table_year('att_array_devstate_rw', 'data_time');

CALL partition_table_year('att_scalar_devencoded_ro', 'data_time');
CALL partition_table_year('att_scalar_devencoded_rw', 'data_time');
CALL partition_table_year('att_array_devencoded_ro', 'data_time');
CALL partition_table_year('att_array_devencoded_rw', 'data_time');

CALL partition_table_year('att_scalar_devenum_ro', 'data_time');
CALL partition_table_year('att_scalar_devenum_rw', 'data_time');
CALL partition_table_year('att_array_devenum_ro', 'data_time');
CALL partition_table_year('att_array_devenum_rw', 'data_time');

DROP PROCEDURE partition_table_year;
DROP PROCEDURE partition_table_bimonth;
