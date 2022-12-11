


#SQL Notebook for Peer Assignment


#!pip install sqlalchemy==1.3.9
#!pip install ibm_db_sa
#!pip install ipython-sql


##Connect to the database
##Let us first load the SQL extension and establish a connection with the database

%load_ext sql


##DB2 magic in case of new UI service credentials. e.g:
%sql ibm_db_sa://my-username:my-password@my-hostname:my-port/my-db-name?security=SSL


%sql select name, coltype, length from sysibm.syscolumns where tbname ='SPACEXDATASET'


##Tasks
##Now write and execute SQL queries to solve the assignment tasks.
##
##Task 1
##Display the names of the unique launch sites in the space mission
%sql select distinct LAUNCH_SITE from SPACEXDATASET

##Task 2
##Display 5 records where launch sites begin with the string 'CCA'¶
%sql select * from SPACEXDATASET where LAUNCH_SITE like 'CCA%' limit 5

##Task 3¶
##Display the total payload mass carried by boosters launched by NASA (CRS)
%sql select SUM(PAYLOAD_MASS__KG_) from SPACEXDATASET where customer = 'NASA (CRS)'

##Task 4¶
##Display average payload mass carried by booster version F9 v1.1
%sql select AVG(PAYLOAD_MASS__KG_) from SPACEXDATASET where booster_version like 'F9 v1.1%'

##Task 5
##List the date when the first successful landing outcome in ground pad was acheived.¶
##Hint:Use min function

%sql select * from SPACEXDATASET where LANDING__OUTCOME = 'Success (ground pad)' and DATE = (select min(DATE) from SPACEXDATASET where LANDING__OUTCOME = 'Success (ground pad)')


##Task 6
##List the names of the boosters which have success in drone ship and have payload mass greater than 4000 but less than 6000¶
%sql select BOOSTER_VERSION from SPACEXDATASET where LANDING__OUTCOME = 'Success (drone ship)' and  PAYLOAD_MASS__KG_ BETWEEN 4000 AND 6000 


##Task 7¶
##List the total number of successful and failure mission outcomes
%sql select mission_outcome, count(*) from SPACEXDATASET group by mission_outcome


##Task 8
##List the names of the booster_versions which have carried the maximum payload mass. Use a subquery¶
%sql select distinct booster_version from SPACEXDATASET where PAYLOAD_MASS__KG_ = (select max(PAYLOAD_MASS__KG_) from SPACEXDATASET)

##Task 9
##List the failed landing_outcomes in drone ship, their booster versions, and launch site names for in year 2015¶
%sql select date, landing__outcome, booster_version, launch_site from SPACEXDATASET where landing__outcome = 'Failure (drone ship)' and year(date) = 2015


##Task 10
##Rank the count of landing outcomes (such as Failure (drone ship) or Success (ground pad)) between the date 2010-06-04 and 2017-03-20, in descending order¶
%sql select landing__outcome, count(*) as thecount from SPACEXDATASET where date between '2010-06-04' and '2017-03-20' group by landing__outcome ORDER BY thecount DESC 



