/*
1)
*/
CREATE OR REPLACE PROCEDURE prcd_table_delete_started_TableName()
LANGUAGE plpgsql
AS $$
BEGIN
    LOOP
        if (SELECT count(table_name) FROM information_schema.tables
            where table_name like 'TableName%') = 0
        THEN
            exit;
        END IF;
        EXECUTE concat('drop table "',
                       (SELECT table_name FROM information_schema.tables
                        WHERE table_name like 'TableName%'
                        LIMIT 1),
                       '"');
    END loop;
END; $$
/*
2)
*/
CREATE or REPLACE PROCEDURE prcdr_amount_list_funcs_with_arguments(
	funcs out text,
	numb out int
)
LANGUAGE plpgsql
AS $$
DECLARE
	line record;
BEGIN
	funcs := '';
	numb := 0;
	FOR line IN
		SELECT (
				p.proname || ' (' || pg_get_function_arguments(p.oid) || ')'
			) AS functions_list
		FROM pg_catalog.pg_namespace n
			JOIN pg_catalog.pg_proc p ON p.pronamespace = n.oid
		WHERE p.prokind = 'f'
			AND n.nspname = 'public'
			and (pg_get_function_arguments(p.oid) = '') IS NOT true
	LOOP
		funcs := (funcs || line.functions_list || E'\n');
		numb := numb + 1;
	END LOOP;
END;
$$
/*
3)
*/
CREATE OR REPLACE PROCEDURE prcdr_destroy_DML_triggers(num out int) 
LANGUAGE plpgsql
AS $$
DECLARE
	i record;
BEGIN
	num := 0;
	for i IN
		SELECT *
		from information_schema.triggers
		WHERE event_manipulation IN ('DELETE', 'UPDATE', 'INSERT')
	loop
		EXECUTE 'drop trigger ' || i.trigger_name || ' on '
			|| i.event_object_table || ' cascade';
		num := num + 1;
	END LOOP;
END;
$$
/*
4)
*/
CREATE or REPLACE PROCEDURE prcd_find_func_proc_with_substr(sub in text, list out text)
language plpgsql
as $$
DECLARE
    line record;
	typeof text;
BEGIN
    list = '';
    for line in 
                select proname, prokind from pg_proc
				join information_schema.ROUTINES
				on concat(proname, '_', pg_proc.oid) = specific_name
				where specific_schema = 'public' and prokind in ('f', 'p')
												 and prosrc ~ sub
    loop
				if line.prokind = 'f'
				then typeof := 'function';
				else typeof := 'procedure';
				end if;
                list := concat(list, 'name: ', line.proname, ' | type: ', typeof, E'\n');
    end loop;
end;
$$
