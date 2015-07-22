declare
  v_comp_count          number(10);  --¹«Ë¾¼ÆÊýÆ÷
  v_user_count          number(10);  --user¼ÆÊýÆ÷
  CURSOR C_USERS IS
          select wu.user_id, wu.comp_id
   from web$user wu
  where 1 = 1
    and exists (select null from seller$company where owner_id = wu.user_id)
    and not exists (select null from web$user_role wur where wur.user_id = wu.user_id);

BEGIN
  dbms_output.put_line(' begin.');
         for curr_user in C_USERS loop
            begin 
                  insert into gm_core.web$user_roles wur
                  (wur.user_role_id, wur.user_id, wur.comp_id, wur.role_type, wur.create_by,
                            wur.create_time, wur.last_update_by, wur.last_update_time
                  )
                  ( select gm_core.sq_web$user_role.nextval, curr_user.user_Id, curr_user.comp_Id,
                  1, 0, sysdate, 0, sysdate
                  from dual
                  );
                  
                  v_user_count := v_user_count+1;
                  dbms_output.put_line('The '||v_user_count||' user record had done.');
                  commit;
                  EXCEPTION when others then  
                            begin
                            dbms_output.put_line(' ERROR HINT. gm_core.acc$user_roles.user_id : ' || curr_user.user_Id);
                            continue;
                            end;
             end;
          end loop;
  dbms_output.put_line(' end.');
end;

