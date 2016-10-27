#!/bin/bash


# 统计接口速度分布
function analyze_log_request(){

    log_file_name=$1

    awk '$1 == "[I" && $5 == 200 {sum += 1; duration = int(substr($10, 0, length($10) - 2)); if(duration < 200) r200 += 1; else if(duration >= 200 && duration < 500) r500 += 1; else r1000 += 1;} END {print "总请求量", "200ms以内", "500ms以内", "500ms以外"; print sum, r200, r500, r1000, r200 / sum}' $log_file_name
}


# 统计接口qps
function analyze_top_qps(){

    log_file_name=$1

    awk '{second = $4; agg[second] += 1} END {for(second in agg) print second, agg[second]}' $log_file_name | sort -nr -k 2 | head

}
