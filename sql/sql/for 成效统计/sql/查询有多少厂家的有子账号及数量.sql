
select temp.userNum, count(0) compNum
  from (select count(0) userNum
          from web$user wu
         where 1 = 1
         and wu.status = 7
           and exists (select null
                  from seller$company sc
                 where sc.comp_id = wu.comp_id and sc.status = 7 and sc.comp_level in ('A','B','C','D','E'))
         group by wu.comp_id
        
        ) temp
 where 1 = 1
   and temp.userNum > 1
 group by userNum
 
--22	1
--25	1
--6	224
--11	33
--13	9
--76	1
--2	1319
--14	9
--4	803
--5	265
--8	86
--17	1
--23	1
--3	898
--7	98
--15	5
--10	33
--9	45
--19	2
--12	18
--16	2

select count(0) from seller$company sc where sc.comp_level in ('A','B','C','D','E','F') and sc.status = 7;