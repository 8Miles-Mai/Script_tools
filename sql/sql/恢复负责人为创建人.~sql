INSERT INTO seller$object_assignment
  (object_assign_id,
   comp_id,
   assigner,
   keeper,
   rule_assign_id,
   enabled,
   entity_source,
   entity_id,
   create_by,
   create_time,
   last_update_by,
   last_update_time)
  (SELECT sq_seller$object_assignment.nextVal,
          comp_Id,
          926836,
          spd.create_by,
          86740,
          'Y',
          53,
          spd.product_Id,
          926836,
          sysdate,
          926836,
          sysdate
          --select count(0)
     FROM seller$product spd
    WHERE spd.comp_id = 1943580
      and spd.status in (7, 13, -3, 0)
      AND spd.product_id not in
          ( select soa.entity_id
             from seller$object_assignment soa
            where soa.comp_id = 1943580
              and soa.entity_source = 53))
      
     