-- Firstly, create this function

CREATE OR REPLACE FUNCTION public.process_audit()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
    BEGIN
        IF (TG_OP = 'DELETE') THEN
            INSERT INTO user_audit SELECT now(), 'D', old.id, old.username, old.email;
        ELSIF (TG_OP = 'UPDATE') THEN
            INSERT INTO user_audit SELECT now(), 'U', NEW.id, new.username, new.email;
        ELSIF (TG_OP = 'INSERT') THEN
            INSERT INTO user_audit SELECT now(), 'I', NEW.id, new.username, new.email;
        END IF;
        RETURN NULL;
    END;
$function$
;

-- Then, create trigger
create trigger audit_user after
insert
    or
delete
    or
update
    on
    public.users for each row execute function process_audit();