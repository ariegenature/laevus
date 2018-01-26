-- name: !create-views
-- Create the views for reporting
create view full_report as (
  select obs.id as id,
    obs.date_time as date_time,
    grp.name as group_name,
    taxon.id as taxref_id,
    mname.value as scientific_name,
    string_agg(cname.value, ';') as common_names,
    obs.count_accuracy_id as count_accuracy,
    obs.count as count,
    obs.is_alive as is_alive,
    obs.comments as comments,
    obs.first_name as first_name,
    obs.surname as surname,
    obs.email as email,
    ST_AsText(ST_Transform(obs.geometry, 2154)) as geometry
  from public.contribution as obs
  left join public."group" as grp on obs.group_id = grp.id
  left join public.taxon as taxon on obs.specie_id = taxon.id
  left join public.scientific_name as mname on taxon.id = mname.taxon_id and mname.is_preferred = true
  left join public.common_name as cname on taxon.id = cname.taxon_id
  group by obs.id,
    obs.date_time,
    grp.name,
    taxon.id,
    mname.value,
    obs.count_accuracy_id,
    obs.count,
    obs.is_alive,
    obs.first_name,
    obs.surname,
    obs.email,
    obs.comments,
    obs.geometry
  order by obs.date_time desc
);
