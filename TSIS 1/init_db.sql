create table if not exists contacts (
    id serial primary key,
    name varchar(255) not null,
    phone varchar(10)
);

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
            insert into contacts(name, phone) values (names[i], phones[i]);
        else
            invalid_data := array_append(invalid_data, names[i] || ':' || phones[i]);
        end if;
    end loop;
end;
$$ language plpgsql;

create or replace function get_contacts_paginated(lim int, off int)
returns table(id int, name varchar, email varchar, group_name varchar, phones text) as $$
begin
    return query
    select c.id, c.name, c.email,
           coalesce(g.name, 'No group'),
           coalesce(string_agg(p.phone || ' (' || p.type || ')', ', '), '')
    from contacts c
    left join phones p on p.contact_id = c.id
    left join groups g on g.id = c.group_id
    group by c.id, g.name
    order by c.name
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

create table if not exists groups (
    id serial primary key,
    name varchar(50) unique not null
);

alter table contacts
    add column if not exists email varchar(100),
    add column if not exists birthday date,
    add column if not exists group_id int references groups(id),
    add column if not exists created_at timestamp default current_timestamp,
    alter column phone drop not null;

create table if not exists phones (
    id serial primary key,
    contact_id int references contacts(id) on delete cascade,
    phone varchar(20) not null,
    type varchar(10) check (type in ('home','work','mobile'))
);

create or replace function search_contacts(pattern text)
returns table(id int, name varchar, email varchar, phone varchar) as $$
begin
    return query
    select distinct c.id, c.name, c.email, p.phone
    from contacts c
    left join phones p on p.contact_id = c.id
    where c.name ilike '%' || pattern || '%'
       or c.email ilike '%' || pattern || '%'
       or p.phone ilike '%' || pattern || '%';
end;
$$ language plpgsql;

create or replace procedure add_phone(p_name text, p_phone text, p_type text)
as $$
declare cid int;
begin
    select id into cid from contacts where name = p_name;
    if cid is null then
        raise exception 'contact not found';
    end if;

    insert into phones(contact_id, phone, type)
    values (cid, p_phone, p_type);
end;
$$ language plpgsql;

create or replace procedure move_to_group(p_name text, p_group text)
as $$
declare gid int;
begin
    if p_group is null then
        return;
    end if;

    select id into gid from groups where name = p_group;

    if gid is null then
        insert into groups(name) values (p_group)
        returning id into gid;
    end if;

    update contacts set group_id = gid where name = p_name;
end;
$$ language plpgsql;

create or replace procedure set_email(p_name text, p_email text)
as $$
begin
    update contacts
    set email = p_email
    where name = p_name;
end;
$$ language plpgsql;