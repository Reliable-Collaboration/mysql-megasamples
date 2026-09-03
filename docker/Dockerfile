# syntax=docker/dockerfile:1.7
# megasamples: MySQL LTS with sample databases baked into the data directory.
# The builder initialises a data directory, loads every core dataset from its MySQL Shell dump,
# creates the accounts and the provenance registry, and shuts down cleanly; the final stage carries
# only that directory. See PLAN.md section 2.2.
ARG MYSQL_VERSION=9.7.2

FROM mysql:${MYSQL_VERSION} AS builder
COPY docker/my.cnf /etc/mysql/conf.d/megasamples.cnf
COPY docker/init/ /build/init/
COPY build/dumps/ /build/dumps/
RUN <<'SH'
set -eux
S=/var/run/mysqld/mysqld.sock
mysqld --initialize-insecure --user=mysql
# util.loadDump uses LOAD DATA LOCAL INFILE, so local_infile must be ON for the import.
mysqld --user=mysql --daemonize --skip-networking --local-infile=1 \
       --socket=$S --pid-file=/var/run/mysqld/mysqld.pid
for i in $(seq 1 60); do mysql -S $S -uroot -e 'SELECT 1' >/dev/null 2>&1 && break; sleep 1; done

mysql -S $S -uroot -e "ALTER INSTANCE DISABLE INNODB REDO_LOG"
for dir in /build/dumps/*/; do
  mysqlsh --no-defaults -S $S -uroot --no-password --py \
    -e "util.load_dump('${dir}', {'deferTableIndexes': 'all', 'threads': 4, 'showProgress': False, 'skipBinlog': True})"
done
mysql -S $S -uroot -e "ALTER INSTANCE ENABLE INNODB REDO_LOG"

# CONVERT_TZ() needs the time-zone tables, which the entrypoint would normally load; it never runs
# here because the shipped data directory is already initialised.
mysql_tzinfo_to_sql /usr/share/zoneinfo 2>/dev/null | mysql -S $S -uroot mysql

# Accounts LAST: 00-users.sql gives root@localhost a password, so everything after it must
# authenticate. Running it earlier fails the rest of the stage (found at P-03).
mysql -S $S -uroot < /build/init/00-users.sql
mysql -S $S -uroot -proot < /build/init/10-registry.sql
mysqladmin -S $S -uroot -proot shutdown
rm -rf /build
SH

FROM mysql:${MYSQL_VERSION}
LABEL org.opencontainers.image.title="mysql-megasamples" \
      org.opencontainers.image.description="MySQL 9.7 LTS preloaded with well-known sample databases" \
      org.opencontainers.image.licenses="MIT AND BSD-3-Clause AND CC-BY-SA-3.0"
COPY docker/my.cnf /etc/mysql/conf.d/megasamples.cnf
COPY docker/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh
COPY --from=builder --chown=mysql:mysql /var/lib/mysql /var/lib/mysql
ENTRYPOINT ["entrypoint-wrapper.sh"]
EXPOSE 3306 33060
CMD ["mysqld"]
