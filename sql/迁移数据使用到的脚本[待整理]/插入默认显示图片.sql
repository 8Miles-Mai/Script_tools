declare
  v_comp_count          number(10);  --公司计数器
  CURSOR C_COMPS IS
         select sc.comp_id compId
         from seller$companies sc where sc.comp_id = 100609;

BEGIN
  dbms_output.put_line(' begin.');

  for curr_comp in C_COMPS loop 
    begin
    -- 1. 
    declare
    CURSOR C_PRODS IS
         select spp.product_id, spp.photo_s
  		from seller$prod_photos spp
 		where 1=1
   		and spp.is_default = 'Y'
   		and spp.product_id in (select sp.product_id
                            from seller$products sp
                           where 1 =1 
				and sp.comp_id = curr_comp.compId
				and sp.thumbnail is null);
           
           begin
             for curr_prod in C_PRODS loop
                begin 
			update seller$products sp
			   set sp.thumbnail = curr_prod.photo_s
			where sp.product_id = curr_prod.product_id;                      
                      commit;
                      EXCEPTION when others then  
                                begin
                                dbms_output.put_line(' ERROR HINT. gm_core.seller$products.product_id : ' || curr_prod.product_id);
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
