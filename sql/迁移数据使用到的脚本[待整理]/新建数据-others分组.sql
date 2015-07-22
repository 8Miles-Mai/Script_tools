declare
  v_comp_count          number(10);
--1.��ѯ��û�С�Others������Ĺ�˾�����������ִ�Сд
  CURSOR C_COMPS IS
      select sc.comp_id compId
        from seller$company sc
       where 1 = 1
         and sc.status in (0, 7)
         and not exists (select null
                from seller$product_group spg
               where spg.comp_id = sc.comp_id
                 and spg.prod_group_name = 'Others');

BEGIN
  dbms_output.put_line(' begin.');
--2.ѭ������˾
  for curr_comp in C_COMPS loop 
    begin
--3.���롮Others������
          insert into seller$product_group
          (prod_group_id, comp_id, prod_group_name, description, protected, unlock_key, 
          render_mode, seq_no, create_by, create_time, last_update_by,
           last_update_time, parent_group_id)
          (select sq_seller$product_group.nextval, curr_comp.compId, 'Others', null,
                  'N', null, 'S', null, 0, sysdate, 0, sysdate, null
             from dual);
          
          v_comp_count := v_comp_count+1;
          dbms_output.put_line('The '||v_comp_count||' comp record had done.');
          commit;
          EXCEPTION when others then  
            begin
            dbms_output.put_line(' ERROR HINT. seller$company.comp_id : ' || curr_comp.compId);
            continue;
            end;
    end;
  end loop;

  dbms_output.put_line(' end.');
end;

