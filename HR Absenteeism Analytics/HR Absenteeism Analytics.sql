-- Joining tables 
select *
from work.dbo.Absenteeism_at_work a
left join work.dbo.compensation c 
on a.ID = c.ID
left join work.dbo.reasons r 
on a.Reason_for_absence  = r.Number

-- Finding the healthiest employee 
select * 
from work.dbo.Absenteeism_at_work
where Social_drinker = 0 and Social_smoker = 0 
and Body_mass_index < 25 and Absenteeism_time_in_hours < (select AVG(Absenteeism_time_in_hours) 
from work.dbo.Absenteeism_at_work)

-- Compensation rate increase for non-smoker | budget $9,83,222 which gives 0.68 times per hour which is $1,414
select count(*) as Non_Smokers from work.dbo.Absenteeism_at_work
where Social_smoker = 0

-- Optimising joined tables 
select 
a.ID,
r.Reason,
a.Body_mass_index,
case when Body_mass_index <18.5 then 'Underweight'
	 when Body_mass_index between 18.5 and 25 then 'Healthy'
	 when Body_mass_index between 25 and 30 then 'Overweight'
	 when Body_mass_index > 30 then 'Obese'
	 else 'unknown' end as BMI_Category,
case when Month_of_absence in (12,1,2) then 'Winter'
	 when Month_of_absence in (3,4,5) then 'Summer'
	 when Month_of_absence in (6,7,8,9) then 'Mansoon'
	 when Month_of_absence in (10,11) then 'Post mansoon'
	 else 'unknown' end as Seasons,
Month_of_absence,Day_of_the_week,Transportation_expense,
Education, Son, Social_drinker, Social_smoker,Pet,
Disciplinary_failure, Age, Work_load_Average_day,
Absenteeism_time_in_hours
from work.dbo.Absenteeism_at_work a
left join work.dbo.compensation c 
on a.ID = c.ID
left join work.dbo.reasons r 
on a.Reason_for_absence  = r.Number