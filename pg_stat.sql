

SELECT * from (SELECT A.relname, 1.0 * A.n_dead_tup / (A.n_live_tup + A.n_dead_tup) as dead_rate from (select relname, n_tup_ins, n_tup_upd, n_tup_del, n_tup_hot_upd, n_live_tup, n_dead_tup from pg_stat_user_tables) A where A.n_dead_tup > 0) B order by B.dead_rate desc;


select relname, pg_size_pretty(table_size) as table_size, pg_size_pretty(index_size) as index_size from (select relname, pg_indexes_size(relname::regclass) as index_size, pg_relation_size(relname::regclass) as table_size from pg_stat_user_tables) A order by A.table_size desc, A.index_size desc;


SELECT relname, indexrelname, idx_scan, idx_tup_read, idx_tup_fetch from pg_stat_user_indexes where relname in (SELECT relname from pg_stat_user_tables) and idx_scan = 0 and idx_tup_read = 0 and idx_tup_fetch = 0;


SELECT client_addr, pg_xlog_location_diff(pg_current_xlog_location(), replay_location) from pg_stat_replication;


select state, count(state) from pg_stat_activity group by state;

