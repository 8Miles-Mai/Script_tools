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
         select au.user_id userId, au.comp_id compId, au.parent_user_id parentUserId
         from acc$users au
         where 1=1
           and au.comp_id = curr_comp.compId
           and exists (select null from web$user wu where wu.user_id = au.user_id);
           
           begin
             for curr_user in C_USERS loop
                begin 
                      insert into web$user_relations wur
                      ( wur.user_rela_id, wur.user_id, wur.superior_user_id, wur.comp_id,
                        wur.create_by, wur.create_time, wur.last_update_by, wur.last_update_time
                      )
                      ( select gm_core.sq_web$user_relation.nextval, curr_user.userId, curr_user.parentUserId,
                               curr_user.compId, 0, sysdate, 0, sysdate
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

