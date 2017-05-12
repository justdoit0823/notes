
-- PostgreSQL相关运维查询SQL


-- 按照dead tuple占比降序排列显示各表
SELECT * from (SELECT A.relname, 1.0 * A.n_dead_tup / A.n_dead_tup as dead_rate from (select relname, n_tup_ins, n_tup_upd, n_tup_del, n_tup_hot_upd, n_live_tup, n_dead_tup from pg_stat_user_tables) A where A.n_dead_tup > 0) B order by B.dead_rate desc;


-- 按照表的大小，表索引的大小降序排列显示各表
select relname, pg_size_pretty(table_size) as table_size, pg_size_pretty(index_size) as index_size from (select relname, pg_indexes_size(relname::regclass) as index_size, pg_relation_size(relname::regclass) as table_size from pg_stat_user_tables) A order by A.table_size desc, A.index_size desc;


-- 找出没有用到的索引
SELECT relname, indexrelname, idx_scan, idx_tup_read, idx_tup_fetch from pg_stat_user_indexes where relname in (SELECT relname from pg_stat_user_tables) and idx_scan = 0 and idx_tup_read = 0 and idx_tup_fetch = 0;


-- 计算各备机相对主机的复制延迟字节数
SELECT client_addr, pg_xlog_location_diff(pg_current_xlog_location(), replay_location) from pg_stat_replication;


-- 按照客户端连接状态分组
select state, count(state) from pg_stat_activity group by state;


-- 手动针对table_name进行垃圾回收并更新统计
vacuum (verbose, analyze) table_name;


-- 手动收集统计数据
analyze table_name;


-- 快速复制一个表
create table new_table(like old_table including all);


-- 快速copy一个表(只有数据)
create table new_table as select * from old_table;


-- 创建一个外部server
create server server_name foreign data wrapper postgres_fdw options (host '127.0.0.1', port '5433', dbanme 'db1');


-- 创建用户映射
create user mapping for user server server_name options (user 'username', password 'password');


-- 创建外部表
create foreign table new_table(column_name data_type) server server_name options (table_name 'old_table');
