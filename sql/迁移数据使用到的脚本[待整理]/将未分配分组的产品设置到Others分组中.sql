declare
  v_comp_count          number(10);
  v_groupId             number(10);
--1.��ѯ��˾id
  CURSOR C_COMPS IS
         select sc.comp_id compId
         from seller$company sc;

BEGIN
  dbms_output.put_line(' begin.');
--2.�Թ�˾Ϊ��λѭ������
  for curr_comp in C_COMPS loop 
    begin
-- 3.���ҵ���Others�������ID
    select spg.prod_group_id into v_groupId
          from seller$product_group spg
         where 1 = 1
           and spg.comp_id = curr_comp.compId
           and spg.prod_group_name = 'Others';
--4.���ù�˾û�����÷���Ĳ�Ʒ�����ߡ�����״̬��ȫ�����õ���Others��������
    insert into seller$pg_product spp                      
   (select gm_portal.sq_seller$pg_product.nextval,      
           v_groupId, sp.product_id, curr_comp.compId,           
           (select max(spd.seq_no) + 1                  
              from seller$pg_product spd                
             where spd.prod_group_id = v_groupId) seqNo, 
           0, sysdate, 0, sysdate           
      from seller$product sp, dual                      
     where 1 = 1                                        
       and sp.status in (7, 13, -3)                         
       and sp.comp_id = curr_comp.compId                    
       and not exists (select null                      
              from seller$pg_product spp                
             where spp.product_id = sp.product_id));
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

