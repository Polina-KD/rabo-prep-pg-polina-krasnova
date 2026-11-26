# My answers — Block 2 (DBA DevOps Engineer)

Write every answer in your own words. Two to four sentences. No copied definitions.
If you used AI to help you, write what you checked.

## 1. Index

What did `EXPLAIN ANALYZE` show before and after your index (scan type and time)? What does an index
cost?
`ANSWER:`Before the index:
- Seq Scan.
- Execution time was higher.(45.262)

After the index:
- Index Scan.
- Execution time was lower because PostgreSQL could find the required rows faster using the 
  index.(0.309)

It costs disk space and can slow down write operations because the index must be updated 
whenever the data changes.

## 2. Partitioning

What is the difference between a partition and an index? When is partitioning useful?
`ANSWER:`An index helps PostgreSQL to search quickly. A partition divides a big table into
smaller once for example by month. PostgreSQL can search in relevant partition. For example, if
a table contains deployment records for several years, we can partition it by month.

## 3. Replication and high availability

What happened when you wrote on the replica? What is failover? Why do companies use a tool like
Patroni for it?
`ANSWER:`When I tried to write data to the replica, PostgreSQL returned an error because the
replica was in read-only mode. Failover is the process of switching to a standby server when the
primary server fails. Patroni monitors the database servers and can automatically promote a
healthy replica if the primary fails.

## 4. Replication or backup?

Your replica is a full copy. Why do you still need a backup? Give an example where the replica does
not help.
`ANSWER:`Replica is a synchronise copy. It makes the same changes as original but with a slight
delay. So if the original became dropped then the replica will repeat the same actions.

## 5. Backup and recovery

What is the difference between `pg_dump` and `pg_basebackup`? What are RPO and RTO? What does Barman
add?
`ANSWER:``pg_dump` writes the content of a table (or a database) to a file
`pg_basebackup` copies the whole database server, as files.
RPO - Recovery Point Objective. It is max size of data that the system cal loose.
RTO - Recovery Time Objective. It is max time for restore that can be spent.
Barman makes base backups, keeps all WAL files, and restores to a moment you choose
(point-in-time recovery).

## 6. Monitoring

Which checks does your monitoring script do? What is the difference between monitoring and
observability?
`ANSWER:`The monitoring script checks that db size, connections and replication lag are in the
normal numbers.
Monitoring checks what you know in advance, with a limit.
Observability is a property of the system that helps to find the cause of a new problem from
logs, metrics and traces.

## 7. Security

Explain least privilege with your roles `dashboard_reader` and `app_writer`. How do authentication,
authorisation, auditing and encryption differ?
`ANSWER:`I have to roles for different needs: `dashboard_reader` and `app_writer`
`dashboard_reader` are able to read the database. And `app_writer` are able to read and write in
the db. It means that nobody doesn't have more rights than it is necessary.

* authentication - checks who may connect from where and how.
* authorisation - checks who and what are allowed to do.
* auditing - checks who and what already did.
* encryption - guarantee that nobody can read it on the way or on the disk.

## 8. CI/CD for databases

What does your database pipeline check? Why does it run the migrations twice?
`ANSWER:`It checks linting, runs the migrations twice and runs tests. It runs the migrations
twice because it checks idempotency of migrations. After second run there shouldn't be any changes.

## 9. Idempotent automation

What does idempotent mean? Show it with `provision.py`. How does Ansible do the same?
`ANSWER:`An idempotent action means that the results of the action stay the same no matter how many
times this action is repeated.
In provision.py, I have a provision function that adds a database and two roles for a squad. And if
they have already been created, the result of retrying will be the same as the first time. So there
will be one database and two roles for the squad.
Ansible is an automation tool used to configure servers and manage infrastructure.
Instead of telling Ansible exactly how to create a database, you describe the desired state:

- The database must exist.
- The user must exist. etc.

Ansible checks the current state and makes only the changes necessary to reach the desired state.

## 10. On-premises, cloud, Kubernetes

What is the difference between running PostgreSQL yourself and AWS RDS or Azure Database for
PostgreSQL? What does a Kubernetes operator for PostgreSQL do?
`ANSWER:`With self-hosted PostgreSQL you manage the server, installation, updates and backups etc.
And provider of cloud service handles this tasks for you. You have less work but less control
at the same time.

## 11. AI

Did you use AI for SQL or `EXPLAIN` plans? What did you check?
`ANSWER:`I used AI for:
- explaining SQL and `EXPLAIN ANALYZE`;
- analyzing indexes and partitioning;
- verifying SQL for database roles;
- understanding and debugging `provision.py`;
- explaining idempotency and Ansible;

## 12. My question for the interviewer

Write one question about the work of the PostgreSQL Squad. Say what you know (vacancy) and what you
assume.
`ANSWER:`How does the team decide when to create an index or partition a table to improve query
performance?
