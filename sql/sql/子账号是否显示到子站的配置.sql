

select * from acc$user_setting aus where aus.comp_id = 2445788;

select * from acc$sub_setting ass where ass.comp_id = 100609;

select * from acc$sub_service ass where ass.comp_id = 2445788;

select * from gm$serv_setting gss;

select * from gm$service gs where gs.serv_code = 'WEBSITE';

--
select * from seller$product_group spg;
--写入gm$setting
insert into gm$setting
  select 'is_show_subuser',
         'ShowSubuser',
         'Portal页面上显示子账号',
         'R',
         null,
         sysdate,
         sysdate
    from dual;
--从gm$pack_service 查出pack_serv_id 【pack_code == WEB】
select gps.pack_serv_id
  from gm$pack_service gps
 where gps.pack_code = 'WEB'
   and gps.serv_code = 'WEBSITE';
--从gm$serv_setting中查出serv_set_id【根据set_code】
insert into gm$serv_setting
  select gm_core.sq_gm$serv_setting.nextval,
         (select gps.pack_serv_id
            from gm$pack_service gps
           where gps.pack_code = 'WEB'
             and gps.serv_code = 'WEBSITE'),
         'is_show_subuser',
         null,
         null,
         null,
         'Y',
         sysdate,
         sysdate
    from dual;
--从acc$sub_service中查出sub_serv_id【根据comp_id&pack_code=WEB】
--插入acc$sub_setting表，得到sub_set_id【sub_serv_id、serv_set_id、set_code】

show_subuser

select * from web$user wu where wu.comp_id = 2445788;

select * from gm$setting gs where gs.set_code = 'is_show_subuser';

select * from gm$serv_setting gss


delete from acc$user_setting aus
 where aus.comp_id = :compId
   and aus.user_id in (:subUserIds)
   and aus.set_code = :setCode;
   
   
select * from acc$user_setting aus
select * from acc$sub_setting 

INSERT INTO acc$user_setting
  SELECT gm_core.sq_acc$user_setting.NEXTVAL from dual, wu.user_id,
         ass.sub_serv_id, ass.sub_set_id, ass.serv_set_id, 
         ass.comp_id, ass.set_code, ass.assignment_type,
         decode(ass.assignment_type, 'Q', :value, NULL),
         decode(ass.assignment_type, 'Q', 0, NULL),
         decode(ass.assignment_type, 'R', :value, 'V', :value, NULL),
         userId, SYSDATE, userId, SYSDATE
    FROM web$user wu, acc$sub_setting ass
   WHERE 1 = 1
     AND wu.comp_id = :compId
     AND wu.user_id IN (subUserIds)
     AND ass.comp_id = wu.comp_id
     AND ass.set_code = :setCode
  
  select * from acc$sub_service ass
  select * from acc$user_setting aus where aus.comp_id = 100609;
  select * from web$user where comp_id = 2445788;
  
  
  select * from seller$product sp where sp.comp_id = 100609;
  select * from web$user wu where wu.comp_id = 100609;
  
  
  102043
  
  
  select * from sns$blog where entity_id = 102043;