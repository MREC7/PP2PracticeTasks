create table if not exists contacts (
id serial primary key,
name varchar(255) not null,
phone varchar(10) not null
);

create or replace function search_contacts(pattern text)
returns table(id int, name varchar, phone varchar) as $$
begin
    return query
    select c.id, c.name, c.phone
    from contacts c
    where c.name ilike '%' || pattern || '%'
or c.phone ilike '%' || pattern || '%';
    end;
    $$ language plpgsql;

create or replace procedure insert_or_update_user(p_name text, p_phone text)
as $$
begin
    if exists (select 1 from contacts where name = p_name) then
update contacts set phone = p_phone where name = p_name;
    else
insert into contacts(name, phone) values (p_name, p_phone);
    end if;
end;
$$ language plpgsql;

create or replace procedure insert_many_users(
names text[],
phones text[],
out invalid_data text[]
)
as $$
declare i int;
begin
    invalid_data := array[]::text[];
    for i in 1..array_length(names, 1) loop
if phones[i] ~ '^[0-9]+$' then
    insert into contacts(name, phone)
    values (names[i], phones[i]);
else
    invalid_data := array_append(invalid_data, names[i] || ':' || phones[i]);
end if;
    end loop;
end;
$$ language plpgsql;

create or replace function get_contacts_paginated(lim int, off int)
returns table(id int, name varchar, phone varchar) as $$
begin
    return query
    select *
    from contacts
    order by name
    limit lim offset off;
end;
$$ language plpgsql;

create or replace procedure delete_contact(p_value text)
as $$
begin
    delete from contacts
    where name = p_value or phone = p_value;
end;
$$ language plpgsql;