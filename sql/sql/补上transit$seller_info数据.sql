
insert into transit$seller_info(seller_info_id, comp_id, info_type,status,remark,post_time, create_by, create_time)
select SQ_TRANSIT$SELLER_INFO.Nextval, 2422364, 6, 3, null, sysdate, 0, sysdate from dual;


select * from transit$seller_info tsi where tsi.comp_id = 2445788;

delete from transit$seller_info tsi where tsi.comp_id = 2445788 and tsi.info_type = 6