declare
  CURSOR C_COMPS IS
         select sc.comp_id compId
         from seller$company sc;

BEGIN
  dbms_output.put_line(' begin.');
  for curr_comp in C_COMPS loop 
    begin
      declare
        CURSOR C_PRODS IS
          select sp.product_id prodId
            from seller$product sp
           where 1 = 1
             and sp.comp_id = curr_comp.compId
             and sp.status in (7, 13, -3)
             and sp.thumbnail is null
             and exists (select null
                           from seller$prod_photo spp
                          where spp.product_id = sp.product_id);
        begin
          for curr_prod in C_PRODS loop
            begin
              update seller$prod_photo spp
                 set spp.is_default = 'Y'
               where spp.product_id = curr_prod.prodId
                 and not exists (select null
                                   from seller$prod_photo spp1
                                  where 1 = 1
                                    and spp1.product_id = spp.product_id
                                    and spp1.is_default = 'Y')
                 and spp.prod_photo_id =
                    (select min(spp2.prod_photo_id)
                       from seller$prod_photo spp2
                      where spp2.product_id = spp.product_id);

              update seller$product sp
                 set sp.thumbnail = (select spp.photo_s
                                       from seller$prod_photo spp
                                      where spp.product_id = sp.product_id
                                        and spp.is_default = 'Y')
               where sp.product_id = curr_prod.prodId;
              commit;
              EXCEPTION when others then
                begin
                dbms_output.put_line(' ERROR HINT. seller$product.product_id : ' || curr_prod.prodId);
                end;
            end;
          end loop;
        end;
    end;
  end loop;
  dbms_output.put_line(' end.');
END;