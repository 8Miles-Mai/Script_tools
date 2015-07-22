declare
  v_comp_count          number(10);  --公司计数器
  v_user_count          number(10);  --user计数器
  CURSOR C_COMPS IS
         select sc.comp_id compId
         from seller$companies sc;

BEGIN
  dbms_output.put_line(' begin.');

  for curr_comp in C_COMPS loop 
    begin
    -- 1. 插入数据到 acc$users 表中
    declare
    CURSOR C_USERS IS
         select aur.user_id userId, aur.comp_id compId, ar.role_name roleName
         from acc$user_roles aur, acc$roles ar
         where 1=1
           and aur.comp_id = curr_comp.compId
           and aur.role_id = ar.role_id
           and ar.role_name in ('主账号','业务经理','业务员','制作员')
           and exists (select null from web$user wu where wu.user_id = aur.user_id);
           
           begin
             for curr_user in C_USERS loop
                begin 
                      insert into gm_core.web$user_roles wur
                      (wur.user_role_id, wur.user_id, wur.comp_id, wur.role_type, wur.create_by,
                                wur.create_time, wur.last_update_by, wur.last_update_time
                      )
                      ( select gm_core.sq_web$user_role.nextval, curr_user.userId, curr_user.compId,
                      decode(curr_user.roleName, '主账号', 1, '业务经理', 2, '业务员', 3, '制作员', 4),
                      0, sysdate, 0, sysdate
                      from dual
                      );
                      
                      v_user_count := v_user_count+1;
                      dbms_output.put_line('The '||v_user_count||' user record had done.');
                      commit;
                      EXCEPTION when others then  
                                begin
                                dbms_output.put_line(' ERROR HINT. gm_core.acc$user_roles.user_id : ' || curr_user.userId);
                                continue;
                                end;
                 end;
              end loop;
           end;
                     
    -- 4. 显示当前处理了多少条记录
    v_comp_count := v_comp_count+1;
    dbms_output.put_line('The '||v_comp_count||' comp record had done.');
  
  end;
  end loop;

  dbms_output.put_line(' end.');
end;

