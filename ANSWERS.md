# My answers — Block 2 (DBA DevOps Engineer)

Write every answer in your own words. Two to four sentences. No copied definitions.
If you used AI to help you, write what you checked.

## 1. Index
What did `EXPLAIN ANALYZE` show before and after your index (scan type and time)? What does an index cost?

## 2. Partitioning
What is the difference between a partition and an index? When is partitioning useful?

## 3. Replication and high availability
What happened when you wrote on the replica? What is failover? Why do companies use a tool like Patroni for it?

## 4. Replication or backup?
Your replica is a full copy. Why do you still need a backup? Give an example where the replica does not help.

## 5. Backup and recovery
What is the difference between `pg_dump` and `pg_basebackup`? What are RPO and RTO? What does Barman add?

## 6. Monitoring
Which checks does your monitoring script do? What is the difference between monitoring and observability?

## 7. Security
Explain least privilege with your roles `dashboard_reader` and `app_writer`. How do authentication, authorisation, auditing and encryption differ?

## 8. CI/CD for databases
What does your database pipeline check? Why does it run the migrations twice?

## 9. Idempotent automation
What does idempotent mean? Show it with `provision.py`. How does Ansible do the same?

## 10. On-premises, cloud, Kubernetes
What is the difference between running PostgreSQL yourself and AWS RDS or Azure Database for PostgreSQL? What does a Kubernetes operator for PostgreSQL do?

## 11. AI
Did you use AI for SQL or `EXPLAIN` plans? What did you check?

## 12. My question for the interviewer
Write one question about the work of the PostgreSQL Squad. Say what you know (vacancy) and what you assume.
