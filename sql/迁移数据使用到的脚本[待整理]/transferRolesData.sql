CREATE OR REPLACE PACKAGE BODY GM_PORTAL.webuser_roleData_transfer
IS
	PROCEDURE transfer_roles_data (p_result	OUT VARCHAR2)
		IS
			e_locked_nowait   EXCEPTION;
			PRAGMA EXCEPTION_INIT (e_locked_nowait, -54);
		BEGIN
			p_result := 'fail';

			BEGIN
				FOR p_user_id IN (    
						SELECT aur.user_id
						  FROM gm_core.acc$user_roles aur, 
                   gm_core.acc$roles ar
						 WHERE aur.comp_id = ar.comp_id
						   AND ar.role_id = aur.role_id
						   AND ar.role_name in ('主账号', '业务经理', '业务员', '制作员')
						   FOR UPDATE NOWAIT
					)
				LOOP
					BEGIN
               --------------------------------------------------------------------------------------
						INSERT INTO web$user_roles (user_role_id, user_id, comp_id, role_type, create_by, create_time, last_update_by, last_update_time)
						(select sq_web$user_role.nextval,
						       aur.user_id,
						       aur.comp_id,
						       decode(ar.role_name, '主账号', 1, '业务经理', 2, '业务员', 3, '制作员', 4),
						       0,
						       sysdate,
						       0,
						       sysdate
						  from gm_core.acc$user_roles aur, gm_core.acc$roles ar
						 where aur.user_id = p_user_id.user_id
						   and ar.role_id = aur.role_id);
               		END;
				END LOOP;
				EXCEPTION
					WHEN e_locked_nowait
					THEN
						DBMS_OUTPUT.put_line ('Fail when select for update nowait');
					WHEN NO_DATA_FOUND
					THEN
						DBMS_OUTPUT.put_line ('No data found');
					WHEN TOO_MANY_ROWS
					THEN
						DBMS_OUTPUT.put_line ('Too many rows found');
					WHEN OTHERS
					THEN
						DBMS_OUTPUT.put_line ('Error info is ' || SQLERRM);
			END;

			IF p_result = 'success'
			THEN
				COMMIT;
			ELSE
				ROLLBACK;
			END IF;
   END transfer_roles_data;
END webuser_roleData_transfer;
