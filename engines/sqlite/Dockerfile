# syntax=docker/dockerfile:1.7
# sql-megasamples-sqlite: the sample databases as SQLite files, with the sqlite3 shell beside them.
# One file per database under /data plus /data/megasamples.sqlite, the provenance registry. The
# context is the repository root filtered by .dockerignore; build/sqlite/image/data/ holds exactly the
# files being shipped. See ARCHITECTURE.md section 4.
#
#   docker run --rm -it sql-megasamples-sqlite:dev sqlite3 /data/sakila.sqlite     the shell, on one database
#   docker run -d --name sqlite sql-megasamples-sqlite:dev                          holds the files (the default command
#   docker exec -it sqlite sqlite3 /data/chinook.sqlite                              sleeps), so exec and volumes work
# alpine:3.22 on 2026-09-09, pinned by digest (docker image inspect)
ARG ALPINE_IMAGE=alpine@sha256:14358309a308569c32bdc37e2e0e9694be33a9d99e68afb0f5ff33cc1f695dce
FROM ${ALPINE_IMAGE}
RUN apk add --no-cache sqlite
LABEL org.opencontainers.image.title="sql-megasamples-sqlite" \
      org.opencontainers.image.description="Well-known sample databases as SQLite files, with the sqlite3 shell (sql-megasamples)" \
      org.opencontainers.image.licenses="MIT AND BSD-3-Clause AND CC-BY-SA-3.0"
COPY NOTICE.md LICENSES.md CATALOGUE.md README.md /usr/share/doc/megasamples/
COPY datasets/ /usr/share/doc/megasamples/datasets/
COPY build/sqlite/image/data/ /data/
VOLUME /data
WORKDIR /data
CMD ["sleep", "infinity"]
